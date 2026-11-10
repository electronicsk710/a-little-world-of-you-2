# A Little World of You: Engineering Report (v1.0 first build)

Stack: HTML5, CSS3, vanilla JavaScript. No frameworks, no analytics, no external requests (fonts and images are self-hosted).
Measured weight (390 px wide, 3x phone screen, fast connection, no scrolling): the first screen needs about 250 KB
(HTML/CSS/JS 43 KB, fonts 147 KB, welcome photo 59 KB). The browser then also pre-fetches the first few gallery photos
as part of its lazy-loading margin, which brought the total to about 1.1 MB after 2.5 seconds. The remaining photos load as she scrolls
(about 60-320 KB each). On slow connections browsers fetch less ahead. I did not test real mobile networks.

## 1. Decisions I made that you should know about

| Decision | Reason | How to reverse |
|---|---|---|
| **Photo 1 (tree, another person) excluded.** The gallery has 8 photos plus the welcome photo, not 10. | Your rule: crop only if natural, otherwise drop it. She stands at the edge of the frame with her hand touching his jacket, and a clean crop would be narrow and low resolution. | Supply a clean crop, name it `photo-01`, run the image tool, add a line in `gallery.photos`. |
| **Welcome photo = a crop of photo 9** (`photo-09-hero`). | Removes the door on the left so the cream wall fills the arch and blends into the page. | Change `welcome.photo.id`, or the crop fractions in `tools/optimize_images.py`. |
| **Photo 5 = the blurred-background version.** | Other people's faces are blurred. | n/a |
| **Photo 11 gently corrected** (saturation x0.84, contrast x0.98). | It arrived over-saturated with a magenta cast. Skin tones are unchanged and it is not graded to the site palette. | `ADJUST` in `tools/optimize_images.py`. |
| **Everything scrolls on one page; "Come in" scrolls to the gallery** and starts music if configured. | The letter is never hidden behind an interaction. The button still acts as the consent tap for audio. | n/a |
| **Letter body set in Fraunces** (18 px on phones, 20 px on tablets and up), headings in Fraunces, UI and captions in DM Sans. | The letter should feel written, not like web copy. | `.letter__p` in `css/style.css` |
| **Words are placeholders in `js/content.js`.** | I do not invent names, memories or feelings. | n/a |
| **Welcome "Come in" label kept** as you proposed. | No strong design reason to change it. | `welcome.buttonLabel` |
| **WebP images only** (no JPEG fallback). | WebP is supported by all current Android and iOS browsers (iOS 14+). Halves the file size. | n/a |

## 2. Important interactions

- **Welcome:** a soft staggered fade-up on load. **Come in** scrolls to the gallery heading, moves keyboard focus there, and starts music only if configured.
- **Gallery:** a single column on phones with deliberate variation (full width, 82% inset left or right, ochre mat on two photos), photos at natural proportions, lazy-loaded. Two staggered columns from 768 px.
- **Lightbox** (native `<dialog>`): tap a photo to open; previous/next buttons (48 px), swipe left or right, arrow keys, Esc, tap the dark area, or the X to close. Focus returns to the photo you opened. Neighbouring photos are preloaded. Photos that are missing are skipped.
- **Letter:** paragraphs fade up as she reads. A soft background shift from cream to warm paper and a short heading make the transition; no loading screen or extra click.
- **Closing:** italic closing line, a crimson italic signature, and a quiet **Back to the photos** link.
- **Music:** prepared but inactive. When enabled: audio object created, nothing downloaded until the tap, fade-in, a 48 px play/pause button, pauses when the page is hidden and resumes if she had not paused it, and the button disappears quietly if the file cannot be loaded.

## 3. Accessibility

- Semantic landmarks, one `h1`, section `h2`s, labelled sections, a "Skip to the letter" link.
- Descriptive `alt` text on every photo; photo buttons are labelled "Enlarge photo: ...".
- Visible focus rings on every control (3 px, offset). Lightbox is a modal `<dialog>` (focus trapped, background inert, Esc closes) with a live-region photo counter.
- Touch targets: Come in 152x52, lightbox and music buttons 48x48, photo buttons full width, return link 48 px tall. No hover-only interactions (hover styles are limited to `@media (hover: hover)`).
- `prefers-reduced-motion`: all entrance animations, reveals, smooth scrolling and the lightbox fade are switched off; content is simply visible.
- Contrast (calculated): espresso on cream 15.05:1, cocoa on cream 9.78:1, crimson on cream 5.67:1, cream on crimson 5.67:1, espresso on paper 13.58:1, crimson on paper 5.12:1 (used only for the large signature), espresso on ochre 9.76:1. **Never** put ochre text on cream (1.54:1) or small crimson text on ochre (3.68:1). Sage is defined but intentionally unused.
- Music is never required; the site is complete without sound. Nothing important is conveyed by colour or sound alone.

