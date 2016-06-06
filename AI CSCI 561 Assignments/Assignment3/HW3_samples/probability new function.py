def computeProbability(input):
    global bayesNet,BaysNetArray,BaysDecisionArr


    input=input.replace('-','False').replace('+','True')
    #print input
    if input.__contains__('|'): #Conditional Probability given evidences
        split=input.split('|')
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
        print "###input=",input
        return input,joint_prob_product
    else:
        if  input.__contains__(','):
            findProb=input.replace('P(','').replace(')','')
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
            print "###input=",input
            return input,joint_prob_product
        else:
            findProb=input.replace('P(','').replace(')','')
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
            print "###input=",input
            return input,joint_prob_product
