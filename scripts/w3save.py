"""Read-only diagnosis and a narrow, audited Witcher 3 recovery profile.

Dependency: lz4 (for example, uv run --with lz4 python w3save.py ...).
Inputs are never modified; repair emits an experimental candidate only.
"""
from pathlib import Path
import argparse, bisect, hashlib, json, struct
import lz4.block


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def tokens(src, expected, prefix=b'', start=0, decode=False):
    """Independent raw LZ4 validator, also usable to decode a surviving suffix."""
    i=start; produced=len(prefix); output=bytearray(prefix) if decode else None
    while i<len(src):
        token=src[i];i+=1;lit=token>>4
        if lit==15:
            while True:
                require(i<len(src),'Missing literal length');x=src[i];i+=1;lit+=x
                if x<255:break
        require(i+lit<=len(src),'Literal exceeds compressed input')
        if decode:output.extend(src[i:i+lit])
        i+=lit;produced+=lit
        require(produced<=expected,'Literal exceeds declared output')
        if i==len(src):break
        require(i+2<=len(src),'Missing match offset')
        offset=struct.unpack_from('<H',src,i)[0]
        require(0<offset<=produced,f'Invalid backward reference at compressed offset {i}: distance {offset}, output {produced}')
        i+=2;match=(token&15)+4
        if token&15==15:
            while True:
                require(i<len(src),'Missing match length');x=src[i];i+=1;match+=x
                if x<255:break
        require(produced+match<=expected,'Match exceeds declared output')
        if decode:
            pattern=bytes(output[-offset:]);output.extend((pattern*((match+offset-1)//offset))[:match])
        produced+=match
    require(produced==expected,'Decoded length does not equal declared length')
    return bytes(output) if decode else {'consumed':i,'produced':produced}


def load(path):
    path=Path(path).resolve();data=path.read_bytes()
    require(data[:8]==b'SNFHFZLC','Unsupported container magic')
    n,offset=struct.unpack_from('<II',data,8)
    require(0<n<=20000 and 16+12*n<=len(data),'Invalid table extent')
    require(16<=offset<len(data),'Invalid data offset')
    headers=[struct.unpack_from('<III',data,16+12*i) for i in range(n)]
    total=sum(u for c,u,e in headers)
    require(0<total<=512*1024*1024,'Payload exceeds 512 MiB analysis limit')
    parts=[];rows=[];pos=offset
    for i,(c,u,end) in enumerate(headers):
        require(0<c and 0<u<=16*1024*1024 and pos+c<=len(data),'Invalid chunk bounds')
        row={'index':i,'compressed':c,'uncompressed':u,'start':pos,'declared_end':end,'computed_end':pos+c,'end_valid':end==pos+c or (i==n-1 and end==0)}
        try:
            block=data[pos:pos+c];decoded=lz4.block.decompress(block,uncompressed_size=u)
            require(len(decoded)==u,'Library output length mismatch');tokens(block,u)
            parts.append(decoded);row['decoded']=True
        except (ValueError,lz4.block.LZ4BlockError) as error:
            parts.append(None);row.update(decoded=False,error=str(error))
        rows.append(row);pos+=c
    report={'name':path.name,'sha256':digest(data),'file_bytes':len(data),'magic':'SNFHFZLC','chunk_count':n,'data_offset':offset,'table_end':16+12*n,'table_overlap_bytes':max(0,16+12*n-offset),'declared_payload_bytes':total,'decoded_chunks':sum(x is not None for x in parts),'computed_eof':pos,'trailing_bytes':len(data)-pos,'chunks':rows}
    return path,data,report,parts


def layout(data,base):
    require(data[-2:]==b'SE','Unsupported serialization footer')
    vt=struct.unpack_from('<I',data,len(data)-6)[0];p=vt-base
    require(10<=p<len(data)-6,'Variable table outside payload')
    count=struct.unpack_from('<I',data,p)[0]
    require(p+4+8*count==len(data)-6,'Variable table does not end at footer')
    nm,rb=struct.unpack_from('<II',data,p-10)
    require(0<=nm-base<len(data) and 0<=rb-base<len(data),'Section pointers out of bounds')
    require(data[nm-base:nm-base+6]==b'NMMANU','Missing names table')
    names_count=struct.unpack_from('<I',data,nm-base+6)[0]
    require(0<names_count<=65535,'Unsupported name count')
    pos=nm-base+14;names=[]
    for _ in range(names_count):
        require(pos<len(data),'Name table truncated');size=data[pos];pos+=1
        require(pos+size<=len(data),'Name truncated');names.append(bytes(data[pos:pos+size]).decode('utf-8',errors='replace'));pos+=size
    require(data[pos+4:pos+8]==b'ENOD','Name table terminator mismatch')
    entries=[struct.unpack_from('<II',data,p+4+8*i) for i in range(count)]
    for off,size in entries:require(base<=off<vt and off+size<=base+len(data),'Variable index outside payload')
    return {'vt':vt,'nm':nm,'rb':rb,'entries':entries,'names':names,'base':base}


def section(data,info,name):
    tag=b'BS'+struct.pack('<H',info['names'].index(name)+1);base=info['base']
    for off,size in info['entries']:
        if data[off-base:off-base+4]==tag:return off-base,size
    raise ValueError('Missing section '+name)


def read_string(data,pos):
    begin=pos;first=data[pos];pos+=1;length=first&63;ansi=bool(first&128)
    if first&64:
        shift=6
        while True:
            require(shift<=34 and pos<len(data),'Invalid packed length')
            x=data[pos];pos+=1;length|=(x&127)<<shift;shift+=7
            if not x&128:break
    size=length*(1 if ansi else 2);require(pos+size<=len(data),'String out of bounds')
    return {'start':begin,'value_start':pos,'byte_count':size,'ansi':ansi},pos+size


def parse_facts(data,start,size):
    require(data[start+4:start+6]==b'SS' and data[start+10:start+14]==b'SXAP' and data[start+26:start+30]==b'SBDF','Unsupported facts schema')
    count=struct.unpack_from('<I',data,start+30)[0]
    require(count<=1000000,'Implausible fact count');pos=start+34;rows=[]
    for i in range(count):
        row,pos=read_string(data,pos);exp,entries=struct.unpack_from('<HH',data,pos);pos+=4
        row.update(index=i,expiring=exp,entries=entries,records_start=pos);pos+=entries*10
        require(pos<=start+size,'Fact records out of bounds');row['records_end']=pos;rows.append(row)
    require(pos+4==start+size and data[pos:pos+4]==b'EBDF','Facts terminator does not match indexed boundary')
    return rows


def packed_string(value):
    n=len(value);first=128|(n&63);n>>=6;out=bytearray([first|(64 if n else 0)])
    while n:
        x=n&127;n>>=7;out.append(x|(128 if n else 0))
    return bytes(out)+value


def healthy(path):
    p,b,r,parts=load(path)
    require(r['table_overlap_bytes']==0 and all(parts) and all(x['end_valid'] for x in r['chunks']) and r['trailing_bytes']==0,'Donor or baseline is not structurally readable')
    return p,b,r,b''.join(parts)


def analyze(args):
    p,b,r,parts=load(args.source)
    # Placeholder bytes maintain offsets; unavailable bytes are never claimed recovered.
    payload=b''.join(x if x is not None else bytes(row['uncompressed']) for x,row in zip(parts,r['chunks']))
    r['decoded_header_magic']=payload[:4].decode('ascii',errors='replace') if parts[0] else None
    try:
        info=layout(payload,r['data_offset']);r['variable_index_entries']=len(info['entries']);r['name_entries']=len(info['names'])
        if all(parts):
            start,size=section(payload,info,'facts');rows=parse_facts(payload,start,size)
            r['facts_count']=len(rows);r['large_fact_identifiers']=[{'index':x['index'],'byte_count':x['byte_count'],'ansi':x['ansi']} for x in rows if x['byte_count']>10000]
    except ValueError as error:r['serialization_error']=str(error)
    require(digest(p.read_bytes())==r['sha256'],'Input changed during analysis')
    out=Path(args.output).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    return r


def repair(args):
    src,source,r,parts=load(args.source);dp,donor,dr,dd=healthy(args.donor);bp,baseline,br,bd=healthy(args.baseline)
    base=r['data_offset'];require((r['chunk_count'],base,r['table_overlap_bytes'])==(266,3084,124),'Unsupported recovery profile')
    require(parts[0] is None and all(x is not None for x in parts[1:]) and r['trailing_bytes']==0,'Profile requires only block zero to fail and exact EOF')
    require(all(x['end_valid'] for x in r['chunks'][:-1]),'Unexpected intermediate end offset corruption')
    require(dd[:16]==bd[:16] and struct.unpack_from('<II',dd,4)==(66,29),'Donor/baseline save version mismatch')
    require(dd[100:116]==bd[100:116] and dd[93:100]==bd[93:100],'Donor/baseline playthrough mismatch')
    c=r['chunks'][0];first=tokens(source[c['start']:c['computed_end']],c['uncompressed'],dd[:128],128,True)
    payload=bytearray(first+b''.join(parts[1:]));require(len(payload)==r['declared_payload_bytes'],'Reconstructed length mismatch')
    info=layout(payload,base);names=info['names'];idx=lambda n:names.index(n)+1
    signatures=[b'VL'+struct.pack('<HH',idx('time'),idx('Uint64')),b'VL'+struct.pack('<HH',idx('type'),idx('Uint8')),b'VL'+struct.pack('<HH',idx('v'),idx('Uint16'))]
    history=0;pos=126
    while payload[pos:pos+6]==signatures[0] and payload[pos+14:pos+20]==signatures[1] and payload[pos+21:pos+27]==signatures[2]:history+=1;pos+=29
    require(0<history<=65535,'Unsupported save history boundary')
    require(source[base+124:base+126]==struct.pack('<H',history),'Surviving count bytes do not match history records')
    struct.pack_into('<I',payload,122,history)
    fs,fsize=section(payload,info,'facts');rows=parse_facts(payload,fs,fsize)
    bi=layout(bd,br['data_offset']);bfs,bsize=section(bd,bi,'facts');baseline_rows=parse_facts(bd,bfs,bsize)
    known={bytes(bd[x['value_start']:x['value_start']+x['byte_count']]) for x in baseline_rows if x['byte_count']>10000}
    edits=[(78,79,packed_string(b'RECOVERY TEST'))];changes=[]
    require(payload[72:79]==b'VL'+struct.pack('<HH',idx('description'),idx('String'))+b'\x80','Unsupported description field')
    for row in rows:
        if row['byte_count']<=10000:continue
        require(row['ansi'],'Non-ANSI oversized identifier needs separate analysis')
        begin=row['value_start'];end=begin+row['byte_count'];value=bytes(payload[begin:end])
        for _ in range(args.inverse_steps):value=value.decode('utf-8').encode('latin1')
        require(0<len(value)<row['byte_count'],'Encoding inverse did not shrink identifier')
        edits.append((row['start'],end,packed_string(value)))
        changes.append({'fact_index':row['index'],'old_bytes':row['byte_count'],'new_bytes':len(value),'inverse_steps':args.inverse_steps,'baseline_byte_match':value in known})
    require(changes and any(x['baseline_byte_match'] for x in changes),'No exact baseline identifier match')
    edits.sort();pieces=[];pos=0;ends=[];deltas=[];delta=0
    for start,end,new in edits:
        require(pos<=start<end,'Overlapping edits');pieces.extend([payload[pos:start],new]);pos=end
        delta+=len(new)-(end-start);ends.append(end);deltas.append(delta)
    pieces.append(payload[pos:]);fixed=bytearray(b''.join(pieces))
    def rel(pos):
        i=bisect.bisect_right(ends,pos)
        require(i==len(edits) or not(edits[i][0]<pos<edits[i][1]),'Pointer inside an edited string')
        return pos+(deltas[i-1] if i else 0)
    absolute=lambda off:base+rel(off-base)
    vt,nm,rb=info['vt'],info['nm'],info['rb'];sscount=0
    for i,(off,size) in enumerate(info['entries']):
        newoff=absolute(off);newsize=rel(off-base+size)-rel(off-base)
        struct.pack_into('<II',fixed,rel(vt-base)+4+8*i,newoff,newsize)
        if payload[off-base:off-base+2]==b'SS':
            require(struct.unpack_from('<I',payload,off-base+2)[0]+6==size,'Original indexed SS length mismatch')
            struct.pack_into('<I',fixed,rel(off-base)+2,newsize-6);sscount+=1
    struct.pack_into('<II',fixed,rel(vt-base-10),absolute(nm),absolute(rb));struct.pack_into('<I',fixed,len(fixed)-6,absolute(vt))
    require(payload[rb-base:rb-base+2]==b'RB','Missing RB table');rcount=struct.unpack_from('<I',payload,rb-base+2)[0]
    for i in range(rcount):
        size,off=struct.unpack_from('<HI',payload,rb-base+6+6*i);struct.pack_into('<HI',fixed,rel(rb-base)+6+6*i,size,absolute(off))
    fi=layout(fixed,base);newfs,newsize=section(fixed,fi,'facts');newrows=parse_facts(fixed,newfs,newsize)
    require(len(rows)==len(newrows),'Fact count changed')
    for old,new in zip(rows,newrows):
        require((old['expiring'],old['entries'])==(new['expiring'],new['entries']),'Fact counters changed')
        require(payload[old['records_start']:old['records_end']]==fixed[new['records_start']:new['records_end']],'Fact values or timestamps changed')
        if old['byte_count']<=10000:require(payload[old['value_start']:old['value_start']+old['byte_count']]==fixed[new['value_start']:new['value_start']+new['byte_count']],'Unselected identifier changed')
    preserved=[]
    for name in ['questSystem','community','CJournalManager','universe','idTagManager']:
        start,size=section(payload,info,name);newstart,newsize=section(fixed,fi,name)
        require(size==newsize and payload[start:start+size]==fixed[newstart:newstart+newsize],name+' changed');preserved.append(name)
    for off,size in fi['entries']:
        if fixed[off-base:off-base+2]==b'SS':require(struct.unpack_from('<I',fixed,off-base+2)[0]+6==size,'Repaired SS length mismatch')
    raw=[bytes(fixed[i:i+1048576]) for i in range(0,len(fixed),1048576)]
    blocks=[lz4.block.compress(x,store_size=False) for x in raw]
    require(16+12*len(raw)<=base,'Repair still exceeds table capacity')
    header=bytearray(base);header[:8]=b'SNFHFZLC';struct.pack_into('<II',header,8,len(raw),base);pos=base
    for i,(u,c) in enumerate(zip(raw,blocks)):
        pos+=len(c);struct.pack_into('<III',header,16+12*i,len(c),len(u),0 if i==len(raw)-1 else pos)
        require(lz4.block.decompress(c,uncompressed_size=len(u))==u,'Round trip mismatch');tokens(c,len(u))
    output=bytes(header)+b''.join(blocks)
    directory=Path(args.output_dir).resolve()
    require(all(directory!=p.parent and p.parent not in directory.parents for p in [src,dp,bp]),'Output must be outside input save folders')
    fields=src.stem.split('_');require(len(fields)==4 and fields[0]=='ManualSave','Specify a supported manual-save input')
    fields[-1]=format(int(fields[-1],16)+1,'x');stem='_'.join(fields)
    sidecars={ext:src.with_suffix('.'+ext).read_bytes() for ext in ['json','png'] if src.with_suffix('.'+ext).exists()}
    for ext in ['sav',*sidecars]:require(not(directory/(stem+'.'+ext)).exists(),'Candidate already exists')
    require(not(directory/'repair-manifest.json').exists(),'Manifest already exists')
    for p,b in [(src,source),(dp,donor),(bp,baseline)]:require(digest(p.read_bytes())==digest(b),'Input changed during repair')
    manifest={'profile':'pc66-chunks266-overlap124','status':'Experimental candidate; game load and later saves unverified','source':src.name,'source_sha256':digest(source),'donor':dp.name,'donor_sha256':digest(donor),'baseline':bp.name,'baseline_sha256':digest(baseline),'lost_prefix_bytes':128,'header_values_from_donor':['magic_number','runtimeGUIDCounter'],'donor_runtimeGUIDCounter':struct.unpack_from('<Q',dd,85)[0],'history_count':history,'fact_count':len(rows),'identifier_changes':changes,'preserved_sections':preserved,'indexed_SS_verified':sscount,'variable_entries_verified':len(fi['entries']),'source_bytes':len(source),'candidate_bytes':len(output),'candidate_payload_bytes':len(fixed),'candidate_sha256':digest(output),'chunks':len(raw),'round_trip_and_independent_tokens_verified':True,'inputs_unchanged':True}
    directory.mkdir(parents=True,exist_ok=True)
    with (directory/(stem+'.sav')).open('xb') as f:f.write(output)
    for ext,b in sidecars.items():
        with (directory/(stem+'.'+ext)).open('xb') as f:f.write(b)
    with (directory/'repair-manifest.json').open('x',encoding='utf-8') as f:json.dump(manifest,f,indent=2)
    return manifest


def main():
    parser=argparse.ArgumentParser(description=__doc__);subs=parser.add_subparsers(dest='command',required=True)
    a=subs.add_parser('analyze');a.add_argument('--source',required=True);a.add_argument('--output',required=True)
    r=subs.add_parser('repair');r.add_argument('--source',required=True);r.add_argument('--donor',required=True);r.add_argument('--baseline',required=True);r.add_argument('--inverse-steps',type=int,choices=range(1,21),required=True);r.add_argument('--output-dir',required=True)
    args=parser.parse_args()
    try:
        result=analyze(args) if args.command=='analyze' else repair(args)
        print(json.dumps({k:v for k,v in result.items() if k not in ('chunks','identifier_changes')},indent=2))
    except (ValueError,OSError,UnicodeError,struct.error,lz4.block.LZ4BlockError) as error:
        parser.exit(2,f'No verified candidate produced: {error}\n')


if __name__=='__main__':main()
