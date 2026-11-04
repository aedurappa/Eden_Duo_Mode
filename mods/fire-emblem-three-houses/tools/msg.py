import struct
R='H:/EdenDuo/output/unpacked/010055D009F78000/romfs/patch4/common/common/msgdata.bin'
B=open(R,'rb').read()
def ptbl(buf,base=0):
    n=struct.unpack_from('<I',buf,base)[0]
    return [struct.unpack_from('<II',buf,base+4+8*i) for i in range(n)]
def xl(buf,off,size):
    assert buf[off:off+2]==b'XL',buf[off:off+4]
    count=struct.unpack_from('<H',buf,off+8)[0]
    hdr=struct.unpack_from('<I',buf,off+0xC)[0]
    offs=struct.unpack_from('<%dI'%count,buf,off+hdr)
    out=[]
    for o in offs:
        p=off+hdr+o; e=buf.index(b'\0',p); out.append(buf[p:e].decode('utf-8','replace'))
    return out
def lang(l):
    lo,ls=ptbl(B)[l]
    parts=ptbl(B[lo:lo+ls])
    sub=B[lo:lo+ls]
    return [xl(sub,po,ps) for po,ps in parts]
