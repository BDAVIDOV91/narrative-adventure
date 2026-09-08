import { AUTO, Game, Scale } from 'phaser';

import { BootScene } from '@/scenes/boot-scene';
import { EarthScene } from '@/scenes/earth/earth-scene';
import { StorybookScene } from '@/scenes/storybook-scene';

new Game({
  type: AUTO,
  parent: 'game',
  backgroundColor: '#0b1026',
  scale: {
    mode: Scale.RESIZE,
    autoCenter: Scale.CENTER_BOTH,
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { x: 0, y: 0 } },
  },
  // AUTO falls back to Canvas when WebGL is unavailable — real insurance on
  // Linux + AMD integrated graphics, where Mesa WebGL can be unreliable.
  scene: [BootScene, StorybookScene, EarthScene],
});
