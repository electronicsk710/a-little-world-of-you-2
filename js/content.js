/* =============================================================================
   A LITTLE WORLD OF YOU - EDITABLE CONTENT
   =============================================================================
   This is the ONE file you edit to change the words, photos and music.
   Anything in [square brackets] is a PLACEHOLDER: replace it with your own words.

   Typography tip: put *asterisks* around a few words inside the letter, the welcome
   message or captions to set them in italics. Example:  "You make *ordinary days* feel
   lighter."
   ============================================================================= */

window.SITE_CONTENT = {

  siteTitle: "A Little World of You",

  /* ---------------------------------------------------------------- WELCOME */
  welcome: {
    eyebrow: "A Little World of You",
    name: "Tattiana Macrotta",
    message: "A little something, just for you",
    buttonLabel: "Come in",

    /* The welcome photo. `id` is a file prefix in assets/images/ (see README).
       To use a different photo, change the id, e.g. "photo-03" (or make a new crop
       in tools/optimize_images.py). `position` moves the focus point of the frame. */
    photo: {
      id: "photo-09-hero",
      alt: "She sits on a stool against a cream wall, smiling warmly at the camera with a phone in her hands.",
      position: "50% 30%"
    }
  },

  /* ---------------------------------------------------------------- GALLERY */
  gallery: {
    eyebrow: "Gallery",
    title: "A Few Lovely Moments",
    intro: "Little glimpses worth keeping",   /* optional line under the heading; leave empty to hide */

    /* The ORDER of this list is the order on the page. To reorder, move a line.
       To remove a photo, delete its line. 
       Per photo:
         id      file prefix in assets/images/  (photo-03 -> photo-03-640.webp ...)
         alt     describes the photo for screen readers (please keep it meaningful)
         caption optional; leave "" for none. Use captions only where they add meaning.
         size    "full" (full width) or "inset" (a little narrower, for rhythm)
         align   "center", "left" or "right" (used by "inset")
         mat     true = sits on a soft ochre mat                                       */
    photos: [
      { id: "photo-03", size: "full",  align: "center", mat: false, caption: "",
        alt: "She stands in warm evening sunlight against a yellow wall in a brown dress, resting her chin on her hand and smiling." },

      { id: "photo-04", size: "inset", align: "right",  mat: true,  caption: "",
        alt: "A close, playful selfie in a brown top, lips pursed, in bright sunlight beside white window frames." },

      { id: "photo-06", size: "inset", align: "left",   mat: false, caption: "",
        alt: "Smiling with her head tilted, in front of green palm leaves, wearing a black blazer over a red dress." },

      { id: "photo-07", size: "full",  align: "center", mat: false, caption: "",
        alt: "A full-length portrait on a balcony among palm trees, in a black blazer, red dress and black shoes." },

      { id: "photo-02", size: "inset", align: "right",  mat: false, caption: "",
        alt: "Smiling at the camera in a cafe, with a tall glass of orange juice in front of her." },

      { id: "photo-11", size: "full",  align: "center", mat: false, caption: "",
        alt: "Standing on grass in a light-blue shirt, dark vest and burgundy trousers, one hand on her shoulder, smiling." },

      { id: "photo-05", size: "inset", align: "left",   mat: false, caption: "",
        alt: "Standing in a warm yellow hall in a brown dress, looking calmly to one side, the background softly blurred." },

      { id: "photo-10", size: "full",  align: "center", mat: true,  caption: "",
        alt: "Seated on a stool and laughing with her head tilted back, a phone in her hands." }
    ]
  },

  /* ----------------------------------------------------------------- LETTER */
  letter: {
    eyebrow: "A letter",
    title: "Something I Wanted You to Know.",
    preface: "To the one who has quietly won my heart.",

    salutation: "Dear Tatianna,",

    /* One entry = one paragraph. Write as you would speak to her. */
    paragraphs: [
      "I was actually planning to wait until your birthday to show you this, but I guess I couldn't keep it to myself any longer. So, you can consider this your little early birthday gift.",
      "I really love your smile, your laugh, your playful side and that joyful personality of yours. Honestly, it's the little things that make you who you are, and I wouldn't want you any other way.",
      "There's something else I want you to know: as time goes by, I find myself falling for you even more. Sometimes I feel like I like you more than you like me, and funny enough, I'm perfectly happy with that.Don't feel intimidated, though. You don't have to catch up; I just wanted you to know how I feel."
    ],

    closing: "Your Boyfriend",
    signature: "Tedd Finley",

    backToGalleryLabel: "Back to the photos"
  },

  /* ------------------------------------------------------------------ MUSIC */
  /* TODO: ADD BACKGROUND MUSIC HERE
     1. Put your licensed audio file at  assets/music/background.mp3
     2. Change  enabled: false  to  enabled: true
     That is all. While `enabled` is false the site creates no audio and shows no
     music button. See README.md > "Adding music". */
  music: {
    enabled: true,
    src: "assets/music/background.mp3",
    volume: 0.35,        /* 0 to 1. (iPhones ignore this; keep the track itself quiet) */
    fadeInSeconds: 2.5
  }
};
