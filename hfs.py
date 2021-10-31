def s(bits):
    l = len(bits)
    for i, b in enumerate(bits):
        if 0 == b:
            bits[i] = 1
            break
        else:
            bits[i] = 0
            if i == len(bits) - 1:
                bits.append(1)
                break
    return bits


def n2ps(n):
    ps=[]
    p=0
    while(n):
        if n&1 : ps.append(p)
        n=n>>1
        p+=1
    return ps

def ps2n(ps):
    return sum(1<<p for p in ps)

def succ(ps):
    if ps==[] : return [0]
    l = len(ps)
    rs=[]
    i=0
    while i<l and i==ps[i]:
        i+=1
    rs.append(i)
    rs.extend(ps[i:])
    return rs


def n2hfs(n):
    if n==0 : return []
    return [n2hfs(p) for p in n2ps(n)]


def hfs2n(hfs):
  if hfs==[]: return 0
  return ps2n(hfs2n(x) for x in hfs)


bs = [1, 1, 1, 1, 1, 1, 1, 1]

print(bs)
print(s(bs))
print('')
a=[0,1,2,7,8,11,13]
print(a)
b=succ(a)
print(b)
print(succ(b))

print('-----')
a=[]
for _ in range(5):
    print(a)
    a=succ(a)

print(ps2n(n2ps(1234567)))
print(hfs2n(n2hfs(1234567)))
