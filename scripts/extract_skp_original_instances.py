#!/usr/bin/env python3
"""Read actual placed-component IDs/transforms from a SketchUp 2024 ZIP model.dat.

This is a narrowly scoped reader for the original Night City 2045 SKP structure.
It writes placement metadata only, not licensed model faces/meshes.
The binary section names and tags are reverse-engineered for this exact source model;
validate the counts and source hash before using a different SKP model.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,struct,zipfile
from pathlib import Path

EXPECTED_HASH='17317588df75a4bea8a87ad86d0438ff112c693f6c54e4ca9da4fa4c53842ee0'

def chunks(data,begin,end):
    p=begin
    while p+6<=end:
        tag,n=struct.unpack_from('<HI',data,p)
        if n>end-p-6:raise ValueError(f'Invalid TLV size at byte {p}')
        yield tag,p+6,n
        p+=6+n
    if p!=end:raise ValueError(f'TLV segment has {end-p} trailing bytes')

def first_child(data,a,b,tag):
    for t,s,n in chunks(data,a,a+b):
        if t==tag:return s,n
    return None

def nested_id(data,st,ln):
    x=first_child(data,st,ln,0x5dc)
    if x:
        p=first_child(data,*x,0x5de)
        if p:return int.from_bytes(data[p[0]:p[0]+p[1]],'little')
    return None

def source_instances(path):
    h=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if h!=EXPECTED_HASH:raise ValueError('Unexpected source SKP SHA256; do not apply hard-coded layout offsets')
    with zipfile.ZipFile(path) as z:d=z.read('model.dat')
    roots={t:(p,n) for t,p,n in chunks(d,6,len(d))}
    # Top-level SketchUp entities (tag 0x1f6) -> entities container (0x1388)
    p,n=roots[0x1f6];root=first_child(d,p,n,0x1388)
    subs={t:(q,l) for t,q,l in chunks(d,root[0],root[0]+root[1])}
    p,n=subs[0x138d] # top-level component instances only
    for tag,st,ln in chunks(d,p,p+n):
        if tag!=0x1d4c:continue
        body=first_child(d,st,ln,0x1964)
        if not body:continue
        fields={t:(q,l) for t,q,l in chunks(d,body[0],body[0]+body[1])}
        if not (0x7d0 in fields and 0x1966 in fields and 0x1967 in fields):continue
        uid=nested_id(d,*fields[0x7d0]);q,l=fields[0x1967]
        native_id=int.from_bytes(d[q:q+l],'little')
        q,l=fields[0x1966]
        if l!=104:continue
        v=struct.unpack_from('<13d',d,q)
        yield {'instance_id':uid,'source_native_id':native_id,
            'm00':v[0],'m01':v[1],'m02':v[2],
            'm10':v[3],'m11':v[4],'m12':v[5],
            'm20':v[6],'m21':v[7],'m22':v[8],
            'world_x_inches':v[9],'world_y_inches':v[10],'world_z_inches':v[11],
            'matrix_bottom_right':v[12]}

def extract(path,output):
    rows=list(source_instances(path));Path(output).parent.mkdir(parents=True,exist_ok=True)
    if not rows:raise ValueError('Found no top-level placed instances')
    with open(output,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    return {'instances':len(rows),'unique_instance_ids':len({r['instance_id'] for r in rows}),
            'unique_definition_ids':len({r['source_native_id'] for r in rows}),
            'source_sha256':EXPECTED_HASH}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--skp',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    print(json.dumps(extract(a.skp,a.output),indent=2))
