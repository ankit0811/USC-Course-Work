from copy import deepcopy
import random,sys,itertools,decimal,copy


def extend(s, var, val):
    s2 = s.copy()
    s2[var] = val
    return s2

def update(x, **entries):
    #Update a dict; or an object with slots; according to entries.
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


class DefaultDict(dict):
    """Dictionary with a default value for unknown keys."""
    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))


    def __copy__(self):
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy


    def __init__(self, default):
        self.default = default




def every(predicate, seq):
    #True if every element of seq satisfies predicate.
    for x in seq:
        if not predicate(x): return False
    return True


def probability(p):
    "Return true with probability p."
    return p > random.uniform(0.0, 1.0)



def if_(test, result, alternative):
    if test:
        if callable(result): return result()
        return result
    else:
        if callable(alternative): return alternative()
        return alternative



class ProbDist:

    def __getitem__(self, val):
        "Given a value, return P(value)."
        try: return self.prob[val]
        except KeyError: return 0

    def __setitem__(self, val, p):
        "Set P(val) = p."
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def __init__(self, varname='?', freqs=None):
        update(self, prob={}, varname=varname, values=[])
        if freqs:
            for (v, p) in freqs.items():
                self[v] = p
            self.normalize()

    def show_approx(self, numfmt='%.3g'):
        return ', '.join([('%s: ' + numfmt) % (v, p)
                          for (v, p) in sorted(self.prob.items())])


    def normalize(self):
        global BaysDecisionArr

        total = float(sum(self.prob.values()))
      #  print "######self =",self.values,self.prob[0],self.prob[1]
        if not (1.0-epsilon < total < 1.0+epsilon) and self.varname not in BaysDecisionArr:
            for val in self.prob:
                self.prob[val] /= total
#        print "######After total self =",self.values,self.prob[0],self.prob[1],self.varname

        return self
epsilon = 0.00


class JointProbDist(ProbDist):
    def __init__(self, variables):
        update(self, prob={}, variables=variables, vals=DefaultDict([]))

    def __getitem__(self, values):
        "Given a tuple or dict of values, return P(values)."
        values = event_values(values, self.variables)
        return ProbDist.__getitem__(self, values)

    def __setitem__(self, values, p):
        """Set P(values) = p.  Values can be a tuple or a dict; it must
        have a value for each of the variables in the joint. Also keep track
        of the values we have seen so far for each variable."""
        values = event_values(values, self.variables)
        self.prob[values] = p
        for var, val in zip(self.variables, values):
            if val not in self.vals[var]:
                self.vals[var].append(val)

    def values(self, var):
        "Return the set of possible values for a variable."
        return self.vals[var]

    def __repr__(self):
        return "P(%s)" % self.variables

def event_values(event, vars):

    global BaysDecisionArr,inArrVal
    arrTest=inArrVal.replace('|',',').replace('-','False').replace('+','True').split(',')

    for i in BaysDecisionArr:
        event[i]=True
        for j in arrTest:
            if j.__contains__('=') and i == j.split('=')[0].strip():
                event[i]=str2bool(j.split('=')[1].strip())


    if isinstance(event, tuple) and len(event) == len(vars):
        return event
    #elif vars in BaysDecisionArr:
     #   return tuple([True, False])
    else:
        #print event,vars
        return tuple([event[var] for var in vars])

#______________________________________________________________________________

class BayesNet:
    "Bayesian network containing only boolean-variable nodes."

    def __init__(self, node_specs=[]):
        "nodes must be ordered with parents before children."
        update(self, nodes=[], vars=[])
        for node_spec in node_specs:
            self.add(node_spec)

    def add(self, node_spec):
        """Add a node to the net. Its parents must already be in the
        net, and its variable must not."""
        node = BayesNode(*node_spec)
#        assert node.variable not in self.vars
#        assert every(lambda parent: parent in self.vars, node.parents)
        self.nodes.append(node)
        self.vars.append(node.variable)
        for parent in node.parents:
            self.variable_node(parent).children.append(node)

    def variable_node(self, var):
        for n in self.nodes:
            if n.variable == var:
                return n
        print "No var found",var
        #raise Exception("No such variable: %s" % var)

    def variable_values(self, var):
        #print "var=",var
        "Return the domain of var."
        '''if var in evidence:
            print "var in evidence",evidence[var]
            return [evidence[var]]
        else:'''
        return [True, False]
        #return [True]

    def __repr__(self):
        return 'BayesNet(%r)' % self.nodes


class BayesNode:

    def __init__(self, X, parents, cpt):
        if isinstance(parents, str): parents = parents.split()

        # We store the table always in the third form above.
        if isinstance(cpt, (float, int)): # no parents, 0-tuple
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            if cpt and isinstance(cpt.keys()[0], bool): # one parent, 1-tuple
                cpt = dict(((v,), p) for v, p in cpt.items())

        '''    assert isinstance(cpt, dict)
        for vs, p in cpt.items():
            assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert every(lambda v: isinstance(v, bool), vs)'''
