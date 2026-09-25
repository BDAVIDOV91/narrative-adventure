import { Scene } from 'phaser';

import { t } from '@/shared/content';
import { FONT_STACK } from '@/shared/fonts';
import { createPlayer, type PlayerHandle } from '@/shared/player-character';

import { EARTH_SCENE, STORYBOOK_SCENE } from '../scene-keys';

import earthData from './earth-data.json';

/**
 * Earth — the tutorial level. Guided and linear: day/night via a shadow-matching
 * sundial, seasons via a tilting globe, then finding the telescope and spotting
 * Зорница at twilight.
 *
 * Skeleton: the map, the player and the puzzle markers load from earth-data.json.
 * The puzzle mini-games themselves are not built yet — a marker currently just
 * reports which puzzle type it would open.
 */

export class EarthScene extends Scene {
  private player: PlayerHandle | undefined;

  constructor() {
    super(EARTH_SCENE);
  }

  create(): void {
    const { width, height } = earthData.map;
    this.physics.world.setBounds(0, 0, width, height);
    this.cameras.main.setBounds(0, 0, width, height);
    this.cameras.main.setBackgroundColor('#16233f');

    this.player = createPlayer(this, earthData.map.spawn.x, earthData.map.spawn.y);
    this.cameras.main.startFollow(this.player.sprite);

    for (const marker of earthData.markers) {
      const dot = this.add
        .circle(marker.position.x, marker.position.y, 12, 0xff_e0_8a)
        .setInteractive({ useHandCursor: true });
      dot.on('pointerup', () => {
        // Placeholder until the puzzle mini-games exist.
        console.warn(`[earth] would open puzzle "${marker.puzzle}" (${marker.id})`);
      });
    }

    this.add
      .text(12, 12, t('ui.puzzle.close'), {
        fontFamily: FONT_STACK,
        fontSize: '16px',
        color: '#cfd6ff',
      })
      .setScrollFactor(0)
      .setInteractive({ useHandCursor: true })
      .on('pointerup', () => {
        this.scene.start(STORYBOOK_SCENE);
      });
  }

  override update(): void {
    this.player?.update();
  }
}
