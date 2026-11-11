/* Spaciel native architecture tile data loader. Code only; no model payloads.
 * Use only with private or licensed assets served by the caller.
 * Atlas frame: top-left origin, 5175 × 7966 working pixels.
 */
export class NativeArchitectureTileStore {
  constructor(baseUrl, { maxCachedTiles = 24 } = {}) {
    this.base = new URL(baseUrl.endsWith('/') ? baseUrl : baseUrl + '/', import.meta.url);
    this.maxCachedTiles = maxCachedTiles;
    this.manifest = null;
    this.templates = null;
    this.cache = new Map();
    this.inflight = new Map();
  }
  async _getJson(relativeUrl, compressed = false) {
    const res = await fetch(new URL(relativeUrl, this.base));
    if (!res.ok) throw new Error('Architecture fetch failed: ' + res.status);
    if (!compressed) return res.json();
    if (!('DecompressionStream' in globalThis)) {
      throw new Error('Browser does not support gzip DecompressionStream');
    }
    const stream = res.body.pipeThrough(new DecompressionStream('gzip'));
    return JSON.parse(await new Response(stream).text());
  }
  async init() {
    const m = await this._getJson('manifest.json');
    if (m.schema !== 'spaciel-native-architecture-tiled-v1') {
      throw new Error('Incompatible Spaciel native architecture schema');
    }
    this.manifest = m;
    return m;
  }
  async loadTemplates() {
    if (!this.manifest) await this.init();
    if (!this.templates) {
      const obj = await this._getJson(this.manifest.model_index, true);
      if (obj.schema !== 'spaciel-native-skp-source-definitions-v1') {
        throw new Error('Incompatible source mesh template schema');
      }
      this.templates = obj.templates;
    }
    return this.templates;
  }
  async loadTile(key) {
    if (!this.manifest) await this.init();
    const record = this.manifest.tiles[key];
    if (!record) return null;
    if (this.cache.has(key)) {
      const item = this.cache.get(key);
      this.cache.delete(key);
      this.cache.set(key, item);
      return item;
    }
    if (this.inflight.has(key)) return this.inflight.get(key);
    const task = this._getJson(record.file, true).then(tile => {
      if (tile.schema !== 'spaciel-native-architecture-tile-v1' ||
          tile.instances.length !== record.count) {
        throw new Error('Invalid native architecture tile: ' + key);
      }
      this.cache.set(key, tile);
      while (this.cache.size > this.maxCachedTiles) {
        this.cache.delete(this.cache.keys().next().value);
      }
      return tile;
    }).finally(() => this.inflight.delete(key));
    this.inflight.set(key, task);
    return task;
  }
  async forBounds(bounds, { marginTiles = 1 } = {}) {
    if (!this.manifest) await this.init();
    // bounds = [xmin, ymin, xmax, ymax] in registered atlas coordinates
    const t = this.manifest.tile_size_atlas_pixels;
    const x0 = Math.floor(bounds[0] / t) - marginTiles;
    const y0 = Math.floor(bounds[1] / t) - marginTiles;
    const x1 = Math.floor(bounds[2] / t) + marginTiles;
    const y1 = Math.floor(bounds[3] / t) + marginTiles;
    const keys = [];
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) {
      const key = x + '_' + y;
      if (this.manifest.tiles[key]) keys.push(key);
    }
    return Promise.all(keys.map(key => this.loadTile(key)));
  }
  clearTiles() { this.cache.clear(); }
}