#For chcecking utility comemnting assert 0 <= p <= 1
            #assert 0 <= p <= 1

        update(self, variable=X, parents=parents, cpt=cpt, children=[])

    def p(self, value, event):
        ptrue = self.cpt[event_values(event, self.parents)]
        ## print "if_(value, ptrue, 1 - ptrue)=",self.variable,self.parents,self.children,if_(value, ptrue, 1 - ptrue)
        return if_(value, ptrue, 1 - ptrue)

    def sample(self, event):
        return probability(self.p(True, event))

    def __repr__(self):
        return repr((self.variable, ' '.join(self.parents)))

# Burglary example [Fig. 14.2]

#T, False = True, False



#______________________________________________________________________________

def enumeration_ask(X, e, bn):
    """Return the conditional probability distribution of variable X
    given evidence e, from BayesNet bn. [Fig. 14.9]
    'False: 0.716, True: 0.284'"""
   # assert X not in e, "Query variable must be distinct from evidence"
    Q = ProbDist(X)
#    print "Added by Ankit:"
#    print X,e,bn
#    print type(X),type(e),type(bn)
#    print bn.variable_node(X),bn.variable_values(X)
    print "####bn.vars=",bn.vars
    for xi in bn.variable_values(X):
        Q[xi] = enumerate_all(bn.vars, extend(e, X, xi), bn)
   # print "### Q++++====>",Q.varname,Q.prob,Q.values
    return Q.normalize()

def enumerate_all(vars, e, bn):
    global BaysDecisionArr
    if not vars :
        #print "vars=",vars,type(vars)
        return 1.0
    Y, rest = vars[0], vars[1:]
    Ynode = bn.variable_node(Y)
    #print 'Y=',Y,'\nrest=',rest,"\nYNode=",Ynode,'\ne=',e,"\nBaysDecisionArr=",BaysDecisionArr
    if Y in BaysDecisionArr :
     ##   print "In BaysDecisionArr",'Y=',Y,"\nrest=",rest,'\ne=',e,'\nbn=',bn
        return 1.0 * enumerate_all(rest, e, bn)
    if Y in e:
#        print "Y in e"
  ##      print "In if Y in e",'Y=',Y,"\nrest=",rest,'\ne=',e,'\nbn=',bn
     #   print "Ynode.p(e[Y], e)=",e[Y],"=",Ynode.p(e[Y], e),"\nrest=",rest,enumerate_all(rest, e, bn)
        return Ynode.p(e[Y], e) * enumerate_all(rest, e, bn)
    else:
         #print "In else",'Y=',Y,"\nrest=",rest,'\ne=',e,'\nbn=',bn
#        print "Not Y not in e\n",'Y=',Y,'\ne=',e
#        print "bn var value=",bn.variable_node(Y),bn.variable_values(Y)
         sum1=0
         '''for y in bn.variable_values(Y):
             print 'y=',y,'rest=',rest,'extend=', extend(e, Y, y),'bn=', bn
             tmp1=Ynode.p(y, e)
             tmp=enumerate_all(rest, extend(e, Y, y), bn)
             sum1=sum1+tmp1*tmp
             print "tmp==",tmp1,tmp,sum1'''
         print "$$$$bn.variable_values(Y)=",Y,bn.variable_values(Y),Ynode.p(True, e),extend(e, Y, True),"enumerate_all(rest, extend(e, Y, True),bn)=",enumerate_all(rest, extend(e, Y, True),bn),Ynode.p(False, e),extend(e, Y, False),"enumerate_all(rest, extend(e, Y, False),bn)=",enumerate_all(rest, extend(e, Y, False),bn)
         return sum(Ynode.p(y, e) * enumerate_all(rest, extend(e, Y, y), bn)
                   for y in bn.variable_values(Y))

#______________________________________________________________________________


def str2bool(v):
    if type(v)==bool:
        return v
    return v.lower() in ("true")

def chkParent(NetArray,var,parent):
 #   print NetArray[1][0]
    for i in range(len(NetArray)):
        print "chkParent=",NetArray[i][0],",",var,",",NetArray[i][1],",",parent
        if NetArray[i][0]==var:
            if parent not in NetArray[i][1].split(' '):
                return False

    return True

