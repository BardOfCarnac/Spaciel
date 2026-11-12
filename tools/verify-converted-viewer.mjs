#!/usr/bin/env node
import fs from 'node:fs';
import assert from 'node:assert/strict';
import vm from 'node:vm';
const path=process.argv[2];if(!path)throw Error('Usage: node tools/verify-converted-viewer.mjs PATH.html');
const html=fs.readFileSync(path,'utf8');
assert.ok(html.includes('SPACIEL_V19_TAXONOMY_MARKER'),'taxonomy patch missing');
const scripts=[...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)];
let checked=0;for(let i=0;i<scripts.length;i++){
 const [,attrs,js]=scripts[i];
 if(/type\s*=\s*["']application\/json["']/i.test(attrs))continue;
 if(!js.trim())continue;
 try{new vm.Script(js,{filename:'converted-viewer-script-'+i+'.js'})}
 catch(e){console.error('Failed to parse generated viewer script '+i+'\n'+e.stack);process.exit(1);}
 checked++;
}
assert.ok(checked>=1,'No executable scripts found');
console.log('Converted viewer compiled:',checked,'scripts; HTML bytes:',Buffer.byteLength(html));