## 4. Performance

- Responsive WebP (640 / 1080 / 1440 px, plus the native width for mid-sized originals) with `srcset` and `sizes`; the 24 files total about 2.7 MB across all sizes, and a phone downloads only one size per photo (the 1440 px size is used by the lightbox on large or high-density screens).
- Welcome photo eager with `fetchpriority="high"`; gallery photos lazy; intrinsic `width`/`height` on every image so nothing jumps.
- Fonts: three self-hosted Latin-subset files (147 KB in total), `font-display: swap`, all three preloaded, real fallback stacks.
- Animations use only opacity and transform. 457 lines of JavaScript (16 KB, no dependencies) plus a 108-line content file. Audio is not downloaded until playback.

## 5. Privacy and security

- Image tool strips all metadata (no GPS, device or dates) and never carries anything over from the originals.
- `noindex, nofollow, noarchive`, `referrer: no-referrer`, no link-preview image, no trackers, no third-party requests, no keys or credentials.
- Text from `content.js` is inserted with DOM text nodes (never `innerHTML`), so nothing typed there can inject markup.
- Originals are git-ignored. **Hosting still decides privacy**; see the README. The site has not been published anywhere.

## 6. What was tested, and how (be aware of the limits)

Automated checks with Chromium (Playwright) using touch emulation at **360x740, 375x812, 390x844 and 430x932**, plus a 1280x800 desktop window: 55 of 55 checks passed.

- No horizontal overflow and no clipped elements at all four phone widths; the welcome screen fits one screen (button bottom edge at 650 / 702 / 725 / 791 px).
- Fonts load (Fraunces roman and italic, DM Sans); all photos load at the expected sizes and keep their proportions.
- Tap targets are at least 44 px; letter text is 18 px with 22 px side margins (about 34-42 characters per line).
- "Come in" lands on the gallery with focus on its heading.
- Lightbox: opens on tap, fits the screen, next/previous, arrow keys, swipe left and right with real touch events, Esc closes, focus returns to a photo, the close button works.
- Reduced motion: nothing hidden, no entrance animation, no smooth scrolling.
- No console errors or failed requests in the default configuration.
- In a throwaway copy (not shipped) I also tested: music switched on with a silent test tone (button visible, no audio request before the tap, audio requested after it, play/pause toggles, 48 px button), a deleted photo (clear fallback box, lightbox skips it, "Photo 1 of 7"), and a long unbroken word in the letter (wraps, no overflow). I also reviewed screenshots of the welcome, gallery, lightbox, letter and desktop layouts.

**NOT tested** (you must do these): a real iPhone or Android device, Safari/WebKit, WhatsApp's in-app browser, real network conditions, a screen reader (VoiceOver/TalkBack), and the actual letter text and captions (not written yet). Treat all browser results above as Chromium-only.

## 7. Known limitations and things to watch

- **iPhone audio:** iOS ignores programmatic volume, so the fade-in will not fade there; master the track quietly.
- **Music button over text:** when music is enabled, the fixed button can briefly cover the end of a line while scrolling through the letter. Say so if you want it moved or hidden in the letter.
- **Android Back button:** it leaves the page, rather than just closing the photo viewer (the viewer's own X, tap-outside and swipe all work).
- Older browsers without `<dialog>` get a simpler fallback viewer; very old browsers without WebP show the photo-missing box.
- Without JavaScript the page shows a message instead of the content (everything is rendered from `content.js`).
- Photo order on tablets and laptops reads left-to-right in pairs (3+4, 6+7, 2+11, 5+10); with different photos, check the pairings.
- Contrast numbers are calculated by formula, not checked with an external tool; colours are still estimates by eye from the photographs, not pixel-sampled.

## 8. Still needs your input

1. The words: name, welcome message, headings, the letter, closing and signature (and any captions).
2. Confirm photo 1 stays out (or supply a clean crop).
3. Confirm hero = photo 9 and the gallery order.
4. The music file and its licence, then flip `music.enabled`.
5. Hosting and privacy choice, and when she should receive the link.
6. A real-phone check (Android and iPhone, in WhatsApp).