def chkfindProbHasSameParents(input):
    print input

    inp=input.split(',')
    sameParent=[]
    diffParent=[]
    Parent=[]
    iParent=''
    for i in range(len(inp)):
        if inp[i].__contains__('='):
            print bayesNet.variable_node(inp[i].split('=')[0].strip()).parents
            if bayesNet.variable_node(inp[i].split('=')[0].strip()).parents<>[]:
                iParent=bayesNet.variable_node(inp[i].split('=')[0].strip()).parents[0]
            print inp[i].split('=')[0].strip(),iParent
        for j in range(i+1,len(inp)):
            if inp[j].__contains__('='):
               # print "in if=",bayesNet.variable_node(inp[j].split('=')[0].strip()).parents[0]
               # print "in if2",iParent
                if bayesNet.variable_node(inp[j].split('=')[0].strip()).parents[0]==iParent:
                   # print "In if"
                    sameParent.append([inp[i].strip(),inp[j].strip()])
                    Parent.append(iParent)

    if len(sameParent)>0:
        for i in inp:
            print "i.strip()=",i.strip()
            for j in range(len(sameParent)):
                if i.strip() not in sameParent[j]:
                    diffParent.append(i.strip())
    print "sameParen==>",sameParent,diffParent,Parent

    return sameParent,diffParent,Parent
    #if BaysNetArray




def computeProbability(input):
    global bayesNet,BaysNetArray,BaysDecisionArr,inArrVal
    print "input=",input
    input=input.replace('-','False').replace('+','True')
    #print input
    if input.__contains__('|'): #Conditional Probability given evidences
        split=input.split('|')
        #print split
        findProb=split[0].replace('P(','').strip()
        evidence=split[1].replace(')','').strip()
        print "findProb,evidence",findProb,evidence
        findProbDict,evidenceDict=dict(),dict()

        evidence_split=dict()
        findProb_split=dict()
        #if evidence.__contains__(','):
        for i in evidence.split(','):
            if i.__contains__('='):
                evidence_split[i.strip().split('=')[0].strip()]=i.strip().split('=')[1].strip()
            else:
                evidence_split[i.strip().split('=')[0].strip()]=''

        for i in findProb.split(','):
            if i.__contains__('='):
                findProb_split[i.strip().split('=')[0].strip()]=i.strip().split('=')[1].strip()
            else:
                findProb_split[i.strip().split('=')[0].strip()]=''



        print "findProb=",findProb,evidence,evidence_split
        #For handling P(C = + , D = +| A = +)
        if findProb.__contains__(','):
            sameParent,diffParent,Parent=chkfindProbHasSameParents(findProb)

            print "findProb====>",findProb,evidence,sameParent,diffParent,Parent
            newPorb=''
            prob=0
            if len(sameParent)>0:

                ParentList=['+','-']
                for k in range(len(sameParent)):
                    prob=0
                    if Parent[k] in evidence_split.keys():
                        ParentList=[evidence_split[Parent[k]]]
                    elif Parent[k] in findProb_split and findProb_split[Parent[k]] <> '':
                        ParentList=[findProb_split[Parent[k]]]
                    print "ParentList=",ParentList

                    for n in range(len(ParentList)):
                        for l in range(len(sameParent[k])):
                            newPorb=''
                            if l == 0:
                                if Parent[k] not in evidence_split.keys():
                                    newPorb='P('+sameParent[k][l] + ' , ' + Parent[k] + ' = ' + ParentList[n] + ' | '
                                else:
                                    newPorb='P('+sameParent[k][l] + ' | '

                                for m in range(len(diffParent)):
                                    newPorb=newPorb+diffParent[m] + ' , '
                                newPorb=newPorb+evidence + ')'
                                inArrVal=newPorb.replace('False','-').replace('True','+').replace('P(','').replace(')','')
                                tempProb=computeProbability(newPorb.replace('False','-').replace('True','+'))
                                print "newPorb=",newPorb,tempProb
                            elif l == len(sameParent[k])-1:
                                newPorb='P( '+sameParent[k][l]+ ' | '+ Parent[k] + ' = ' + ParentList[n] + ' , ' + evidence + ')';
                                inArrVal=newPorb.replace('False','-').replace('True','+').replace('P(','').replace(')','')
                                tempProb=tempProb*computeProbability(newPorb.replace('False','-').replace('True','+'))
                                print "newPorb=",newPorb,tempProb
                        prob=prob+tempProb
                print "prob=",prob
                print prob
                return prob

        for j in findProb.split(','):
            if j.__contains__('='):     #Seperate the joint probability and make a dictionary
                findProbDict[j.split("=")[0].strip()]=str2bool(j.split("=")[1].strip())
            else:
                findProbDict[j]=''

        for j in evidence.split(','):   #Get evidence dictionary
            if j.__contains__('='):
               ## print "j.split(=)[1].strip()====",j.split("=")[1].strip(),(j.split("=")[1].strip()),
                evidenceDict[j.split("=")[0].strip()]=str2bool(j.split("=")[1].strip())
            else:
                findProbDict[j]=''
       ## print "evidenceDict=",evidenceDict

        findProbArr=findProbDict.keys()
       ## print "findProbArr=",findProbArr
        joint_prob_product=1
        for j in range(len(findProbArr)):
            tempevidenceDict=dict()
            tempevidenceDict=deepcopy(evidenceDict)
            for k in range(len(findProbArr)):
                print "*******",j,k,findProbArr[j],findProbArr[k]
                if j<>k and chkParent(BaysNetArray,findProbArr[j],findProbArr[k]):
                ##    print "####",j,k,findProbArr[j],findProbArr[k],"tempevidenceDict=",tempevidenceDict
                    tempevidenceDict[findProbArr[k]]=str2bool(findProbDict[findProbArr[k]])

            print "findProbArr[k],tempevidenceDict,bayesNet:",findProbArr[j],tempevidenceDict,bayesNet
            if findProbArr[j] in tempevidenceDict.keys():
                if tempevidenceDict[findProbArr[j]]==True:
                    str='False: 0.0, True: 1.0'
                else:
                    str='False: 1.0, True: 0.0'
            else:
                str=enumeration_ask(findProbArr[j],tempevidenceDict,bayesNet).show_approx()
            print "str==>",str
            #print "str=",str,str.split(',')[0].split(':')[1],str.split(',')[1].split(':')[1]
            #if str.split(',')[0].split(':')[0]==findProbDict[findProbArr[j]]:
            if str2bool(findProbDict[findProbArr[j]])==False:
                joint_prob_product=joint_prob_product*float(str.split(',')[0].split(':')[1])
            else:
                joint_prob_product=joint_prob_product*float(str.split(',')[1].split(':')[1])
        #print "###input=",input
        return joint_prob_product
    else:
        if  input.__contains__(','):
            findProb=input.replace('P(','').replace(')','')
            evidence=dict()#split[1].replace(')','')
           ## print findProb,evidence
            findProbDict,evidenceDict=dict(),dict()

            for j in findProb.split(','):
                if j.__contains__('='):     #Seperate the joint probability and make a dictionary
                    findProbDict[j.split("=")[0].strip()]=str2bool(j.split("=")[1].strip())
                else:
                    findProbDict[j]=''

            findProbArr=findProbDict.keys()
          ##  print "findProbArr=",findProbArr
            joint_prob_product=1
            for j in range(len(findProbArr)):
                tempevidenceDict=dict()
                tempevidenceDict=deepcopy(evidenceDict)
                for k in range(len(findProbArr)):
                    #print "*******",j,k,findProbArr[j],findProbArr[k]
                    if j<>k and chkParent(BaysNetArray,findProbArr[j],findProbArr[k]):
                     #   print "####",j,k,findProbArr[j],findProbArr[k],"tempevidenceDict=",tempevidenceDict,"evidenceDict=",evidenceDict
                        tempevidenceDict[findProbArr[k]]=str2bool(findProbDict[findProbArr[k]])

                #joint_prob_product=joint_prob_product*enumeration_ask(findProbArr[k],tempevidenceDict,bayesNet).show_approx()
             #   print "findProbArr[k],tempevidenceDict,bayesNet:",findProbArr[j],tempevidenceDict,bayesNet
                str=enumeration_ask(findProbArr[j],tempevidenceDict,bayesNet).show_approx()
                #print "str=",str,str.split(',')[0].split(':')[1],str.split(',')[1].split(':')[1]
                #if str.split(',')[0].split(':')[0]==findProbDict[findProbArr[j]]:
                if str2bool(findProbDict[findProbArr[j]])==False:
                  #  print "Prob selected=",float(str.split(',')[0].split(':')[1])
                    joint_prob_product=joint_prob_product*float(str.split(',')[0].split(':')[1])
                else:
                  #  print "Prob selected=",float(str.split(',')[1].split(':')[1])
                    joint_prob_product=joint_prob_product*float(str.split(',')[1].split(':')[1])
            #print "###input=",input
            return joint_prob_product
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
           # print "###input=",input
            return joint_prob_product

