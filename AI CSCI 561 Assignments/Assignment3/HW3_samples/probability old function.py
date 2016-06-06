def computeProbability():
    global bayesNet,BaysNetArray,arr,BaysDecisionArr

    for i in range(len(arr)):
        arr[i]=arr[i].replace('-','False').replace('+','True')
        #print arr[i]
        if arr[i].__contains__('|'): #Conditional Probability given evidences
            split=arr[i].split('|')
            #print split
            findProb=split[0].replace('P(','')
            evidence=split[1].replace(')','')
            #print findProb,evidence
            findProbDict,evidenceDict=dict(),dict()

            for j in findProb.split(','):
                if j.__contains__('='):     #Seperate the joint probability and make a dictionary
                    findProbDict[j.split("=")[0].strip()]=str2bool(j.split("=")[1].strip())
                else:
                    findProbDict[j]=''

            for j in evidence.split(','):   #Get evidence dictionary
                if j.__contains__('='):
                    #print "j.split(=)[1].strip()====",j.split("=")[1].strip(),(j.split("=")[1].strip()),
                    evidenceDict[j.split("=")[0].strip()]=str2bool(j.split("=")[1].strip())
                else:
                    findProbDict[j]=''
            print "evidenceDict=",evidenceDict

            findProbArr=findProbDict.keys()
            print "findProbArr=",findProbArr
            joint_prob_product=1
            for j in range(len(findProbArr)):
                tempevidenceDict=dict()
                tempevidenceDict=deepcopy(evidenceDict)
                for k in range(len(findProbArr)):
                    #print "*******",j,k,findProbArr[j],findProbArr[k]
                    if j<>k and chkParent(BaysNetArray,findProbArr[j],findProbArr[k]):
                        print "####",j,k,findProbArr[j],findProbArr[k],"tempevidenceDict=",tempevidenceDict
                        tempevidenceDict[findProbArr[k]]=str2bool(findProbDict[findProbArr[k]])

                #joint_prob_product=joint_prob_product*enumeration_ask(findProbArr[k],tempevidenceDict,bayesNet).show_approx()
                print "findProbArr[k],tempevidenceDict,bayesNet:",findProbArr[j],tempevidenceDict,bayesNet
                str=enumeration_ask(findProbArr[j],tempevidenceDict,bayesNet).show_approx()
                #print "str=",str,str.split(',')[0].split(':')[1],str.split(',')[1].split(':')[1]
                #if str.split(',')[0].split(':')[0]==findProbDict[findProbArr[j]]:
                if str2bool(findProbDict[findProbArr[j]])==False:
                    joint_prob_product=joint_prob_product*float(str.split(',')[0].split(':')[1])
                else:
                    joint_prob_product=joint_prob_product*float(str.split(',')[1].split(':')[1])

            print "for i=",i,"prob for ",arr[i],joint_prob_product
        else:
            if  arr[i].__contains__(','):
                findProb=arr[i].replace('P(','').replace(')','')
                evidence=dict()#split[1].replace(')','')
                print findProb,evidence
                findProbDict,evidenceDict=dict(),dict()

                for j in findProb.split(','):
                    if j.__contains__('='):     #Seperate the joint probability and make a dictionary
                        findProbDict[j.split("=")[0].strip()]=str2bool(j.split("=")[1].strip())
                    else:
                        findProbDict[j]=''

                findProbArr=findProbDict.keys()
                print "findProbArr=",findProbArr
                joint_prob_product=1
                for j in range(len(findProbArr)):
                    tempevidenceDict=dict()
                    tempevidenceDict=deepcopy(evidenceDict)
                    for k in range(len(findProbArr)):
                        #print "*******",j,k,findProbArr[j],findProbArr[k]
                        if j<>k and chkParent(BaysNetArray,findProbArr[j],findProbArr[k]):
                            print "####",j,k,findProbArr[j],findProbArr[k],"tempevidenceDict=",tempevidenceDict,"evidenceDict=",evidenceDict
                            tempevidenceDict[findProbArr[k]]=str2bool(findProbDict[findProbArr[k]])

                    #joint_prob_product=joint_prob_product*enumeration_ask(findProbArr[k],tempevidenceDict,bayesNet).show_approx()
                    print "findProbArr[k],tempevidenceDict,bayesNet:",findProbArr[j],tempevidenceDict,bayesNet
                    str=enumeration_ask(findProbArr[j],tempevidenceDict,bayesNet).show_approx()
                    #print "str=",str,str.split(',')[0].split(':')[1],str.split(',')[1].split(':')[1]
                    #if str.split(',')[0].split(':')[0]==findProbDict[findProbArr[j]]:
                    if str2bool(findProbDict[findProbArr[j]])==False:
                        print "Prob selected=",float(str.split(',')[0].split(':')[1])
                        joint_prob_product=joint_prob_product*float(str.split(',')[0].split(':')[1])
                    else:
                        print "Prob selected=",float(str.split(',')[1].split(':')[1])
                        joint_prob_product=joint_prob_product*float(str.split(',')[1].split(':')[1])

                print "for i=",i,"prob for ",arr[i],joint_prob_product
            else:
                findProb=arr[i].replace('P(','').replace(')','')
                evidence=dict()#split[1].replace(')','')
                #print findProb,evidence
                findProbDict,evidenceDict=dict(),dict()

                for j in findProb.split(','):
                    if j.__contains__('='):     #Seperate the joint probability and make a dictionary
                        findProbDict[j.split("=")[0].strip()]=str2bool(j.split("=")[1].strip())
                    else:
                        findProbDict[j]=''

                findProbArr=findProbDict.keys()
                for j in range(len(findProbArr)):
                    str=enumeration_ask(findProbArr[j],dict(),bayesNet).show_approx()
                    #print "str=",str,str.split(',')[0].split(':')[1],str.split(',')[1].split(':')[1]
                    #if str.split(',')[0].split(':')[0]==findProbDict[findProbArr[j]]:
                    if str2bool(findProbDict[findProbArr[j]])==False:
                        print "Prob selected=",float(str.split(',')[0].split(':')[1])
                        joint_prob_product=float(str.split(',')[0].split(':')[1])
                    else:
                        print "Prob selected=",float(str.split(',')[1].split(':')[1])
                        joint_prob_product=float(str.split(',')[1].split(':')[1])

                print "for i=",i,"prob for ",arr[i],joint_prob_product

#    print enumeration_ask('B',dict(C=False),bayesNet).show_approx()
#    print enumeration_ask('C',dict(B=True),bayesNet).show_approx()
