import os

root='.'
found=[]
for dirpath, dirnames, filenames in os.walk(root):
    for fn in filenames:
        if fn.endswith('.py'):
            path=os.path.join(dirpath, fn)
            try:
                with open(path,'rb') as f:
                    data=f.read()
                if b'\x00' in data:
                    found.append(path)
            except Exception as e:
                print('ERROR', path, e)
if not found:
    print('NO_NULL_BYTES_FOUND')
else:
    for p in found:
        print(p)