#    print enumeration_ask('B',dict(C=False),bayesNet).show_approx()
#    print enumeration_ask('C',dict(B=True),bayesNet).show_approx()

def computeEU(input):
    global BaysUtilityArr,inArrVal

    EU=0
    expectedUtilFor=input.replace('EU(','').replace(')','').replace('|',',').split(',') #replace('|',',') as it was taking two | in case of EU(A=+|B=+)
#    print expectedUtilFor
    expectedUtilDict=dict()
    utilityLookupDict=dict()
    for i in expectedUtilFor:
        expectedUtilDict[i.split(' = ')[0].strip()]=i.split(' = ')[1].strip()

#    print expectedUtilDict


    utilityNodeArr=[]
#    print BaysUtilityArr[1].split(' ')

    for k in BaysUtilityArr[1].split(' '):
        #print "k=",k
        if k not in expectedUtilDict.keys():
            utilityNodeArr.append(k)
        else:
            if k in expectedUtilDict.keys():
                if str(expectedUtilDict[k])=='+':
                    utilityLookupDict[k]=True
                else:
                    utilityLookupDict[k]=False

 #   print utilityNodeArr



    lst = map(list, itertools.product(['+', '-'], repeat=len(utilityNodeArr)))

    for i in range(len(lst)):
        new_prob="P("
        utilLookUp=[]
        for j in range(len(utilityNodeArr)):
            #Compute Utility multiplying factor
            if str(lst[i][j])=='+':
                utilityLookupDict[utilityNodeArr[j]]=True
            else:
                utilityLookupDict[utilityNodeArr[j]]=False

            if j==len(utilityNodeArr)-1:
                #print new_prob,str(utilityNodeArr[j]) ,' = ', str(lst[i][j])+' |'
                new_prob=new_prob+ str(utilityNodeArr[j]) +' = ' + str(lst[i][j])
                #Adding the condiitonal part
                for k in range(len(expectedUtilFor)):
                    if k==0:
                   #     print"#################In k====0",expectedUtilFor
                        new_prob=new_prob+ ' | '
                    if k==len(expectedUtilFor)-1:
                        new_prob=new_prob+expectedUtilFor[k]+')'
                    else:
                        new_prob=new_prob+expectedUtilFor[k]+', '

            else:
                new_prob=new_prob+ str(utilityNodeArr[j]) +' = ' + str(lst[i][j]) + ' , '

        for k in BaysUtilityArr[1].split(' '):
            utilLookUp.append(utilityLookupDict[k])
