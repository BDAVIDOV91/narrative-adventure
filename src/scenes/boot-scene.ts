import { Scene } from 'phaser';

import { t } from '@/shared/content';
import { FONT_STACK } from '@/shared/fonts';

import { STORYBOOK_SCENE } from './scene-keys';

export const BOOT_SCENE = 'boot';

export class BootScene extends Scene {
  constructor() {
    super(BOOT_SCENE);
  }

  preload(): void {
    const { width, height } = this.scale;
    this.add
      .text(width / 2, height / 2, t('ui.loading'), {
        fontFamily: FONT_STACK,
        fontSize: '20px',
        color: '#cfd6ff',
      })
      .setOrigin(0.5);
  }

  create(): void {
    this.scene.start(STORYBOOK_SCENE);
  }
}
