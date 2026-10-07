import { FONT_STACK } from './fonts';

import type { Scene } from 'phaser';

/**
 * The companion's speech box: screen-fixed at the bottom, above the puzzle overlay. It speaks the tier lines
 * (companion-tiers.ts) and the success fact. Text wraps and the box grows with it: Bulgarian runs long (rule 3).
 *
 * No animation of its own: it appears and goes with the overlay, so it needs no reduced path (CF A12).
 * Colours: #f4e6c3 on #0b1026, well above 4.5:1 (standards-frontend.md).
 */

const MAX_WIDTH = 640;
const MARGIN = 16;
const PAD = 14;
const DEPTH = 1100;

export interface CompanionBox {
  show: (text: string) => void;
  hide: () => void;
  destroy: () => void;
}

export function createCompanionBox(scene: Scene): CompanionBox {
  const panel = scene.add
    .rectangle(0, 0, 10, 10, 0x0b_10_26, 0.95)
    .setStrokeStyle(2, 0xf4_e6_c3)
    .setOrigin(0.5, 1)
    .setScrollFactor(0)
    .setDepth(DEPTH)
    .setVisible(false);
  const text = scene.add
    .text(0, 0, '', {
      fontFamily: FONT_STACK,
      fontSize: '18px',
      color: '#f4e6c3',
      align: 'center',
    })
    .setOrigin(0.5, 1)
    .setScrollFactor(0)
    .setDepth(DEPTH + 1)
    .setVisible(false);

  const layout = (): void => {
    const { width, height } = scene.scale;
    const boxWidth = Math.min(width - 2 * MARGIN, MAX_WIDTH);
    text.setWordWrapWidth(boxWidth - 2 * PAD);
    text.setPosition(width / 2, height - MARGIN - PAD);
    panel.setPosition(width / 2, height - MARGIN);
    panel.setSize(boxWidth, text.height + 2 * PAD);
  };
  scene.scale.on('resize', layout);

  return {
    show: (line: string): void => {
      text.setText(line);
      layout();
      panel.setVisible(true);
      text.setVisible(true);
    },
    hide: (): void => {
      panel.setVisible(false);
      text.setVisible(false);
    },
    destroy: (): void => {
      scene.scale.off('resize', layout);
      panel.destroy();
      text.destroy();
    },
  };
}