#        print new_prob,utilLookUp,tuple(utilLookUp),utilityLookupDict
        inArrVal=new_prob.replace('P(','').replace(')','')
        prob=computeProbability(new_prob)
        print "@@@@@@@Prob=",new_prob,' == ',prob,tuple(utilLookUp)
        #Adding If condition as tuple for one value was coming as (true,) and hence genrating error while lookup
        if len(utilLookUp)==1:
            EU=EU+prob*BaysUtilityArr[2][utilLookUp[0]]
            print BaysUtilityArr[2][utilLookUp[0]]
        else:
            EU=EU+prob*BaysUtilityArr[2][tuple(utilLookUp)]
            print BaysUtilityArr[2][tuple(utilLookUp)]
 #       print EU

    return EU


arr=[]
BaysDecisionArr=[]
BaysNetArray=[]
bayesNet=[]
BaysUtilityArr=[]

def readFile():
    global arr,BaysUtilityArr,BaysDecisionArr,BaysNetArray,bayesNet
    txt=open(sys.argv[-1])
    txtread=""
    FinalArr=[]
    IntermediateArr=[]
    while txtread<>'******':
        txtread=txt.readline().strip()
        if txtread<>'******':
            arr.append(txtread)

    txtread=txt.readline().strip()
    while txtread<>'' and txtread<>'******':
        IntermediateArr=[]
        UtilityDict=dict()
        chkinConditional=False
        if txtread.__contains__('|'):
            IntermediateArr.append(txtread.split('|')[0].strip())
            IntermediateArr.append(txtread.split('|')[1].strip())
            txtread=txt.readline().strip()

            while txtread.__contains__('***')==False and txtread<>'': #<> '***' or txtread <> '******':
                inArr=txtread.split(' ')
                TrueFalseArr=[]
  #              print "inArr=",inArr,txtread,"txtread"

                for i in range(1,len(inArr)):
                    if inArr[i]=='+':
                        TrueFalseArr.append(True)
                    else:
                        TrueFalseArr.append(False)
                if len(TrueFalseArr)<>1:
                    UtilityDict[tuple(TrueFalseArr)]=float(inArr[0])
                else:
                    UtilityDict[TrueFalseArr[0]]=float(inArr[0])

                txtread=txt.readline().strip()
   #             print "TrueFalseArr",TrueFalseArr
            IntermediateArr.append(UtilityDict)
            if IntermediateArr[0]=='utility':
                BaysUtilityArr=deepcopy(IntermediateArr)
            else:
                FinalArr.append(IntermediateArr)
            txtread=txt.readline().strip()
            chkinConditional=True
        else:
            IntermediateArr.append(txtread)
            IntermediateArr.append('')
            txtread=txt.readline().strip()
            if txtread=='decision':
                IntermediateArr.append(1)
                BaysDecisionArr.append(IntermediateArr[0])

            else:
                IntermediateArr.append(float(txtread))
            txtread=txt.readline().strip() #skipping '***'
        if chkinConditional==False:
            FinalArr.append(IntermediateArr)
            txtread=txt.readline().strip()

    #    print IntermediateArr,BaysDecisionArr
        BaysNetArray=deepcopy(FinalArr)
    print "Arr=",arr,"\n\nBayUtilArr=",BaysUtilityArr,"\n\nBaysNetArray=",BaysNetArray,"\n\nBaysDecisionArr=",BaysDecisionArr
    tempArr=[]
    for i in range(len(BaysNetArray)):
     #   print "^^^^Tuple i=",tuple(BaysNetArray[i])
        tempArr.append(tuple(BaysNetArray[i]))
    print tempArr
    bayesNet=BayesNet(tempArr)
    print bayesNet
    txt.close()

