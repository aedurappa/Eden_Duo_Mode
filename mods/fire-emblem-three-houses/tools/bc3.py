import numpy as np, struct
def bc3_alpha(data,w,h):
    bw,bh=w//4,h//4
    blk=np.frombuffer(data,dtype=np.uint8).reshape(bh,bw,16)
    a0=blk[...,0].astype(np.int32); a1=blk[...,1].astype(np.int32)
    bits=np.zeros((bh,bw),dtype=np.uint64)
    for k in range(6): bits|=blk[...,2+k].astype(np.uint64)<<np.uint64(8*k)
    pal=np.zeros((bh,bw,8),dtype=np.int32)
    pal[...,0]=a0; pal[...,1]=a1
    gt=a0>a1
    for i in range(1,7):
        pal[...,1+i]=np.where(gt,((7-i)*a0+i*a1)//7,0)
    for i in range(1,5):
        v=((5-i)*a0+i*a1)//5
        pal[...,1+i]=np.where(gt,pal[...,1+i],v)
    pal[...,6]=np.where(gt,pal[...,6],0)
    pal[...,7]=np.where(gt,pal[...,7],255)
    out=np.zeros((h,w),dtype=np.uint8)
    for py in range(4):
        for px in range(4):
            idx=((bits>>np.uint64(3*(py*4+px)))&np.uint64(7)).astype(np.int64)
            v=np.take_along_axis(pal,idx[...,None],axis=2)[...,0]
            out[py::4,px::4]=v
    return out
