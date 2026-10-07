import { Geom, Scene } from 'phaser';

import { createCompanionBox, type CompanionBox } from '@/shared/companion-box';
import { arrivalKey, type CompanionTiers } from '@/shared/companion-tiers';
import { isContentKey, t } from '@/shared/content';
import { FONT_STACK } from '@/shared/fonts';
import { createPlayer, type PlayerHandle } from '@/shared/player-character';
import { commitSolve } from '@/shared/progress-write';
import { openPuzzleOverlay, type PuzzleOverlay } from '@/shared/puzzle-overlay';

import { EARTH_SCENE, STORYBOOK_SCENE } from '../scene-keys';

import earthData from './earth-data.json';

/**
 * Earth — the tutorial level. Guided and linear: day/night via a shadow-matching
 * sundial, seasons via a tilting globe, then finding the telescope and spotting
 * Зорница at twilight.
 *
 * The map, the player and the puzzle markers load from earth-data.json. A marker
 * opens the shared puzzle overlay; the engines that fill it arrive from E3, so
 * every marker shows "coming soon" for now.
 */

type EarthMarker = (typeof earthData.markers)[number];

/** A level-data key, checked at runtime too: validate-levels.py proves it at build time. */
function say(key: string): string {
  return isContentKey(key) ? t(key) : key;
}

export class EarthScene extends Scene {
  private player: PlayerHandle | undefined;
  private companion: CompanionBox | undefined;
  private overlay: PuzzleOverlay | undefined;

  constructor() {
    super(EARTH_SCENE);
  }

  private openMarker(marker: EarthMarker): void {
    if (this.overlay?.isOpen() === true) return;
    this.player?.setEnabled(false);

    const arrival = arrivalKey(earthData.companionTiers as CompanionTiers, marker.id);
    if (arrival === undefined) this.companion?.hide();
    else this.companion?.show(t(arrival));

    this.overlay = openPuzzleOverlay(
      this,
      {
        title: say(marker.label),
        body: t('ui.puzzle.coming-soon'),
        closeLabel: t('ui.puzzle.close'),
      },
      {
        onSolved: () => {
          // Bug 4: the progress write. Fires once the engines (E3+) report a solve.
          commitSolve(earthData.id, marker.id, earthData.markers, earthData.unlockThreshold);
          this.companion?.show(`${t('ui.puzzle.solved')} ${say(marker.reward.fact)}`);
        },
        onClosed: () => {
          this.companion?.hide();
          this.player?.setEnabled(true);
        },
      },
    );
  }

  create(): void {
    const { width, height } = earthData.map;
    this.physics.world.setBounds(0, 0, width, height);
    this.cameras.main.setBounds(0, 0, width, height);
    this.cameras.main.setBackgroundColor('#16233f');

    this.player = createPlayer(this, earthData.map.spawn.x, earthData.map.spawn.y);
    this.cameras.main.startFollow(this.player.sprite);
    this.companion = createCompanionBox(this);
    this.overlay = undefined;
    this.events.once('shutdown', () => {
      this.companion?.destroy();
    });

    for (const marker of earthData.markers) {
      this.add
        .circle(marker.position.x, marker.position.y, 12, 0xff_e0_8a)
        // The dot stays 24 px; the tap target is 44 px across (standards-frontend.md). Local coordinates.
        .setInteractive({
          hitArea: new Geom.Circle(12, 12, 22),
          hitAreaCallback: (area: Geom.Circle, x: number, y: number): boolean =>
            Geom.Circle.Contains(area, x, y),
          useHandCursor: true,
        })
        .on('pointerup', () => {
          this.openMarker(marker);
        });
    }

    this.add
      .text(0, 0, t('ui.puzzle.close'), {
        fontFamily: FONT_STACK,
        fontSize: '16px',
        color: '#cfd6ff',
        // Padding grows the tap target past 44 x 44 without changing the look.
        padding: { left: 12, right: 12, top: 14, bottom: 14 },
      })
      .setScrollFactor(0)
      .setInteractive({ useHandCursor: true })
      .on('pointerup', () => {
        if (this.overlay?.isOpen() === true) return;
        this.scene.start(STORYBOOK_SCENE, { returnFrom: earthData.id });
      });
  }

  override update(): void {
    this.player?.update();
  }
}
