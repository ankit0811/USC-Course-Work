# -*- coding: utf-8 -*-
import os
from collections import defaultdict
import sys
import codecs
import math




def getFiles(cand, ref):
    refAll=[];
    candAll=[];

    if (os.path.isdir(ref)):
        for files in os.listdir(ref):
            print "files=>",files
            with codecs.open(ref+files,"r","UTF-8") as fp:
                refAll.append(fp.readlines());
                fp.close()

    else:
        with codecs.open(ref,"r","UTF-8") as fp:
            refAll.append(fp.readlines());
            fp.close();

    with codecs.open(cand,"r","UTF-8") as fp:
        for lines in fp:
            candAll.append(lines.strip());
        fp.close();

    return  candAll, refAll;



def generateNGrams(cand, ref, n):

    cnt = 0;

    candWordCounts=0;
    totalCandNGramCnt=0
    numerator=0
    for sentence_i in range(len(cand)):
        bestDiff=float('Inf');

        matchClippedCount=0;
        #print "\nFor candLine",cand[sentence_i]
        candNGramDict = defaultdict(int);
        candWordList=cand[sentence_i].split()
        currCandLength=len(candWordList)
        totalCandNGramCnt+=len(candWordList)-n+1;

        for j in range(len(candWordList)-n+1):
            candNGramDict[" ".join(candWordList[j:j+n])] += 1

        currRefLengthArr = []
        refNGramAllFilesDictArr=[]
        for refArr in ref:

            refWordList=refArr[sentence_i].strip().split()
            currRefLengthArr.append(len(refWordList))
            refNGramDict = defaultdict(int)


            for j in range(len(refWordList)-n+1):
                refNGramDict[" ".join(refWordList[j:j + n])] += 1
            refNGramAllFilesDictArr.append(refNGramDict)

        for canRefToken in candNGramDict:
            candNGramCnt=candNGramDict[canRefToken];
            candNGramMax=0;

            for refNGramDict in refNGramAllFilesDictArr:
                if canRefToken in refNGramDict:
                    #print canRefToken , refNGramDict
                    candNGramMax=max(candNGramMax, refNGramDict[canRefToken])
                    #print "For token ", canRefToken  , "matched max value so far ", matchClippedDict[canRefToken]
            candNGramCnt=min(candNGramCnt,candNGramMax)
            matchClippedCount+=candNGramCnt
        cnt+=matchClippedCount

        bestVal=0;
        for vals in currRefLengthArr:
            if bestDiff > abs(vals - currCandLength):
                bestDiff=abs(vals-currCandLength)
                bestVal=vals
        #print "For sentence", sentence_i, bestVal, numerator
        numerator+=bestVal;

        #print "candNGramDict",candNGramDict, matchClippedCount
        #print "matchClippedCount==>",matchClippedCount,cnt, totalCandNGramCnt
        candWordCounts+=currCandLength
    if (cnt==0):
        prec=0;
    else:
        prec=(1.0 * cnt) / totalCandNGramCnt

    if candWordCounts > numerator:
        brevPenalty = 1
    else:
        brevPenalty = math.exp(1.0 - (numerator * 1.0 / candWordCounts))

    return prec, brevPenalty





inCand=sys.argv[1]
inRef=sys.argv[2]
candidate, reference=getFiles(inCand, inRef);
#print len(candidate), len(reference)
gMean=1.0;

for i in range(4):

    #print i+1;
    precI, brevPenaltyI = generateNGrams(candidate, reference, i+1);
    print precI, brevPenaltyI
    gMean*=precI

gMean = math.pow(gMean, (1.0 / 4))
bleuScore = gMean * brevPenaltyI
print bleuScore

f_out =  open('bleu_out.txt','w')
f_out.write(str(bleuScore))
f_out.close()