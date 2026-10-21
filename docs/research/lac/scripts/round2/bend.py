import numpy as np
def resample(p, step=1.0):
    p=np.asarray(p,float); d=np.r_[0,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))]
    keep=np.r_[True,np.diff(d)>1e-9]; p,d=p[keep],d[keep]
    at=np.linspace(0,d[-1],max(3,int(np.ceil(d[-1]/step))+1)); return np.stack([np.interp(at,d,p[:,k]) for k in range(3)],1), at
def bends(p, window=3.0):
    """turn (deg) over each `window` mm, per mm: robust to the 1-mm zigzag of CAD centre lines"""
    q,s=resample(p,0.5); n=int(round(window/0.5/2))
    t=np.gradient(q,axis=0); t/=np.linalg.norm(t,axis=1)[:,None]
    out=np.zeros(len(q))
    for i in range(n,len(q)-n):
        out[i]=np.degrees(np.arccos(np.clip(t[i-n]@t[i+n],-1,1)))/window
    return s,q,out
def summary(p, window=3.0, thr=8.0):
    s,q,k=bends(p,window)
    segs=[]; on=False
    for i,v in enumerate(k):
        if v>thr and not on: on=True; a=i
        if v<=thr and on: on=False; j=a+int(np.argmax(k[a:i])); segs.append((round(s[a],1),round(s[i],1),round(float(k[j]),1),q[j].round(1).tolist()))
    tot=np.degrees(np.sum(np.arccos(np.clip((np.diff(q,axis=0)[1:]/np.linalg.norm(np.diff(q,axis=0)[1:],axis=1)[:,None]*np.diff(q,axis=0)[:-1]/np.linalg.norm(np.diff(q,axis=0)[:-1],axis=1)[:,None]).sum(1),-1,1))))
    return dict(length=round(s[-1],1), max=round(float(k.max()),1), total_turn=round(float(tot)), sharp=segs)
