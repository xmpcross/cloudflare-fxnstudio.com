/* Reference: https://v0-optimus-delta.vercel.app/
 * Extracted visual settings; standalone canvas implementation for the static site.
 * 0.15-radian sampling, 12px glyphs, radius 52.5%, rotation factors .5/.3/.2.
 * Reference advances .02 per frame; elapsed time preserves its 60Hz speed.
 */
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('hero-globe');
  if (!canvas) return;
  const context = canvas.getContext('2d');
  if (!context) return;
  const container = canvas.closest('.hero-animation');
  const button = document.querySelector('[data-globe-toggle]');
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const glyphs = '░▒▓█▀▄▌▐│─┤├┴┬╭╮╰╯';
  const samples = [];
  for (let longitude = 0; longitude < Math.PI * 2; longitude += .15) {
    for (let latitude = 0; latitude < Math.PI; latitude += .15) {
      samples.push({longitude, sinLatitude:Math.sin(latitude), cosLatitude:Math.cos(latitude)});
    }
  }
  let width = 0, height = 0, angle = 0, frame = 0, previousTime = null;
  let visible = true, userPaused = false;
  const shouldAnimate = () => !preference.matches && !document.hidden && visible && !userPaused;
  const draw = () => {
    context.clearRect(0, 0, width, height);
    context.font = '12px monospace';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    const radius = Math.min(width, height) * .525;
    const yRotation = angle * .3, xRotation = angle * .2;
    const cy = Math.cos(yRotation), sy = Math.sin(yRotation);
    const cx = Math.cos(xRotation), sx = Math.sin(xRotation);
    const points = samples.map(point => {
      const longitude = point.longitude + angle * .5;
      const x = point.sinLatitude * Math.cos(longitude);
      const y = point.sinLatitude * Math.sin(longitude);
      const z = point.cosLatitude;
      const rotatedX = x * cy - z * sy;
      const rotatedZ = x * sy + z * cy;
      const rotatedY = y * cx - rotatedZ * sx;
      const depth = y * sx + rotatedZ * cx;
      return {x:width / 2 + rotatedX * radius, y:height / 2 + rotatedY * radius, depth};
    }).sort((a, b) => a.depth - b.depth);
    for (const point of points) {
      const index = Math.max(0, Math.min(glyphs.length - 1, Math.floor((point.depth + 1) / 2 * (glyphs.length - 1))));
      context.fillStyle = `rgba(33,25,49,${.2 + (point.depth + 1) * .4})`;
      context.fillText(glyphs[index], point.x, point.y);
    }
  };
  const tick = now => {
    frame = 0;
    if (!shouldAnimate()) return;
    if (previousTime !== null) angle += Math.min(now - previousTime, 50) * .0012;
    previousTime = now;
    draw();
    frame = requestAnimationFrame(tick);
  };
  const sync = () => {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    previousTime = null;
    const running = shouldAnimate();
    canvas.dataset.motion = running ? 'running' : 'paused';
    button.hidden = preference.matches;
    button.textContent = userPaused ? 'Resume animation' : 'Pause animation';
    button.setAttribute('aria-label', userPaused ? 'Resume globe animation' : 'Pause globe animation');
    if (running) frame = requestAnimationFrame(tick);
  };
  const resize = () => {
    const bounds = canvas.getBoundingClientRect();
    width = bounds.width; height = bounds.height;
    if (!width || !height) return;
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    draw();
    container.classList.add('is-ready');
  };
  button.addEventListener('click', () => {userPaused = !userPaused; sync();});
  preference.addEventListener('change', () => {draw(); sync();});
  document.addEventListener('visibilitychange', sync);
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(entries => {visible = entries[0].isIntersecting; sync();}).observe(canvas);
  resize();
  sync();
});
