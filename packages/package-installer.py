#!/usr/bin/env python3
from subprocess import run
def paruin(L):
    s=''
    for i in L:
        s+=i+' '
    run('paru -S --noconfirm --needed '+s,shell=True)

with open('packages.txt') as f:
    packages=f.readlines()

for i in range(len(packages)):
    packages[i]=packages[i].strip()

for i in range(0,len(packages),2):
    s=packages[i:i+2]
    paruin(s)
