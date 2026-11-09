#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
function patchViewer(html,data){
 const originalMatch=html.match(/const GEO_ROWS=(\[[^\n]*?\]);/);
 if(!originalMatch)throw Error("GEO_ROWS missing");
 const original=JSON.parse(originalMatch[1]);
 if(original.length!==556||data.records.length!==556)throw Error("Unexpected count");
 for(let i=0;i<556;i++){const a=original[i],b=data.records[i];if(a[0]!==b.index||a[1]!==b.name||a[3]!==b.original.x||a[4]!==b.original.z||a[5]!==b.original.h||a[6]!==b.original.category||a[7]!==b.original.subtype)throw Error("Source data mismatch pin "+i);}
 if(html.includes("SPACIEL_V19_TAXONOMY_MARKER"))throw Error("Already patched");
 function one(a,b){const n=html.split(a).length-1;if(n!==1)throw Error("Expected 1 replacement, found "+n+": "+a.slice(0,100));html=html.replace(a,b);}
 const order=["work","leisure","food","living","shopping","municipal","civic"];
 const byFamily=Object.fromEntries(order.map(f=>[f,data.role_definitions.filter(r=>r.family===f)]));
 const name=order.map(f=>data.role_families.find(g=>g.id===f).name);
 const subName=order.map(f=>byFamily[f].map(r=>r.name));
 const lookup=Object.fromEntries(data.records.map(x=>{let j=byFamily[x.family].findIndex(r=>r.id===x.role_id);if(j<0)throw Error("Role missing "+x.role_id);return[x.index,[order.indexOf(x.family),j,x.artwork.exact_match?x.artwork.legacy_category:null,x.artwork.exact_match?x.artwork.legacy_subtype:null,x.review_needed?1:0,x.source_place_type,(x.secondary_family_ids||[]).map(f=>{const id=order.indexOf(f);if(id<0)throw Error('Secondary family missing '+f);return id;})]];}));
 const namesPatch="\n/* SPACIEL_V19_TAXONOMY_MARKER */\nCAT_NAMES.splice(0,7,..."+JSON.stringify(name)+");\nSUB_NAMES.splice(0,7,..."+JSON.stringify(subName)+");\nwindow.CAT_NAMES="+JSON.stringify([...name].reverse())+";\n";
 const cl='const CAT_COLORS=["#d54ae8", "#08a4f5", "#42d7ff", "#00d79d", "#ffeb26", "#ff8527", "#ff4237"];';
 one(cl,cl+namesPatch);
 const gp='const GEO_POINTS=GEO_ROWS.map(p=>({index:p[0],name:p[1],district:p[2],x:p[3],z:p[4],h:p[5],c:p[6],sub:p[7],source:p[8],id:p[9],added:p[10],basis:p[11]}));';
 one(gp,gp+"\nconst GEO_FAMILY_ART=[0,5,5,3,4,2,6];\nconst GEO_OLD_TO_NEW=[0,5,5,3,4,2,6];\nconst GEO_NEW_TAXONOMY="+JSON.stringify(lookup)+";\nfor(const p of GEO_POINTS){const a=GEO_NEW_TAXONOMY[p.index];if(!a)throw Error('Missing role for '+p.index);p.legacyCat=p.c;p.legacySub=p.sub;p.c=a[0];p.sub=a[1];p.iconCat=a[2];p.iconSub=a[3];p.needsTaxonomyReview=!!a[4];p.sourcePlaceType=a[5];p.secondaryFamilyCats=a[6]||[]}\n");
 one("img.src=PARENT_IMAGES[cat];img.alt=","img.src=PARENT_IMAGES[GEO_FAMILY_ART[cat]];img.alt=");
 one("p.childCats=[...new Set(p.shops.map(e=>e.cat).filter(c=>c!==null))];","p.childCats=[...new Set([...(p.secondaryFamilyCats||[]),...p.shops.map(e=>e.cat===null?null:GEO_OLD_TO_NEW[e.cat])].filter(c=>c!==null))];");
 one("CAT_NAMES[shop.cat].toLocaleLowerCase()","CAT_NAMES[GEO_OLD_TO_NEW[shop.cat]].toLocaleLowerCase()");
 one("glyph.style.background=CAT_COLORS[shop.cat]+\u002728\u0027;","glyph.style.background=CAT_COLORS[GEO_OLD_TO_NEW[shop.cat]]+\u002728\u0027;");
 one("(item.basis==='sourcebook_review_provisional'?' · REVIEW':'')","(item.needsTaxonomyReview?' · REVIEW':'')");
 one("const subMode=renderCat>=0&&item.c===renderCat&&item.sub!==null,bitmap=categoryHost?parentBitmaps[renderCat]:(isNeutral?null:(subMode?subBitmaps[item.c][item.sub]:parentBitmaps[item.c]));",
 "const bitmap=categoryHost?parentBitmaps[GEO_FAMILY_ART[renderCat]]:(item.iconCat===null?null:(item.iconSub!==null&&subBitmaps[item.iconCat]?.[item.iconSub]?subBitmaps[item.iconCat][item.iconSub]:parentBitmaps[item.iconCat]));");
 one("document.getElementById('geo-location-count').textContent=cat<0?'556 PINS · 90 VENUES':cat===4?(GEO_POINTS.filter(x=>x.c===4||(x.shops.length>0)).length+' COMMERCE SITES'):GEO_POINTS.filter(x=>x.c===cat).length+' LOCATIONS';",
 "document.getElementById('geo-location-count').textContent=cat<0?GEO_POINTS.length+' PINS · '+GEO_SHOP_ROWS.length+' LINKED VENUES':GEO_POINTS.filter(x=>visibleGeoCategory(x,cat)).length+' LOCATIONS';");
 one("Search 556 mapped places plus '+GEO_SHOP_ROWS.length+' Vend-R occupants, shops, bars and services.",
 "Search '+GEO_POINTS.length+' mapped places plus '+GEO_SHOP_ROWS.length+' Vend-R occupants, shops, bars and services.");
 const output=JSON.parse(html.match(/const GEO_ROWS=(\[[^\n]*?\]);/)[1]);if(JSON.stringify(output)!==JSON.stringify(original))throw Error("Original rows mutated");
 return html;
}
const source=process.argv[2],target=process.argv[3];
if(!source||!target){console.error('Usage: node tools/build-v19-taxonomy-viewer.mjs SOURCE.html OUTPUT.html');process.exit(2)}
const here=path.dirname(fileURLToPath(import.meta.url));
const data=JSON.parse(fs.readFileSync(path.resolve(here,'../data/locations/v19_location_icon_taxonomy_review.json'),'utf8'));
const html=fs.readFileSync(source,'utf8');
const output=patchViewer(html,data);
fs.writeFileSync(target,output,'utf8');
console.log(JSON.stringify({output:target,location_count:data.records.length,previously_grey:data.records.filter(p=>p.original.category===null).length,still_uncategorized:0,review_flags:data.records.filter(p=>p.review_needed).length}));