readFile()




def computeMEU(input):
    #computeMEU('MEU(Infiltration | LeakIdea = +)')
    if input.__contains__('|'):
        probVar=input.replace('MEU(','').replace(')','').split('|')[0]
        evidenceVar=input.replace('MEU(','').replace(')','').split('|')[1]


        probArr=probVar.split(',')
        probDict=dict()
        probVarArray=[]
        probGivenArray=[]
        for i in range(len(probArr)):
            if probArr[i].__contains__(' = '):
                probDict[probArr[i].strip().split(' = ')[0].strip()]=probArr[i].strip().split(' = ')[1].strip()
                probGivenArray.append(probArr[i].strip().split('=')[0].strip()+' = '+probArr[i].strip().split(' = ')[1].strip())
            else:
                probDict[probArr[i].strip()]='';
                probVarArray.append(probArr[i].strip())
        print probDict,probGivenArray,probVarArray


        evidenceArr=evidenceVar.split(',')
        evidenceDict=dict()
        evidenceVarArray=[]
        evidenceGivenArray=[]
        for i in range(len(evidenceArr)):
            if evidenceArr[i].__contains__(' = '):
                evidenceDict[evidenceArr[i].strip().split(' = ')[0].strip()]=evidenceArr[i].strip().split(' = ')[1].strip()
                evidenceGivenArray.append(evidenceArr[i].strip().split('=')[0].strip()+' = '+evidenceArr[i].strip().split(' = ')[1].strip())
            else:
                evidenceDict[evidenceArr[i].strip()]='';
                evidenceVarArray.append(evidenceArr[i].strip())
        print evidenceDict,evidenceGivenArray,evidenceVarArray


        lstprob = map(list, itertools.product(['+', '-'], repeat=len(probVarArray)))
        print "lstprob=",lstprob

        lstevidence = map(list, itertools.product(['+', '-'], repeat=len(evidenceVarArray)))
        print "lstevidence=",lstevidence

        #case i (when both given var are null)
        if len(evidenceGivenArray)==0 and len(probGivenArray)==0:
            maxVal=-9999999999
            for k1 in range(len(lstprob)):
                newMEU='EU('
                for j1 in range(len(probVarArray)):
                    if j1==len(probVarArray)-1:
                        newMEU=newMEU + probVarArray[j1] + ' = ' +lstprob[k1][j1] +' | '
                    else:
                        newMEU=newMEU + probVarArray[j1] + ' = ' +lstprob[k1][j1] +' , '

                for l1 in range(len(lstevidence)):
                    newMEU1=''
                    for m1 in range(len(evidenceVarArray)):
                        if m1==len(evidenceVarArray)-1:
                            newMEU1=newMEU1 + evidenceVarArray[m1] + ' = ' +lstevidence[l1][m1] +' )'

                        else:
                            newMEU1=newMEU1 + evidenceVarArray[m1] + ' = ' +lstevidence[l1][m1] +' , '
                    #Need to call computeMEU() here
                    print "$$$$$newMeu========>",newMEU+newMEU1
                    MEUVal=computeEU(newMEU+newMEU1)
                    print "$$$$$$$VAL",newMEU+newMEU1,MEUVal
                    if maxVal<MEUVal:
                        maxVal=MEUVal
                        maxFor=newMEU+newMEU1


        #case ii (when given evidence var are present and prob var are null)
        if len(evidenceGivenArray)<>0 and len(probGivenArray)==0:
            maxVal=-999999999
            for k1 in range(len(lstprob)):
                newMEU='EU('
                for j1 in range(len(probVarArray)):
                    if j1==len(probVarArray)-1:
                        newMEU=newMEU + probVarArray[j1] + ' = ' +lstprob[k1][j1] +' | '
                    else:
                        newMEU=newMEU + probVarArray[j1] + ' = ' +lstprob[k1][j1] +' , '

                for l1 in range(len(lstevidence)):
                    newMEU1=''

                    for m1 in range(len(evidenceVarArray)):
                        #if m1==len(evidenceVarArray)-1:
                        #    newMEU1=newMEU1 + evidenceVarArray[m1] + ' = ' +lstevidence[l1][m1] +' )'
                        #else:

                        newMEU1=newMEU1 + evidenceVarArray[m1] + ' = ' +lstevidence[l1][m1] +' , '

                    for n1 in range(len(evidenceGivenArray)):
                        if n1==len(evidenceGivenArray)-1:
                            newMEU1=newMEU1 + evidenceGivenArray[n1] +' )'

                        else:
                            newMEU1=newMEU1 + evidenceGivenArray[n1] +' , '

                    #Need to call computeMEU() here
                    print "$$$$$newMeu========>",newMEU+newMEU1
                    MEUVal=computeEU(newMEU+newMEU1)
                    print "$$$$$$$VAL",newMEU+newMEU1,MEUVal
                    if maxVal<MEUVal:
                        maxVal=MEUVal
                        maxFor=newMEU+newMEU1


        #case iii (when given evidence var are null and prob var are present)
        if len(evidenceGivenArray)==0 and len(probGivenArray)<>0:
            maxVal=-999999999
            for k1 in range(len(lstprob)):
                newMEU='EU('
                for j1 in range(len(probVarArray)):
                    #if j1==len(probVarArray)-1:
                    #    newMEU=newMEU + probVarArray[j1] + ' = ' +lstprob[k1][j1] +' | '
                    #else:
                    newMEU=newMEU + probVarArray[j1] + ' = ' +lstprob[k1][j1] +' , '
                for j11 in range(len(probGivenArray)):
                    if j11==len(probGivenArray)-1:
                        newMEU=newMEU + probGivenArray[j11] + ' | '
                    else:
                        newMEU=newMEU + probGivenArray[j11] + ' , '

                for l1 in range(len(lstevidence)):
                    newMEU1=''
                    for m1 in range(len(evidenceVarArray)):
                        if m1==len(evidenceVarArray)-1:
                            newMEU1=newMEU1 + evidenceVarArray[m1] + ' = ' +lstevidence[l1][m1] +' )'
                        else:
                            newMEU1=newMEU1 + evidenceVarArray[m1] + ' = ' +lstevidence[l1][m1] +' , '

                    #Need to call computeMEU() here
                    print "$$$$$newMeu========>",newMEU+newMEU1
                    MEUVal=computeEU(newMEU+newMEU1)
                    print "$$$$$$$VAL",newMEU+newMEU1,MEUVal
                    if maxVal<MEUVal:
                        maxVal=MEUVal
                        maxFor=newMEU+newMEU1





        #case iv (when given evidence var are present and prob var are present)
        if len(evidenceGivenArray)<>0 and len(probGivenArray)<>0:
            maxVal=-999999999
            for k1 in range(len(lstprob)):
                newMEU='EU('
                for j1 in range(len(probVarArray)):
                    #if j1==len(probVarArray)-1:
                    #    newMEU=newMEU + probVarArray[j1] + ' = ' +lstprob[k1][j1] +' | '
                    #else:
                    newMEU=newMEU + probVarArray[j1] + ' = ' +lstprob[k1][j1] +' , '
                for j11 in range(len(probGivenArray)):
                    if j11==len(probGivenArray)-1:
                        newMEU=newMEU + probGivenArray[j11] + ' | '
                    else:
                        newMEU=newMEU + probGivenArray[j11] + ' , '

                for l1 in range(len(lstevidence)):
                    newMEU1=''
                    for m1 in range(len(evidenceVarArray)):
                        #if m1==len(evidenceVarArray)-1:
                        #    newMEU1=newMEU1 + evidenceVarArray[m1] + ' = ' +lstevidence[l1][m1] +' )'
                        #else:
                        newMEU1=newMEU1 + evidenceVarArray[m1] + ' = ' +lstevidence[l1][m1] +' , '
                    for n1 in range(len(evidenceGivenArray)):
                        if n1==len(evidenceGivenArray)-1:
                            newMEU1=newMEU1 + evidenceGivenArray[n1] +' )'
                        else:
                            newMEU1=newMEU1 + evidenceGivenArray[n1] +' , '
                    #Need to call computeMEU() here
                    print "$$$$$newMeu========>",newMEU+newMEU1
                    MEUVal=computeEU(newMEU+newMEU1)
                    print "$$$$$$$VAL",newMEU+newMEU1,MEUVal
                    if maxVal<MEUVal:
                        maxVal=MEUVal
                        maxFor=newMEU+newMEU1


        input_arr=input.replace('MEU(','').replace(')','').split('|')
        input_prob=input_arr[0].strip().split(',')
        input_evidence=input_arr[1].strip().split(',')

        final_arr=maxFor.replace('EU(','').replace(')','').split('|')
        final_prob=final_arr[0].strip().split(',')
        final_evidence=final_arr[1].strip().split(',')

        print input_prob,'\n',final_prob
        print input_evidence,'\n',final_evidence

        outMax=''
        for i1 in input_prob:
            if i1.__contains__('=')==False:
                for j1 in final_prob:
                    if j1.strip().split('=')[0].strip()==i1.strip():
                        outMax=outMax+j1.strip().split('=')[1].strip()+' '

        for i1 in input_evidence:
            if i1.__contains__('=')==False:
                for j1 in final_evidence:
                    if j1.strip().split('=')[0].strip()==i1.strip():
                        outMax=outMax+j1.strip().split('=')[1].strip()+' '


        print 'outMax=',outMax
        print maxFor,input,maxVal
        return outMax,maxVal


    elif input.__contains__(','):
        probVarDict=dict()
        #2 cases. i. All are missing
        #        ii. Some are missing

        for i in input.replace('MEU(','').replace(')','').split(','):
            if i.strip().__contains__(' = '):
                probVarDict[i.strip().split(' = ')[0].strip()]=i.strip().split(' = ')[1].strip()
            else:
                probVarDict[i.strip()]=''

        probVarEnum=[]
        probVarGiven=[]

        for i in probVarDict:
            if probVarDict[i]=='':
                probVarEnum.append(i)
            else:
                probVarGiven.append(i+' = '+ probVarDict[i])

        print probVarDict,probVarGiven,probVarEnum
        #Case i
        if len(probVarGiven)==0:
            lst=map(list, itertools.product(['+', '-'], repeat=len(probVarEnum)))
            print lst
            maxVal=-9999999999999
            maxFor=''
            for i in range(len(lst)):
                newEU='EU('
                for j in range(len(probVarEnum)):
                    if j==len(probVarEnum)-1:
                        newEU=newEU + probVarEnum[j]+ ' = ' + lst[i][j] + ' )'
                    else:
                        newEU=newEU + probVarEnum[j]+ ' = ' + lst[i][j] + ' , '
                EUVal=computeEU(newEU)
                print "########newEU",newEU,EUVal

                if maxVal<EUVal:
                    maxFor=lst[i]
                    maxVal=EUVal

            print maxFor,probVarEnum,maxVal

        #Case ii
        else:

            lst=map(list, itertools.product(['+', '-'], repeat=len(probVarEnum)))
            print lst
            maxVal=-9999999999999
            maxFor=''
            for i in range(len(lst)):
                newEU='EU('
                for j in range(len(probVarEnum)):
                    if j==len(probVarEnum)-1:
                        newEU=newEU + probVarEnum[j]+ ' = ' + lst[i][j] + ' , '
                        for k in range(len(probVarGiven)):
                            if k==len(probVarGiven)-1:
                                newEU=newEU + probVarGiven[k]+ ' )'
                            else:
                                newEU=newEU + probVarGiven[k]+ ' , '

                    else:
                        newEU=newEU + probVarEnum[j]+ ' = ' + lst[i][j] + ' , '
                print "########newEU",newEU
                EUVal=computeEU(newEU)
                print "########newEU",newEU,EUVal

                if maxVal<EUVal:
                    maxFor=lst[i]
                    maxVal=EUVal

            print maxFor,probVarEnum,maxVal

        print "Out Of ifelse loop:",maxFor,probVarEnum,maxVal,input
        outFor=''
        for i in input.replace('MEU(','').replace(')','').split(','):
            if i.strip() in probVarEnum:
                outFor=outFor+maxFor[probVarEnum.index(i.strip())]+' '

        return outFor,maxVal

    else:
        if input.__contains__(' = '):
            print computeEU(input.replace('MEU('),'EU(')
            return input.split(' = ')[1].strip(),computeEU(input.replace('MEU('),'EU(')
        else:
            lst = map(list, itertools.product(['+', '-'], repeat=1))
            maxVal=-9999999999999999
            maxFor=''
            for i in range(len(lst)):
                EUVal=computeEU(input.replace('MEU(','EU(').replace(')',' = '+str(lst[i][0])+' )'))
                if maxVal<EUVal:
                    maxFor=lst[i][0]
                    maxVal=EUVal
            return  maxFor+' ',maxVal
