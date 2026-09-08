import type { Scene } from 'phaser';

/**
 * The player: a Bulgarian kid of about 11-12 who finds the telescope.
 *
 * Placeholder — movement is wired, art is not. Kept deliberately small: the
 * top-down levels are a couple of minutes of walking, not a platformer.
 */

const WALK_SPEED = 160;

export interface PlayerHandle {
  readonly sprite: Phaser.GameObjects.Rectangle;
  update: () => void;
}

export function createPlayer(scene: Scene, x: number, y: number): PlayerHandle {
  // Stand-in rectangle until the character art exists.
  const sprite = scene.add.rectangle(x, y, 18, 26, 0xff_d2_6a);
  scene.physics.add.existing(sprite);
  const body = sprite.body as Phaser.Physics.Arcade.Body;
  body.setCollideWorldBounds(true);

  const keys = scene.input.keyboard?.createCursorKeys();

  return {
    sprite,
    update: (): void => {
      if (!keys) return;
      const vx = (keys.right.isDown ? 1 : 0) - (keys.left.isDown ? 1 : 0);
      const vy = (keys.down.isDown ? 1 : 0) - (keys.up.isDown ? 1 : 0);
      // Normalise so diagonal walking is not faster.
      const len = Math.hypot(vx, vy) || 1;
      body.setVelocity((vx / len) * WALK_SPEED, (vy / len) * WALK_SPEED);
    },
  };
}
