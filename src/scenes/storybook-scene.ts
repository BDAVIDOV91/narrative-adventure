import { Scene } from 'phaser';

import { t, type ContentKey } from '@/shared/content';
import { FONT_STACK } from '@/shared/fonts';
import { loadProgress } from '@/shared/game-state';

import { EARTH_SCENE, STORYBOOK_SCENE } from './scene-keys';

/**
 * The book IS the level select. Each page is a painted scene; tapping one zooms
 * in until the player is inside that world.
 *
 * Skeleton: pages are coloured rectangles with Bulgarian titles. Art comes later.
 */

interface PageDef {
  readonly levelId: string;
  readonly nameKey: ContentKey;
  readonly blurbKey: ContentKey;
  readonly sceneKey: string | null;
}

const PAGES: readonly PageDef[] = [
  {
    levelId: 'earth',
    nameKey: 'level.earth.name',
    blurbKey: 'level.earth.blurb',
    sceneKey: EARTH_SCENE,
  },
  {
    levelId: 'moon',
    nameKey: 'level.moon.name',
    blurbKey: 'level.moon.blurb',
    sceneKey: null,
  },
  {
    levelId: 'mars',
    nameKey: 'level.mars.name',
    blurbKey: 'level.mars.blurb',
    sceneKey: null,
  },
];

export class StorybookScene extends Scene {
  constructor() {
    super(STORYBOOK_SCENE);
  }

  create(): void {
    const { width, height } = this.scale;
    const progress = loadProgress();

    this.cameras.main.setBackgroundColor('#0b1026');

    this.add
      .text(width / 2, 56, t('app.title'), {
        fontFamily: FONT_STACK,
        fontSize: '38px',
        color: '#f4e6c3',
      })
      .setOrigin(0.5);

    this.add
      .text(width / 2, 98, t('ui.book.hint'), {
        fontFamily: FONT_STACK,
        fontSize: '16px',
        color: '#8f9ad0',
      })
      .setOrigin(0.5);

    const pageWidth = 200;
    const gap = 24;
    const totalWidth = PAGES.length * pageWidth + (PAGES.length - 1) * gap;
    const startX = (width - totalWidth) / 2 + pageWidth / 2;

    for (const [index, page] of PAGES.entries()) {
      const x = startX + index * (pageWidth + gap);
      const y = height / 2;
      const unlocked =
        index === 0 || (progress.levels[PAGES[index - 1]?.levelId ?? '']?.completed ?? false);

      const card = this.add
        .rectangle(x, y, pageWidth, 260, unlocked ? 0x1c2a5e : 0x141a33)
        .setStrokeStyle(2, unlocked ? 0xf4e6c3 : 0x2a3050);

      this.add
        .text(x, y - 90, t(page.nameKey), {
          fontFamily: FONT_STACK,
          fontSize: '24px',
          color: unlocked ? '#f4e6c3' : '#4d5678',
        })
        .setOrigin(0.5);

      this.add
        .text(x, y + 10, unlocked ? t(page.blurbKey) : t('ui.book.locked'), {
          fontFamily: FONT_STACK,
          fontSize: '14px',
          color: unlocked ? '#b9c2ea' : '#4d5678',
          align: 'center',
          // Bulgarian runs longer than English — text wraps, never clips.
          wordWrap: { width: pageWidth - 28 },
        })
        .setOrigin(0.5);

      if (unlocked && page.sceneKey !== null) {
        const sceneKey = page.sceneKey;
        card.setInteractive({ useHandCursor: true });
        card.on('pointerup', () => {
          this.scene.start(sceneKey);
        });
      }
    }
  }
}