inArrVal=''

"""outputFile="output.txt"
txt=open(outputFile,'w')
for i in range(len(arr)):

    if arr[i][0:2]==('P('):
        print "arr[i]=",arr[i]
        inArrVal=arr[i].replace('P(','').replace(')','')

        outputVal=computeProbability(arr[i])
        print "**********Probability for ",arr[i]," is ",outputVal
        #rounding two nearest two decimal as round doesnot work on 0.215 giving 0.21 instea of 0.22
        txt.write(str(decimal.Decimal(str(outputVal)).quantize(decimal.Decimal('1.00'), rounding=decimal.ROUND_HALF_UP))+"\n")
        print "\n"
    elif arr[i][0:3]==('EU('):
        print "**********Expected Utility for "
        inArrVal=arr[i].replace('EU(','').replace(')','')

        outputVal=computeEU(arr[i])
        print "**********Expected Utility for ",arr[i]," is ",outputVal
        txt.write(str(decimal.Decimal(str(outputVal)).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))+"\n")
    elif arr[i][0:4]==('MEU('):
        print "**********In Maximum Expected Utility for "
        inArrVal=arr[i].replace('MEU(','').replace(')','')

        outputVal=computeMEU(arr[i])
        print "**********Maximum Expected Utility for ",arr[i]," is ",outputVal,outputVal[0],outputVal[0]
        txt.write(outputVal[0]+''+str(decimal.Decimal(str(outputVal[1])).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))+"\n")
        #txt.write(outputVal[0]+''+str(int(round(outputVal[1],0)))+"\n")

txt.close()
"""

##OUTPUT TEST
out1=computeMEU('MEU(NightDefense = - , Infiltration )')

print out1
