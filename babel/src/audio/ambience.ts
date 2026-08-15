/**
 * The sound of the Library, synthesized: distant air in the shafts, the
 * tick of footsteps on stone, the flutter of opened pages. No samples —
 * nothing here was recorded in our universe.
 */

export class Ambience {
  private ctx: AudioContext | null = null;
  private master: GainNode | null = null;
  private muted = false;

  /** Call from a user gesture. Safe to call twice. */
  start(): void {
    if (this.ctx) return;
    try {
      const ctx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
      this.ctx = ctx;
      this.master = ctx.createGain();
      this.master.gain.value = 0.55;
      this.master.connect(ctx.destination);

      // Room tone: filtered brown noise, barely there.
      const len = ctx.sampleRate * 4;
      const buf = ctx.createBuffer(1, len, ctx.sampleRate);
      const data = buf.getChannelData(0);
      let last = 0;
      for (let i = 0; i < len; i++) {
        const white = Math.random() * 2 - 1;
        last = (last + 0.02 * white) / 1.02;
        data[i] = last * 3.2;
      }
      const src = ctx.createBufferSource();
      src.buffer = buf;
      src.loop = true;
      const lp = ctx.createBiquadFilter();
      lp.type = "lowpass";
      lp.frequency.value = 240;
      const g = ctx.createGain();
      g.gain.value = 0.05;
      src.connect(lp).connect(g).connect(this.master);
      src.start();

      // A slow breath in the gain, like air moving in a deep shaft.
      const lfo = ctx.createOscillator();
      lfo.frequency.value = 0.05;
      const lfoGain = ctx.createGain();
      lfoGain.gain.value = 0.018;
      lfo.connect(lfoGain).connect(g.gain);
      lfo.start();
    } catch {
      this.ctx = null; // headless or blocked: the Library falls silent
    }
  }

  toggleMute(): boolean {
    this.muted = !this.muted;
    if (this.master) this.master.gain.value = this.muted ? 0 : 0.55;
    return this.muted;
  }

  isMuted(): boolean {
    return this.muted;
  }

  private burst(freq: number, q: number, dur: number, gain: number, type: BiquadFilterType = "bandpass"): void {
    if (!this.ctx || !this.master || this.muted) return;
    const ctx = this.ctx;
    const len = Math.ceil(ctx.sampleRate * dur);
    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < len; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, 2.2);
    }
    const src = ctx.createBufferSource();
    src.buffer = buf;
    const f = ctx.createBiquadFilter();
    f.type = type;
    f.frequency.value = freq;
    f.Q.value = q;
    const g = ctx.createGain();
    g.gain.value = gain;
    src.connect(f).connect(g).connect(this.master);
    src.start();
  }

  footstep(): void {
    this.burst(620 + Math.random() * 240, 1.1, 0.09, 0.16);
  }

  bookSlide(): void {
    this.burst(1700, 0.7, 0.16, 0.1, "highpass");
  }

  pageFlutter(): void {
    this.burst(2600, 0.5, 0.07, 0.06, "highpass");
  }

  thud(): void {
    this.burst(140, 1.4, 0.18, 0.3, "lowpass");
  }

  /** The travel: a long airy sweep, then a low arrival. */
  whoosh(): void {
    if (!this.ctx || !this.master || this.muted) return;
    const ctx = this.ctx;
    const dur = 1.6;
    const len = Math.ceil(ctx.sampleRate * dur);
    const buf = ctx.createBuffer(1, len, ctx.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) {
      const t = i / len;
      d[i] = (Math.random() * 2 - 1) * Math.sin(Math.PI * t) ** 1.5;
    }
    const src = ctx.createBufferSource();
    src.buffer = buf;
    const f = ctx.createBiquadFilter();
    f.type = "bandpass";
    f.Q.value = 2.2;
    f.frequency.setValueAtTime(220, ctx.currentTime);
    f.frequency.exponentialRampToValueAtTime(2400, ctx.currentTime + dur * 0.7);
    f.frequency.exponentialRampToValueAtTime(160, ctx.currentTime + dur);
    const g = ctx.createGain();
    g.gain.value = 0.34;
    src.connect(f).connect(g).connect(this.master);
    src.start();
    // Arrival bell, very soft.
    const osc = ctx.createOscillator();
    osc.frequency.value = 196;
    const og = ctx.createGain();
    og.gain.setValueAtTime(0.0001, ctx.currentTime + dur * 0.8);
    og.gain.exponentialRampToValueAtTime(0.12, ctx.currentTime + dur * 0.85);
    og.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + dur + 1.4);
    osc.connect(og).connect(this.master);
    osc.start(ctx.currentTime + dur * 0.8);
    osc.stop(ctx.currentTime + dur + 1.5);
  }

  wind(on: boolean): void {
    // The endless fall: reuse the room tone by raising master briefly.
    if (!this.ctx || !this.master) return;
    this.master.gain.cancelScheduledValues(this.ctx.currentTime);
    this.master.gain.linearRampToValueAtTime(on ? 1.1 : this.muted ? 0 : 0.55, this.ctx.currentTime + 0.8);
  }
}
