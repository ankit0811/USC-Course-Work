from collections import defaultdict;
import math;
import sys;
import json;
import codecs

print sys.argv[1]

#Contains Token and their tags emission prob
inDict=dict();
#Contains Tags count
allTagsTransCountDict=defaultdict(int);
allTagsEmmCountDict=defaultdict(int);
transitionDict=dict();
cnt=0;
with codecs.open(sys.argv[1], 'r', "utf-8") as inFile:
    for line in inFile:
        lineList=line.strip().split(" ")

        prevTag="q0";

        for  lineListidx in range(len(lineList)):
            tokenswithTags=lineList[lineListidx]
            tokenTag=tokenswithTags.split('/')

            #For Handling words with "/" char
            token="".join(tokenTag[0:len(tokenTag)-1])
            tag=tokenTag[len(tokenTag)-1]
            if token !="":
                if lineListidx<len(lineList)-1:
                    allTagsTransCountDict[tag] += 1

                if prevTag=="q0":
                    allTagsTransCountDict[prevTag] += 1
                    allTagsEmmCountDict[prevTag] += 1
                allTagsEmmCountDict[tag] += 1

                #Creating a transition Dictionary q0->NN, q1->VB, VB->VB etc
                if prevTag not in transitionDict:
                    tagToTagDict=defaultdict(int)
                    tagToTagDict[tag] +=1;

                    transitionDict[prevTag]=tagToTagDict
                else:
                    transitionDict[prevTag][tag] += 1

                prevTag=tag


                #create token dictionary
                if token not in inDict:

                    tokenTagsDict=defaultdict(int)
                    tokenTagsDict[tag] += 1
                    inDict[token]=tokenTagsDict
                else:

                    inDict[token][tag] +=1
inFile.close()


#print allTagsTransCountDict
#print "\n",transitionDict,"\n"

#print transitionDict

for i in transitionDict:
    for j in allTagsTransCountDict:
        if j != "q0":
            if j not in transitionDict[i]:

                transitionDict[i][j]= math.log((1)/(1.0 * (allTagsTransCountDict[i]+len(allTagsTransCountDict)-1)),2)
            else:
                transitionDict[i][j]= math.log((transitionDict[i][j]+1)/(1.0 * (allTagsTransCountDict[i]+len(allTagsTransCountDict)-1)),2)

print len(allTagsTransCountDict)



#print "After"
#print "\n",transitionDict,"\n"





for i in inDict:
    for j in inDict[i]:
        inDict[i][j]= math.log((inDict[i][j] / (1.0 * allTagsEmmCountDict[j])),2)

jsonEmissions = json.dumps(inDict)
jsonTransitions = json.dumps(transitionDict)

print len(inDict)

f=codecs.open("hmmmodel.txt","w","utf-8")
f.write(jsonEmissions+"\n")
f.write(jsonTransitions )
f.close()
