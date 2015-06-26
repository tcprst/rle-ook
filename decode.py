#! /usr/bin/env python
import getopt
import sys
import re

try:
    options, args = getopt.getopt(sys.argv[1:], 'hal:v', ["help","analyze","len=","verbose"])
except getopt.GetoptError as err:
    print str(err)
    #usage()
    sys.exit(2)

#default options
len=450
analyze=False
verbose=False

for opt, arg in options:
    if opt in ("-h","--help"):
        #usage()
        sys.exit(2)
    elif opt in ("-a","--analyze"):
        analyze=True
    elif opt in ("-v","--verbose"):
        verbose=True
    elif opt in ("-l","--length"):
        len = int(arg)
    else:
        assert False, "Unhandled option"
try:
    filename=args[0]
except:
    print "Must provide an input file"
    #usage()  -- Add print usage
    sys.exit(2)

f=open(filename)
bits=f.read()

current=bits[0]
ctr=0
out=[]

for x in bits:
    if x==current:
        ctr=ctr+1
    else:
        out.append([current,ctr])
        current=x
        ctr=0

def group(string,n):
    string=re.sub('(.{%d})'%n,'\\1 ',string)
    return string.split()

def decode(string):
    out=""
    if verbose:
        print "s:",group(string,4)
    for bit in group(string,4):
#          print "b: ",bit
        if bit=="1110":
            out=out+"1"
        elif bit=="1000":
            out=out+"0"
        else:
            out=out+"."+bit+"."
    return out

bout=[]
for (c,time) in out:
    l=(time+len/2)/len
    if analyze:
        print "%c %4d %2d"%(c,time,l)
    if(l>5):
        print "Bits:",decode("".join(bout))
        bout=[]
    else:
        bout.append(c*l)
