/**
 * Cyrillic-capable font stack.
 *
 * Any storybook display font adopted later MUST be verified for Cyrillic
 * coverage — and for Bulgarian glyph forms specifically, since some Cyrillic
 * fonts default to Russian shapes. A Latin-only font renders every string in
 * the game as blank boxes. If Phaser bitmap fonts are used, the atlas must be
 * generated with the Cyrillic block included.
 */
export const FONT_STACK = 'Georgia, "DejaVu Serif", "Liberation Serif", serif';
