import { FONT_STACK } from './fonts';
import { prefersReducedMotion } from './reduced-motion';

import type { Scene } from 'phaser';

/**
 * The shared puzzle overlay (09-09 task #3): opens over the dimmed walking view, hosts a puzzle, and closes. Every
 * level and every puzzle type uses this one overlay.
 *
 * E1 hosts no engine yet, so `body` is `ui.puzzle.coming-soon` for every marker. The engines (E3+) replace the body
 * and call `onSolved`, which the level wires to the progress write.
 *
 * Motion: a 200 ms fade. Reduced motion (owner, 2026-10-07): it appears and goes in one frame.
 * Screen-fixed and re-laid out on resize (the game runs Scale.RESIZE). The dim swallows pointer input; the level
 * freezes the player itself while `isOpen`.
 */

export interface OverlayContent {
  readonly title: string;
  readonly body: string;
  readonly closeLabel: string;
}

export interface OverlayCallbacks {
  /** The hosted puzzle reported a solve. The level commits it (progress-write.ts) and lets the companion speak. */
  readonly onSolved: () => void;
  /** The overlay is gone: the level unfreezes the player. */
  readonly onClosed: () => void;
}

export interface PuzzleOverlay {
  readonly isOpen: () => boolean;
  /** Called by the hosted engine (E3+) when the child solves the puzzle. Once per opening. */
  readonly solve: () => void;
  readonly close: () => void;
}

const FADE_MS = 200;
const DEPTH = 1000;
const PANEL_MAX_WIDTH = 640;
const MARGIN = 16;
const PAD = 24;
const BUTTON = { width: 140, height: 48 }; // at least 44 x 44 (standards-frontend.md)

/** Screen-fixed: the overlay stays put while the level camera follows the player. */
function fixed<T extends Phaser.GameObjects.Components.ScrollFactor>(object: T): T {
  return object.setScrollFactor(0);
}

export function openPuzzleOverlay(
  scene: Scene,
  content: OverlayContent,
  callbacks: OverlayCallbacks,
  reduced = prefersReducedMotion(),
): PuzzleOverlay {
  let open = true;
  let solved = false;

  const dim = fixed(
    scene.add.rectangle(0, 0, 10, 10, 0x05_08_14, 0.72).setOrigin(0).setDepth(DEPTH),
  );
  dim.setInteractive(); // swallows taps on the markers underneath
  const panel = fixed(
    scene.add
      .rectangle(0, 0, 10, 10, 0x1c_2a_5e)
      .setStrokeStyle(2, 0xf4_e6_c3)
      .setDepth(DEPTH + 1),
  );
  const title = fixed(
    scene.add
      .text(0, 0, content.title, {
        fontFamily: FONT_STACK,
        fontSize: '26px',
        color: '#f4e6c3',
        align: 'center',
      })
      .setOrigin(0.5, 0)
      .setDepth(DEPTH + 2),
  );
  const body = fixed(
    scene.add
      .text(0, 0, content.body, {
        fontFamily: FONT_STACK,
        fontSize: '18px',
        color: '#dfe4ff',
        align: 'center',
      })
      .setOrigin(0.5, 0)
      .setDepth(DEPTH + 2),
  );
  const button = fixed(
    scene.add
      .rectangle(0, 0, BUTTON.width, BUTTON.height, 0x0b_10_26)
      .setStrokeStyle(2, 0xf4_e6_c3)
      .setDepth(DEPTH + 2)
      .setInteractive({ useHandCursor: true }),
  );
  const buttonLabel = fixed(
    scene.add
      .text(0, 0, content.closeLabel, {
        fontFamily: FONT_STACK,
        fontSize: '18px',
        color: '#f4e6c3',
      })
      .setOrigin(0.5)
      .setDepth(DEPTH + 3),
  );
  const parts = [dim, panel, title, body, button, buttonLabel];

  const layout = (): void => {
    const { width, height } = scene.scale;
    const panelWidth = Math.min(width - 2 * MARGIN, PANEL_MAX_WIDTH);
    title.setWordWrapWidth(panelWidth - 2 * PAD);
    body.setWordWrapWidth(panelWidth - 2 * PAD);
    const panelHeight = PAD + title.height + PAD + body.height + PAD + BUTTON.height + PAD;
    const top = Math.max(MARGIN, (height - panelHeight) / 2);
    dim.setSize(width, height);
    (dim.input?.hitArea as Phaser.Geom.Rectangle | undefined)?.setTo(0, 0, width, height);
    panel.setSize(panelWidth, panelHeight).setPosition(width / 2, top + panelHeight / 2);
    title.setPosition(width / 2, top + PAD);
    body.setPosition(width / 2, top + PAD + title.height + PAD);
    const buttonY = top + panelHeight - PAD - BUTTON.height / 2;
    button.setPosition(width / 2, buttonY);
    buttonLabel.setPosition(width / 2, buttonY);
  };
  layout();
  scene.scale.on('resize', layout);

  const destroy = (): void => {
    scene.scale.off('resize', layout);
    for (const part of parts) part.destroy();
    callbacks.onClosed();
  };

  const close = (): void => {
    if (!open) return;
    open = false;
    button.disableInteractive();
    if (reduced) {
      destroy();
      return;
    }
    scene.tweens.add({ targets: parts, alpha: 0, duration: FADE_MS, onComplete: destroy });
  };
  button.on('pointerup', close);

  if (!reduced) {
    for (const part of parts) part.setAlpha(0);
    scene.tweens.add({ targets: parts, alpha: 1, duration: FADE_MS });
  }

  const solve = (): void => {
    if (!open || solved) return;
    solved = true;
    callbacks.onSolved();
  };

  return { isOpen: () => open, solve, close };
}
