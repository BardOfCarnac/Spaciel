/**
 * Spaciel Coastal Spectral Bridge v1 — WebGL2 host binding
 * Only supplies the two APPROVED V19 geographic textures and scalar controls.
 * Does not create waves, reflections, colours, geometry, or its own timebase.
 * Use with coastal_spectral_bridge_v1.glsl and the existing surface renderer.
 */
export class SpacielCoastalSpectralBridge {
  constructor(gl, {
    maskUrl, fetchUrl,
    maskUnit = 4, fetchUnit = 5,
    width = 1112, height = 1392,
  } = {}) {
    if (!(gl instanceof WebGL2RenderingContext)) {
      throw new TypeError('Coastal bridge requires a WebGL2RenderingContext');
    }
    if (!maskUrl || !fetchUrl) throw new Error('Supply the actual V19 mask and fetch PNG URLs');
    if (maskUnit === fetchUnit) throw new Error('Texture units must be distinct');
    this.gl = gl;
    this.width = width;
    this.height = height;
    this.maskUrl = maskUrl;
    this.fetchUrl = fetchUrl;
    this.maskUnit = maskUnit;
    this.fetchUnit = fetchUnit;
    this.mask = gl.createTexture();
    this.fetch = gl.createTexture();
    this.ready = false;
    this.error = null;
    this._uniforms = new WeakMap();
    this.configure({
      enabled: true, influence: 1.0, swell: 0.90, wind: 0.90, windFrom: 270
    });
    this._allocate(this.mask, this.maskUnit, gl.RGBA8, gl.RGBA);
    this._allocate(this.fetch, this.fetchUnit, gl.RGB8, gl.RGB);
  }

  configure({enabled, influence, swell, wind, windFrom} = {}) {
    const finite = (value, fallback) => Number.isFinite(value) ? value : fallback;
    const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
    if (enabled !== undefined) this.enabled = Boolean(enabled);
    if (influence !== undefined) this.influence = clamp(finite(influence, 1), 0, 1);
    if (swell !== undefined) this.swell = clamp(finite(swell, 0.9), 0, 1);
    if (wind !== undefined) this.wind = clamp(finite(wind, 0.9), 0, 1);
    // V1 has source-derived directional fetch ONLY for SW, W and NW.
    if (windFrom !== undefined) this.windFrom = clamp(finite(windFrom, 270), 225, 315);
  }

  _allocate(texture, unit, internal, format) {
    const gl = this.gl;
    gl.activeTexture(gl.TEXTURE0 + unit);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texImage2D(gl.TEXTURE_2D, 0, internal, 1, 1, 0, format, gl.UNSIGNED_BYTE,
      format === gl.RGBA ? new Uint8Array([0,0,0,0]) : new Uint8Array([0,0,0]));
  }

  async _image(url) {
    return await new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        if (img.naturalWidth !== this.width || img.naturalHeight !== this.height) {
          reject(new Error('Mask grid mismatch: expected ' + this.width + '×' + this.height));
        } else resolve(img);
      };
      img.onerror = () => reject(new Error('Could not load the V19 coastal PNG: ' + url));
      img.src = url;
    });
  }

  _upload(texture, unit, internal, format, img) {
    const gl = this.gl;
    gl.activeTexture(gl.TEXTURE0 + unit);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false);
    gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
    gl.pixelStorei(gl.UNPACK_COLORSPACE_CONVERSION_WEBGL, gl.NONE);
    gl.texImage2D(gl.TEXTURE_2D, 0, internal, format, gl.UNSIGNED_BYTE, img);
    const err = gl.getError();
    if (err !== gl.NO_ERROR) throw new Error('Coastal texture GL upload failed: '+err);
  }

  async load() {
    this.ready = false;
    this.error = null;
    try {
      const [mask, fetch] = await Promise.all([
        this._image(this.maskUrl), this._image(this.fetchUrl)
      ]);
      this._upload(this.mask, this.maskUnit, this.gl.RGBA8, this.gl.RGBA, mask);
      this._upload(this.fetch, this.fetchUnit, this.gl.RGB8, this.gl.RGB, fetch);
      this.ready = true;
      return this;
    } catch (e) {
      this.error = e;
      throw e;
    }
  }

  bind(program) {
    const gl = this.gl;
    gl.useProgram(program);
    let u = this._uniforms.get(program);
    if (!u) {
      u = {};
      for (const name of [
        'uCoastalMask','uCoastalFetch','uCoastReady','uCoastEnabled',
        'uCoastInfluence','uCoastSwell','uCoastWind','uWindFrom'
      ]) u[name] = gl.getUniformLocation(program, name);
      this._uniforms.set(program,u);
    }
    gl.activeTexture(gl.TEXTURE0 + this.maskUnit);
    gl.bindTexture(gl.TEXTURE_2D, this.mask);
    gl.activeTexture(gl.TEXTURE0 + this.fetchUnit);
    gl.bindTexture(gl.TEXTURE_2D, this.fetch);
    if (u.uCoastalMask !== null) gl.uniform1i(u.uCoastalMask, this.maskUnit);
    if (u.uCoastalFetch !== null) gl.uniform1i(u.uCoastalFetch, this.fetchUnit);
    if (u.uCoastReady !== null) gl.uniform1i(u.uCoastReady, this.ready ? 1 : 0);
    if (u.uCoastEnabled !== null) gl.uniform1i(u.uCoastEnabled, this.enabled ? 1 : 0);
    if (u.uCoastInfluence !== null) gl.uniform1f(u.uCoastInfluence, this.influence);
    if (u.uCoastSwell !== null) gl.uniform1f(u.uCoastSwell, this.swell);
    if (u.uCoastWind !== null) gl.uniform1f(u.uCoastWind, this.wind);
    if (u.uWindFrom !== null) gl.uniform1f(u.uWindFrom, this.windFrom);
  }

  dispose() {
    if (this.mask) this.gl.deleteTexture(this.mask);
    if (this.fetch) this.gl.deleteTexture(this.fetch);
    this.mask = this.fetch = null;
    this.ready = false;
  }
}

// Reference numeric model for assertions and offline comparisons.
// Pure JS equivalent of the V3.6 geography weight rule, NOT a wave generator.
export function referenceCoastalGains({
  exposure = 0, shelter = 0, fetch = 0, reservoir = false,
  enabled = true, influence = 1, swell = 0.9, wind = 0.9
} = {}) {
  const clamp = (x,a,b)=>Math.max(a,Math.min(b,x));
  const targetSwell = reservoir ? 0.12 :
    clamp(0.16+0.98*exposure*(1-0.37*shelter),0.13,1.15);
  const targetRipple = reservoir ? 0.24 :
    clamp(0.20+1.02*Math.sqrt(Math.max(fetch,0))*(1-0.25*shelter),0.16,1.16);
  const on = enabled ? clamp(influence,0,1) : 0;
  return {
    swell: 1+(targetSwell-1)*on*clamp(swell,0,1),
    ripple: 1+(targetRipple-1)*on*clamp(wind,0,1)
  };
}
