#!/usr/bin/env python3
"""
Optimise the original photographs for the website.

What it does
------------
* Reads originals named photo-NN.jpg / .jpeg / .png / .webp from a source folder
  (default: ./source-photos  -- this folder is git-ignored, originals never get committed).
* Fixes phone rotation (EXIF orientation), converts to sRGB and STRIPS ALL METADATA
  (GPS position, device model, timestamps) by never writing it to the output.
* Writes responsive WebP files:  assets/images/photo-NN-640.webp, -1080.webp, -1440.webp
  (only sizes that do not enlarge the original; the native width is added when it is
  clearly larger than the biggest standard size).
* Creates derived crops (for example the welcome-screen crop of photo 9).
* Applies gentle per-photo colour adjustments (see ADJUST).
* Writes js/photo-manifest.js so the website knows which sizes exist.

Usage
-----
    pip install pillow
    python3 tools/optimize_images.py                 # uses ./source-photos
    python3 tools/optimize_images.py --src /path/to/originals

Add a new photo: put photo-12.jpg in the source folder, run this script, then add
{ id: "photo-12", alt: "..." } to the gallery list in js/content.js.
"""
import argparse
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageCms, ImageEnhance, ImageOps

WIDTHS = (640, 1080, 1440)   # responsive sizes (pixels wide)
QUALITY = 76                  # WebP quality: 74-80 is a good phone/size balance
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Derived crops. Fractions of the (rotated) original: (left, top, right, bottom).
# Fractions, not pixels, so the crop still works if you swap in a higher-resolution original.
DERIVED = {
    # Welcome-screen crop of photo 9: trims the door on the left, keeps her face and torso.
    "photo-09-hero": ("photo-09", (0.26, 0.04, 1.00, 0.73)),
}

# Gentle, natural colour adjustments (1.0 = unchanged). Never force photos to match the site palette.
ADJUST = {
    # Photo 11 arrived heavily saturated, with a magenta cast.
    "photo-11": {"saturation": 0.84, "contrast": 0.98},
}

ROOT = Path(__file__).resolve().parent.parent


def to_srgb(im):
    icc = im.info.get("icc_profile")
    if icc:
        try:
            src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
            dst = ImageCms.createProfile("sRGB")
            im = ImageCms.profileToProfile(im, src, dst, outputMode="RGB")
        except Exception:
            pass
    return im.convert("RGB")


def load(path):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)  # apply the phone's rotation flag
    return to_srgb(im)


def adjust(im, photo_id):
    opts = ADJUST.get(photo_id)
    if not opts:
        return im
    if "saturation" in opts:
        im = ImageEnhance.Color(im).enhance(opts["saturation"])
    if "contrast" in opts:
        im = ImageEnhance.Contrast(im).enhance(opts["contrast"])
    return im


def variant_widths(width):
    widths = [w for w in WIDTHS if w <= width]
    if not widths:
        return [width]
    # Add the native width only for mid-sized originals (e.g. 813, 1024, 1333 px wide).
    # Very large originals are capped at the biggest standard size to keep files light.
    if widths[-1] * 1.1 < width <= WIDTHS[-1] + 160:
        widths.append(width)
    return widths


def save_variants(im, photo_id, out_dir):
    out = {}
    width, height = im.size
    for w in variant_widths(width):
        h = round(height * w / width)
        resized = im if w == width else im.resize((w, h), Image.LANCZOS)
        target = out_dir / f"{photo_id}-{w}.webp"
        # No exif= / icc_profile= arguments: nothing from the original is carried over.
        resized.save(target, "WEBP", quality=QUALITY, method=6)
        out[w] = (h, target.stat().st_size)
    widths = sorted(out)
    biggest = widths[-1]
    return {"w": biggest, "h": out[biggest][0], "widths": widths}, out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src", default=str(ROOT / "source-photos"), help="folder with originals (photo-NN.jpg ...)")
    parser.add_argument("--out", default=str(ROOT / "assets" / "images"), help="output folder")
    parser.add_argument("--manifest", default=str(ROOT / "js" / "photo-manifest.js"))
    args = parser.parse_args()

    src_dir, out_dir = Path(args.src), Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    originals = {}
    for p in sorted(src_dir.iterdir()):
        if p.suffix.lower() in EXTENSIONS and re.fullmatch(r"photo-\d{2,3}", p.stem):
            originals[p.stem] = p
    if not originals:
        sys.exit(f"No files named photo-NN.jpg/.png/.webp found in {src_dir}")

    manifest, total = {}, 0
    images = {}
    for photo_id, path in originals.items():
        im = adjust(load(path), photo_id)
        images[photo_id] = im
        info, sizes = save_variants(im, photo_id, out_dir)
        manifest[photo_id] = info
        total += sum(s for _, s in sizes.values())
        print(f"{photo_id}: {im.size[0]}x{im.size[1]} -> " + ", ".join(f"{w}w {s//1024}KB" for w, (_, s) in sorted(sizes.items())))

    for new_id, (base_id, box) in DERIVED.items():
        if base_id not in images:
            print(f"skip {new_id}: {base_id} not found")
            continue
        base = images[base_id]
        w, h = base.size
        crop = base.crop((round(box[0] * w), round(box[1] * h), round(box[2] * w), round(box[3] * h)))
        info, sizes = save_variants(crop, new_id, out_dir)
        manifest[new_id] = info
        total += sum(s for _, s in sizes.values())
        print(f"{new_id}: crop {crop.size[0]}x{crop.size[1]} -> " + ", ".join(f"{w}w {s//1024}KB" for w, (_, s) in sorted(sizes.items())))

    header = (
        "/* GENERATED by tools/optimize_images.py - do not edit by hand.\n"
        "   Lists which responsive sizes exist for each photo id. */\n"
    )
    Path(args.manifest).write_text(
        header + "window.PHOTO_MANIFEST = " + json.dumps(manifest, indent=2, sort_keys=True) + ";\n",
        encoding="utf-8",
    )
    print(f"\nDone. {len(manifest)} photos, {total // 1024} KB of WebP written to {out_dir}")


if __name__ == "__main__":
    main()
