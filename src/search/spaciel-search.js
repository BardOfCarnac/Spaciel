/* Spaciel standard unified geographic search (V19)
 * Standalone browser script or Node module. No private viewer assets.
 */
(function(root, factory) {
  'use strict';
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.SpacielSearch = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function() {
  'use strict';
  const KINDS = Object.freeze({district:'DISTRICT', locality:'NEIGHBOURHOOD', street:'STREET', pin:'PLACE', venue:'VENUE'});
  const PRIORITY = Object.freeze({district:0, locality:1, street:2, pin:3, venue:4});
  const normalize = value => String(value == null ? '' : value).normalize('NFKD')
    .replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase().trim();

  function createIndex({geography={}, locations=[], venues=[]}={}) {
    const records=[], byId=new Map();
    function add(kind,name,subtitle,payload,extra='') {
      if (!name) return;
      records.push({kind,name:String(name),subtitle:String(subtitle||''),payload,
        searchName:normalize(name),searchExtra:normalize(extra),typePriority:PRIORITY[kind]});
    }
    for (const a of geography.districts||[])
      add('district',a[0],'Official 2045 district',a);
    for (const a of geography.localities||[])
      add('locality',a[0],String(a[3])+' · mapped neighbourhood',a);
    for (const s of geography.streets||[])
      add('street',s.name,(s.provisional?'Provisional name · ':'')+'Named street'+(s.review?' · alignment to review':''),s);
    for (const p of locations) {
      add('pin',p.name,(p.district||'Night City')+' · location pin',p,(p.district||'')+' '+(p.source||''));
      if (p.id != null) byId.set(String(p.id),p);
      for (const shop of p.shops||[]) {
        if (shop.ownPin) continue;
        add('venue',shop.name,'Inside '+p.name+' · '+(p.district||'Night City'),
          {p,shop},(p.district||'')+' '+(shop.kind||''));
      }
    }
    for (const shop of venues) {
      if (shop.ownPin) continue;
      const p=shop.p||byId.get(String(shop.parentId||shop.parent_id||''));
      if (!p||(p.shops||[]).some(s=>s.id!=null&&s.id===shop.id)) continue;
      add('venue',shop.name,'Inside '+p.name+' · '+(p.district||'Night City'),
        {p,shop},(p.district||'')+' '+(shop.kind||''));
    }
    return {
      version:geography.version||'unified-geographic-v1',records,
      counts:{districts:(geography.districts||[]).length,
        neighbourhoods:(geography.localities||[]).length,
        streets:(geography.streets||[]).length,
        locations:locations.length,venues:records.filter(r=>r.kind==='venue').length}
    };
  }

  function search(index,text,{limit=50,minLength=2}={}) {
    const q=normalize(text);if(q.length<minLength)return [];
    const hits=[];
    for(const row of index.records) {
      const n=row.searchName, inName=n.includes(q);
      const inContext=(row.kind==='pin'||row.kind==='venue')&&row.searchExtra.includes(q);
      if(!inName&&!inContext)continue;
      const rank=n===q?0:n.startsWith(q)?1:inName?2:3;
      hits.push({kind:row.kind,name:row.name,subtitle:row.subtitle,
        payload:row.payload,rank,typePriority:row.typePriority});
    }
    hits.sort((a,b)=>a.rank-b.rank||a.typePriority-b.typePriority||a.name.localeCompare(b.name));
    return hits.slice(0,Math.max(0,limit));
  }

  /* Coordinates remain in their original registered frames. The map viewer
   * must perform prototypeToWorld / road-to-atlas conversion itself. */
  function destination(hit) {
    if (!hit) return null;
    if(hit.kind==='district'){
      const [name,x,y,w,h]=hit.payload;
      return {kind:'district',name,frame:'district-prototype-900x1390',bounds:[x,y,x+w,y+h]};
    }
    if(hit.kind==='locality'){
      const [name,x,y,parentDistrict]=hit.payload;
      return {kind:'locality',name,parentDistrict,frame:'district-prototype-900x1390',point:[x,y]};
    }
    if(hit.kind==='street'){
      const s=hit.payload;
      return {kind:'street',name:s.name,frame:'v17-local-roads',
        point:[s.x,s.y],lines:s.lines,provisional:!!s.provisional,review:!!s.review};
    }
    const p=hit.kind==='venue'?hit.payload.p:hit.payload;
    return {kind:hit.kind,name:hit.name,frame:'viewer-world',
      point:[p.x,p.z==null?p.y:p.z],locationId:p.id,
      shopId:hit.kind==='venue'?hit.payload.shop.id:null};
  }

  /* Mount uses the reviewed V19 HTML IDs and gives the host a result
   * and its renderer-neutral destination. The host owns actual navigation,
   * pin-to-bubble morphing, category visibility and street highlighting. */
  function mount({index,trigger,panel,input,results,onSelect}={}) {
    if(!index||!trigger||!panel||!input||!results||typeof onSelect!=='function')
      throw new Error('SpacielSearch.mount needs index, trigger, panel, input, results and onSelect');
    let rendered=[];
    function close(){panel.classList.remove('open');trigger.setAttribute('aria-expanded','false');}
    function render(){
      const q=input.value.trim();results.replaceChildren();rendered=search(index,q);
      if(normalize(q).length<2){
        const c=index.counts,el=document.createElement('div');el.className='search-summary';
        el.textContent='Search '+c.locations+' location pins, linked venues, '+
          c.districts+' districts, '+c.neighbourhoods+' mapped neighbourhoods and '+
          c.streets+' named streets.';
        results.append(el);return;
      }
      if(!rendered.length){
        const el=document.createElement('div');el.className='search-summary';
        el.textContent='No matching places, districts or streets';results.append(el);return;
      }
      for(const hit of rendered){
        const btn=document.createElement('button');btn.type='button';
        const tag=document.createElement('span');tag.className='search-kind '+hit.kind;
        tag.textContent=KINDS[hit.kind];
        const sub=document.createElement('span');sub.className='search-sub';
        sub.textContent=hit.subtitle;
        btn.append(tag,document.createTextNode(hit.name),sub);
        btn.addEventListener('click',()=>{close();onSelect(hit,destination(hit));});
        results.append(btn);
      }
    }
    function toggle(){
      const open=!panel.classList.contains('open');
      panel.classList.toggle('open',open);trigger.setAttribute('aria-expanded',String(open));
      if(open){render();input.focus();}
    }
    function keydown(e){
      if(e.key==='Escape'){close();trigger.focus();}
      if(e.key==='Enter'&&rendered.length){e.preventDefault();close();onSelect(rendered[0],destination(rendered[0]));}
    }
    trigger.addEventListener('click',toggle);
    input.addEventListener('input',render);
    input.addEventListener('keydown',keydown);
    trigger.setAttribute('aria-expanded','false');
    return {render,close,destroy(){
      trigger.removeEventListener('click',toggle);
      input.removeEventListener('input',render);
      input.removeEventListener('keydown',keydown);
    }};
  }
  return Object.freeze({KINDS,normalize,createIndex,search,destination,mount});
});
