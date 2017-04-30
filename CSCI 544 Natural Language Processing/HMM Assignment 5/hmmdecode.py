import json;
import sys;
import codecs;
reload(sys)
sys.setdefaultencoding("utf-8")

def printDict(d,fopen):
    for key,val in d.iteritems():
        fopen.write(key+" : "+ str(val)+"\n")


def callDecode(inLine, emmission, transition, foutput):

    with open("temptest.txt","w") as fopen:

        probArray=[]
        backPtrArray=[]
        for i in range(len(inLine)):
            backPtrArray.append({})
            probArray.append({})


        for wordIdx in range(len(inLine)):
            print "-------------------",inLine[wordIdx],"-------------------"

            if wordIdx==0: #First token

                if inLine[wordIdx] not in emmission: #If not in emmision, then same as transition of q0
                    probArray[wordIdx]=transition["q0"]

                    for key,val in transition["q0"].iteritems():
                        backPtrArray[wordIdx][key] = key

                else: #Present in emmision

                    transEmission=dict();
                    max=float('-inf')

                    for tags, wordValue in emmission[inLine[wordIdx]].iteritems():

                        transEmission[tags]=wordValue+transition["q0"][tags];
                        backPtrArray[wordIdx][tags] = tags

                        if max<=transEmission[tags]:
                            max=transEmission[tags];
                    probArray[wordIdx]=transEmission;

            else:

                if inLine[wordIdx] not in emmission:
                    #print "probArray[wordIdx-1]=",probArray[wordIdx-1]
                    #print "Not in emission, transition="
                    #for tags in transition:
                    #    print tags

                    for tags in transition:
                        max = float('-inf')
                        if tags !="q0":
                            for prevStatetag,value in probArray[wordIdx-1].iteritems():


                                newProb=value+transition[prevStatetag][tags]
                                print "prevStatetag=",prevStatetag, "   value=",value, "    currtag",tags, "    transition[prev][curr]",transition[prevStatetag][tags], "    newProb",newProb
                                if max<=newProb:
                                    max=newProb
                                    backPtrArray[wordIdx][tags]=prevStatetag
                                    probArray[wordIdx][tags]=newProb

                    #            print prevStatetag,value , tags, wordIdx, probArray[wordIdx][tags], backPtrArray[wordIdx][tags]

                else:

#
#                    print "probArray[wordIdx-1]",probArray[wordIdx-1]
                    for tags,wordValue in emmission[inLine[wordIdx]].iteritems():
                        max = float('-inf')
                        if tags != "q0":
                            for prevStatetag,value in probArray[wordIdx-1].iteritems():
                                newProb=value+transition[prevStatetag][tags]+wordValue


                                print "prevStatetag=", prevStatetag, "   value=", value, "    currtag", tags, "    transition[prev][curr]",transition[prevStatetag][tags], "    newProb", newProb

                                if max<=newProb:
                                    max=newProb
                                    backPtrArray[wordIdx][tags]=prevStatetag
                                    probArray[wordIdx][tags]=newProb


            fopen.write("\nFor word:"+inLine[wordIdx]+"\n")
            if inLine[wordIdx] in emmission:
                fopen.write("Emmission: true")
                printDict(emmission[inLine[wordIdx]], fopen)
            else:
                fopen.write("Emmission: false")

            fopen.write("Back Ptr Array :")
            printDict(backPtrArray[wordIdx], fopen)
            fopen.write("Prob Array:")
            printDict(probArray[wordIdx],fopen)



    fopen.close()
    taggedOut=[]
    for i in range(len(inLine)):
        taggedOut.append([])

    prevKey=""
    for i in reversed(range(len(inLine))):

        if i==len(inLine)-1:
            max=float('-inf')
            for key,value in probArray[i].iteritems():
                if max<value:
                    max=value
                    maxKey=key

            prevKey=maxKey
            if i!=0:
                maxKey=backPtrArray[i][maxKey]
        else:

            prevKey = maxKey
            maxKey=backPtrArray[i][maxKey]

        taggedOut[i]=str(inLine[i])+str("/")+str(prevKey)
#    print taggedOut
    for i in taggedOut:
        foutput.write(i+" ")
    foutput.write("\n")


#HmmDecode
cnt=0
with codecs.open("hmmmodel.txt", "r","utf-8") as fopen:
    cnt=0
    for line in fopen:
        if cnt==0:
            inDict=json.loads(line)
        if cnt ==1:
            transitionDict=json.loads(line)
        cnt+=1;


fopen.close()


'''for key, value in inDict.iteritems():
    if "Acc" in key and "s" in key:
        print key, value'''


with codecs.open("hmmoutput.txt","w","utf-8") as foutput:
    cntr = 0;
    with open(sys.argv[1],'r') as fopen:
        for line in fopen:
            cntr+=1
            if cntr == 13:
                lineList = line.decode("utf-8").strip().split(" ")
                callDecode(lineList, inDict, transitionDict, foutput)
                break

    fopen.close()

foutput.close()
