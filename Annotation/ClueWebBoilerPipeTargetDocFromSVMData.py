'''
Created on Mar 14, 2015 3:40:52 PM
@author: cx

what I do:
I get the boiler piped raw texts for doc ids in SVMData
what's my input:
CW boilerpipe in + svm (LeToR used)
what's my output:
doc's boilerpipe in SVM data

'''

import sys


def LoadTargetDocNo(SVMInName):
    hDocNo = {}
    for line in open(SVMInName):
        vCol = line.strip().split('#')
        if len(vCol) < 2:
            continue
        DocNo = vCol[-1].strip().strip('\t')
        hDocNo[DocNo] = 1
    return hDocNo


def Process(DocIn,SVMInName,OutName):
    hDocNo = LoadTargetDocNo(SVMInName)
    out = open(OutName,'w')
    
    cnt = 0
    for line in open(DocIn):
        line = line.strip()
        DocNo = line.split()[0]
        if DocNo in hDocNo:
            print >> out, line
        cnt += 1
        if 0 == (cnt % 10000):
            print "processed [%d] line" %(cnt)
    out.close()
    
    print "done"
    
    
if 4 != len(sys.argv):
    print "ClueWeb Boidlerpipe in + svm data with target docs + out"
    sys.exit()
    
Process(sys.argv[1],sys.argv[2],sys.argv[3])
    
    
        