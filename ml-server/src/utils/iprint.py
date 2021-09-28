import sys
def iprint(*args,**kwargs):
    print(*args,**kwargs,file=sys.stderr)