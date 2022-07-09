def make_slug(name):
    name=name.replace(' ','_')
    k=[]
    for i in name.lower():
        k.append(i)
    return ''.join(k)