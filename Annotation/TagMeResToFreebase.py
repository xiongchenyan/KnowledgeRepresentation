'''
Created on Mar 11, 2015 3:36:33 PM
@author: cx

what I do:
I match the annotated AOL log to Freebase
what's my input:
text tagged with # as indicator
what's my output:
tagged, but wiki name replaced by Freebase ID

'''


import site
# from CandidateGeneration import FbCandidateGenerator
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
from FreebaseDump.FbObjWikiMatch import FbObjWikiMatchC
from cxBase.Conf import cxConfC
import sys

MinRho = 0

def ProcessOneLine(line,WikiFbMatcher):
    if not '#' in line:
        return ""
    global MinRho
    vMid = line.split('#')
    if len(vMid) != 2:
        return ""
    QStr,AnaStr = vMid
    QStr = QStr.strip('\t')
    AnaStr =AnaStr.strip('\t')
    vCol = AnaStr.split('\t')
    if len(vCol) < 6:
        return line
    if 0 != (len(vCol) % 6):
        return line
    
    for i in range(len(vCol) / 6):
        if (vCol[i * 6 + 1] == 'www') | (vCol[i*6 + 1] == 'com'):
            continue
        if float(vCol[i*6 + 4]) < MinRho:
            continue
        WikiTitle = vCol[i * 6 + 5].lower()
        WikiUrl = 'http://en.wikipedia.org/wiki/%s' %(WikiTitle.replace(' ','_'))
        lObjId = WikiFbMatcher.MatchWikiToObj(WikiUrl)
        if [] == lObjId:
            print '[%s] not matched to fb' %(WikiTitle)
            continue
        vCol[i*6 + 5] = lObjId[0]
        
    return QStr + '\t#\t' + '\t'.join(vCol)


if 2 != len(sys.argv):
    FbObjWikiMatchC.ShowConf()
    print "in\nout"
    sys.exit()

WikiFbMatcher = FbObjWikiMatchC(sys.argv[1])
conf = cxConfC(sys.argv[1])    
InName = conf.GetConf('in')
OutName = conf.GetConf('out')

out = open(OutName,'w')

cnt = 0
AnaCnt = 0
ErrCnt = 0
for line in open(InName):
    line = line.strip()
    Res = ProcessOneLine(line, WikiFbMatcher)
    if Res == "":
        ErrCnt += 1
        continue
    print >> out, Res
    cnt += 1
    if Res != line:
        AnaCnt += 1
    if 0 == (cnt % 1000):
        print "annotated [%d/%d] line [%d] err" %(AnaCnt,cnt,ErrCnt)
    
    
out.close()

print "finished"


