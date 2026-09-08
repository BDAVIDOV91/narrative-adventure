/**
 * The only place Three.js is used. It is imported dynamically so the ~600KB
 * chunk is never fetched until a 3D moment actually opens — the storybook shell
 * and all 2D gameplay run without it.
 *
 * Scope rule from the brief: single-object renders only. No 3D environments,
 * no scene graphs of many meshes. This machine is an integrated AMD APU.
 */

export interface PlanetRenderHandle {
  dispose: () => void;
}

export async function renderPlanet(
  canvas: HTMLCanvasElement,
  textureUrl: string,
): Promise<PlanetRenderHandle> {
  const THREE = await import('three');

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false });
  // Capped deliberately: devicePixelRatio 2+ on a weak APU costs 4x the fill
  // rate for a sphere the player looks at for a few seconds.
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    45,
    canvas.clientWidth / canvas.clientHeight,
    0.1,
    100,
  );
  camera.position.z = 3;

  const texture = await new THREE.TextureLoader().loadAsync(textureUrl);
  texture.colorSpace = THREE.SRGBColorSpace;

  const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(1, 48, 32),
    new THREE.MeshStandardMaterial({ map: texture }),
  );
  scene.add(sphere);
  scene.add(new THREE.AmbientLight(0xff_ff_ff, 0.35));
  const sun = new THREE.DirectionalLight(0xff_ff_ff, 2);
  sun.position.set(5, 2, 3);
  scene.add(sun);

  let frame = 0;
  const tick = (): void => {
    sphere.rotation.y += 0.002;
    renderer.render(scene, camera);
    frame = requestAnimationFrame(tick);
  };
  tick();

  return {
    dispose: (): void => {
      cancelAnimationFrame(frame);
      texture.dispose();
      sphere.geometry.dispose();
      (sphere.material as { dispose: () => void }).dispose();
      renderer.dispose();
    },
  };
}
