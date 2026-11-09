#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Script} from 'node:vm';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const d=JSON.parse(fs.readFileSync(path.join(root,'data/locations/v19_location_icon_taxonomy_review.json'),'utf8'));
assert.equal(d.records.length,556);assert.equal(d.role_definitions.length,35);assert.equal(d.role_families.length,7);
const roles=new Map(d.role_definitions.map(r=>[r.id,r])),families=new Set(d.role_families.map(f=>f.id)),counts=Object.fromEntries([...families].map(f=>[f,0]));
for(let i=0;i<d.records.length;i++){const r=d.records[i];assert.equal(r.index,i);assert.ok(r.name&&r.original);for(const c of ['x','z','h'])assert.ok(Number.isFinite(r.original[c]),'geometry '+i);assert.ok(families.has(r.family));assert.equal(roles.get(r.role_id)?.family,r.family);for(const f of r.secondary_family_ids||[]){assert.ok(families.has(f));assert.notEqual(f,r.family);}counts[r.family]++;}
assert.deepEqual(counts,d.counts);
for(const [n,role] of [['The Crater','leisure:culture'],['Zhirafa Office Park','work:offices'],['Bristol Business Park','work:offices'],['Main Gate','municipal:security'],['Hunger Street','food:restaurants'],['Obsidian Equinox Marina & Docks','municipal:freight'],['Graceland Medical','civic:medical']])assert.equal(d.records.find(r=>r.name===n)?.role_id,role);
for(const n of ['Graceland Medical','Bristol Business Park','Obsidian Equinox Marina & Docks','Stop. Shop. Stitch.','Snack & Shack'])assert.ok(d.records.find(r=>r.name===n)?.secondary_family_ids?.length);
const node=fs.readFileSync(path.join(root,'tools/build-v19-taxonomy-viewer.mjs'),'utf8');
const ins=fs.readFileSync(path.join(root,'review/Spaciel_V19_Icon_Taxonomy_Installer.html'),'utf8');
const payload=ins.match(/<script id="spaciel-payload" type="application\/json">([\s\S]*?)<\/script>/);assert.ok(payload);assert.deepEqual(JSON.parse(payload[1]),d);
const getfn=s=>{let i=s.indexOf('function patchViewer(html,data){');assert.ok(i>=0);let j=s.indexOf('return html;\n}',i);assert.ok(j>i);return s.slice(i,j+'return html;\n}'.length)};
assert.equal(getfn(node),getfn(ins));
new Script(node.replace(/^#!.*\n/,'').replace(/^import .*\n/g,''),{filename:'taxonomy-converter'});
const scripts=[...ins.matchAll(/<script(?![^>]*type=)[^>]*>([\s\S]*?)<\/script>/g)];assert.ok(scripts.length);for(const m of scripts)new Script(m[1]);
assert.equal(d.records.filter(x=>x.review_needed).length,178);
console.log(JSON.stringify({locations:556,roles:35,families:7,corrections:d.sourcebook_corrections.length,secondary_sites:d.records.filter(x=>x.secondary_family_ids?.length).length,review_flags:178,counts},null,2));
