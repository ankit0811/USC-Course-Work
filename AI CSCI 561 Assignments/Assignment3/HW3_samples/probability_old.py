"""Probability models. (Chapter 13-15)
"""

from copy import deepcopy
import random


def extend(s, var, val):
    s2 = s.copy()
    s2[var] = val
    return s2

def update(x, **entries):
    """Update a dict; or an object with slots; according to entries.
    >>> update({'a': 1}, a=10, b=20)
    {'a': 10, 'b': 20}
    >>> update(Struct(a=1), a=10, b=20)
    Struct(a=10, b=20)
    """
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


class DefaultDict(dict):
    """Dictionary with a default value for unknown keys."""
    def __init__(self, default):
        self.default = default

    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))

    def __copy__(self):
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy


def every(predicate, seq):
    """True if every element of seq satisfies predicate.
    >>> every(callable, [min, max])
    1
    >>> every(callable, [min, 3])
    0
    """
    for x in seq:
        if not predicate(x): return False
    return True


def probability(p):
    "Return true with probability p."
    return p > random.uniform(0.0, 1.0)



def if_(test, result, alternative):
    """Like C++ and Java's (test ? result : alternative), except
    both result and alternative are always evaluated. However, if
    either evaluates to a function, it is applied to the empty arglist,
    so you can delay execution by putting it in a lambda.
    >>> if_(2 + 2 == 4, 'ok', lambda: expensive_computation())
    'ok'
    """
    if test:
        if callable(result): return result()
        return result
    else:
        if callable(alternative): return alternative()
        return alternative



class ProbDist:
    """A discrete probability distribution.  You name the random variable
    in the constructor, then assign and query probability of values.
    >>> P = ProbDist('Flip'); P['H'], P['T'] = 0.25, 0.75; P['H']
    0.25
    >>> P = ProbDist('X', {'lo': 125, 'med': 375, 'hi': 500})
    >>> P['lo'], P['med'], P['hi']
    (0.125, 0.375, 0.5)
    """
    def __init__(self, varname='?', freqs=None):
        """If freqs is given, it is a dictionary of value: frequency pairs,
        and the ProbDist then is normalized."""
        update(self, prob={}, varname=varname, values=[])
        if freqs:
            for (v, p) in freqs.items():
                self[v] = p
            self.normalize()

    def __getitem__(self, val):
        "Given a value, return P(value)."
        try: return self.prob[val]
        except KeyError: return 0

    def __setitem__(self, val, p):
        "Set P(val) = p."
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        global BaysDecisionArr
        """Make sure the probabilities of all values sum to 1.
        Returns the normalized distribution.
        Raises a ZeroDivisionError if the sum of the values is 0.
        >>> P = ProbDist('Flip'); P['H'], P['T'] = 35, 65
        >>> P = P.normalize()
        >>> print '%5.3f %5.3f' % (P.prob['H'], P.prob['T'])
        0.350 0.650
        """

        total = float(sum(self.prob.values()))
      #  print "######self =",self.values,self.prob[0],self.prob[1]
        if not (1.0-epsilon < total < 1.0+epsilon) and self.varname not in BaysDecisionArr:
            for val in self.prob:
                self.prob[val] /= total
       # print "######After total self =",self.values,self.prob[0],self.prob[1]
        return self

    def show_approx(self, numfmt='%.3g'):
        """Show the probabilities rounded and sorted by key, for the
        sake of portable doctests."""
        return ', '.join([('%s: ' + numfmt) % (v, p)
                          for (v, p) in sorted(self.prob.items())])

    '''def printProbDist(self):
        for i in self:
            print i
'''
epsilon = 0.00

class JointProbDist(ProbDist):
    """A discrete probability distribute over a set of variables.
    >>> P = JointProbDist(['X', 'Y']); P[1, 1] = 0.25
    >>> P[1, 1]
    0.25
    >>> P[dict(X=0, Y=1)] = 0.5
    >>> P[dict(X=0, Y=1)]
    0.5"""
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
    """Return a tuple of the values of variables vars in event.
    >>> event_values ({'A': 10, 'B': 9, 'C': 8}, ['C', 'A'])
    (8, 10)
    >>> event_values ((1, 2), ['C', 'A'])
    (1, 2)
    """
    if isinstance(event, tuple) and len(event) == len(vars):
        return event
    else:
        return tuple([event[var] for var in vars])

#______________________________________________________________________________

def enumerate_joint_ask(X, e, P):
    """Return a probability distribution over the values of the variable X,
    given the {var:val} observations e, in the JointProbDist P. [Section 13.3]
    >>> P = JointProbDist(['X', 'Y'])
    >>> P[0,0] = 0.25; P[0,1] = 0.5; P[1,1] = P[2,1] = 0.125
    >>> enumerate_joint_ask('X', dict(Y=1), P).show_approx()
    '0: 0.667, 1: 0.167, 2: 0.167'
    """
    assert X not in e, "Query variable must be distinct from evidence"
    Q = ProbDist(X) # probability distribution for X, initially empty
    Y = [v for v in P.variables if v != X and v not in e] # hidden vars.
    for xi in P.values(X):
        Q[xi] = enumerate_joint(Y, extend(e, X, xi), P)
    return Q.normalize()

def enumerate_joint(vars, e, P):
    """Return the sum of those entries in P consistent with e,
    provided vars is P's remaining variables (the ones not in e)."""
    if not vars:
        return P[e]
    Y, rest = vars[0], vars[1:]
    return sum([enumerate_joint(rest, extend(e, Y, y), P)
                for y in P.values(Y)])

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
        assert node.variable not in self.vars
        assert every(lambda parent: parent in self.vars, node.parents)
        self.nodes.append(node)
        self.vars.append(node.variable)
        for parent in node.parents:
            self.variable_node(parent).children.append(node)

    def variable_node(self, var):
        """Return the node for the variable named var.
        >>> burglary.variable_node('Burglary').variable
        'Burglary'"""
        for n in self.nodes:
            if n.variable == var:
                return n
        raise Exception("No such variable: %s" % var)

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
    """A conditional probability distribution for a boolean variable,
    P(X | parents). Part of a BayesNet."""

    def __init__(self, X, parents, cpt):
        """X is a variable name, and parents a sequence of variable
        names or a space-separated string.  cpt, the conditional
        probability table, takes one of these forms:

        * A number, the unconditional probability P(X=true). You can
          use this form when there are no parents.

        * A dict {v: p, ...}, the conditional probability distribution
          P(X=true | parent=v) = p. When there's just one parent.

        * A dict {(v1, v2, ...): p, ...}, the distribution P(X=true |
          parent1=v1, parent2=v2, ...) = p. Each key must have as many
          values as there are parents. You can use this form always;
          the first two are just conveniences.

        In all cases the probability of X being false is left implicit,
        since it follows from P(X=true).

        """
        if isinstance(parents, str): parents = parents.split()

        # We store the table always in the third form above.
        if isinstance(cpt, (float, int)): # no parents, 0-tuple
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            if cpt and isinstance(cpt.keys()[0], bool): # one parent, 1-tuple
                cpt = dict(((v,), p) for v, p in cpt.items())

        assert isinstance(cpt, dict)
        for vs, p in cpt.items():
            assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert every(lambda v: isinstance(v, bool), vs)
#For chcecking utility comemnting assert 0 <= p <= 1
            #assert 0 <= p <= 1

        update(self, variable=X, parents=parents, cpt=cpt, children=[])

    def p(self, value, event):
        """Return the conditional probability
        P(X=value | parents=parent_values), where parent_values
        are the values of parents in event. (event must assign each
        parent a value.)
        >>> bn = BayesNode('X', 'Burglary', {T: 0.2, False: 0.625})
        >>> bn.p(False, {'Burglary': False, 'Earthquake': True})
        0.375"""
        assert isinstance(value, bool)
        ptrue = self.cpt[event_values(event, self.parents)]
        return if_(value, ptrue, 1 - ptrue)

    def sample(self, event):
        """Sample from the distribution for this variable conditioned
        on event's values for parent_vars. That is, return True/False
        at random according with the conditional probability given the
        parents."""
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
    assert X not in e, "Query variable must be distinct from evidence"
    Q = ProbDist(X)
#    print "Added by Ankit:"
#    print X,e,bn
#    print type(X),type(e),type(bn)
#    print bn.variable_node(X),bn.variable_values(X)
    for xi in bn.variable_values(X):
        Q[xi] = enumerate_all(bn.vars, extend(e, X, xi), bn)
    return Q.normalize()

def enumerate_all(vars, e, bn):
    global BaysDecisionArr
    """Return the sum of those entries in P(vars | e{others})
    consistent with e, where P is the joint distribution represented
    by bn, and e{others} means e restricted to bn's other variables
    (the ones other than vars). Parents must precede children in vars."""
    if not vars:
        return 1.0
    Y, rest = vars[0], vars[1:]
    Ynode = bn.variable_node(Y)
   # print 'Y=',Y,'\nrest=',rest,"\nYNode=",Ynode,'\ne=',e,"\nBaysDecisionArr=",BaysDecisionArr
    if Y in BaysDecisionArr:
   #     print "In BaysDecisionArr",Y,rest
        return 1.0 * enumerate_all(rest, e, bn)
    if Y in e:
#        print "Y in e"
 #       print "Ynode.p(e[Y], e)=",e[Y],"=",Ynode.p(e[Y], e),"\n"
        return Ynode.p(e[Y], e) * enumerate_all(rest, e, bn)
    else:

#        print "Not Y not in e\n",'Y=',Y,'\ne=',e
#        print "bn var value=",bn.variable_node(Y),bn.variable_values(Y)
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
        if NetArray[i][0]==var:
            if NetArray[i][1]<>parent:
                return False

    return True

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
        return joint_prob_product
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
            print "###input=",input
            return joint_prob_product

#    print enumeration_ask('B',dict(C=False),bayesNet).show_approx()
#    print enumeration_ask('C',dict(B=True),bayesNet).show_approx()

def computeEU(input):
    global BaysUtilityArr

    EU=0
    expectedUtilFor=input.replace('EU(','').replace(')','').replace('|',',').split(',') #replace('|',',') as it was taking two | in case of EU(A=+|B=+)
    print expectedUtilFor
    expectedUtilDict=dict()
    utilityLookupDict=dict()
    for i in expectedUtilFor:
        expectedUtilDict[i.split(' = ')[0]]=i.split(' = ')[1]

    print expectedUtilDict


    utilityNodeArr=[]
    print BaysUtilityArr[1].split(' ')

    for k in BaysUtilityArr[1].split(' '):
        print "k=",k
        if k not in expectedUtilDict.keys():
            utilityNodeArr.append(k)
        else:
            if k in expectedUtilDict.keys():
                if str(expectedUtilDict[k])=='+':
                    utilityLookupDict[k]=True
                else:
                    utilityLookupDict[k]=False

    print utilityNodeArr


    import itertools
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
                        print"#################In k====0",expectedUtilFor
                        new_prob=new_prob+ ' | '
                    if k==len(expectedUtilFor)-1:
                        new_prob=new_prob+expectedUtilFor[k]+')'
                    else:
                        new_prob=new_prob+expectedUtilFor[k]+', '

            else:
                new_prob=new_prob+ str(utilityNodeArr[j]) +' = ' + str(lst[i][j]) + ' , '

        for k in BaysUtilityArr[1].split(' '):
            utilLookUp.append(utilityLookupDict[k])
        print new_prob,utilLookUp,tuple(utilLookUp),utilityLookupDict
        prob=computeProbability(new_prob)
        #Adding If condition as tuple for one value was coming as (true,) and hence genrating error while lookup
        if len(utilLookUp)==1:
            EU=EU+prob*BaysUtilityArr[2][utilLookUp[0]]
        else:
            EU=EU+prob*BaysUtilityArr[2][tuple(utilLookUp)]
        print EU

    return EU


    #print BaysUtilityArr[2][tuple([True,False])]





'''

bayesNet = BayesNet([
    ('LeakIdea', '', 0.4),
    ('NightDefense', 'LeakIdea', {True: 0.8,False: 0.3}),
    ('Infiltration','',0.5), #If decision node, then for probability given
    ('Demoralize', 'NightDefense Infiltration',{(True, True): 0.3, (True, False): 0.6, (False, True): 0.95, (False, False): 0.05})#,
    #('Utility','Demoralize',{True: 100,False: -10})
    ])

BaysNetArray = [
    ['LeakIdea', '', 0.4],
    ['NightDefense', 'LeakIdea', {True: 0.8,False: 0.3}],
    ['Infiltration','',0.5],
    ['Demoralize', 'NightDefense Infiltration',{(True, True): 0.3, (True, False): 0.6, (False, True): 0.95, (False, False): 0.05}]
    ]

bayesNet  = BayesNet([
    ('A', '', 0.4),
    ('B', 'A', {True: 0.8,False: 0.5}),
    ('C','B',{True:0.2,False:0.3}),
    ('D', 'A', {True: 0.8,False: 0.5})
    ])

BaysNetArray=[['A', '', 0.4],
              ['B', 'A', {True: 0.8,False: 0.5}],
              ['C','B',{True:0.2,False:0.3}],
              ['D', 'A', {True: 0.8,False: 0.5}]]



BaysDecisionArr=['LeakIdea','Infiltration']
BaysUtilityArr=['Utility','Demoralize Infiltration',{(True,False)  : 100,
                                                     (True,True) : 80,
                                                     (False,False) : -10,
                                                     (False,True): -50}]

BaysDecisionArr=[]
BaysUtilityArr=['Utility','Demoralize',{True:100,False:-10}]


BaysUtilityArr=['Utility','C D',{(True,True)  : 100,
                                 (True,False) : 50,
                                 (False,True) : 10,
                                 (False,False): 0}]


#arr=['P(A = -)','P(A = +, B = -)','P(C = -)','P(B = +, C = -)','P(B = + | C = -)']
arr=[#'P(NightDefense = +, Infiltration = -)',
     #'P(Demoralize = + | LeakIdea = +, Infiltration = +)'
     'P(Demoralize = + | LeakIdea = -, Infiltration = +)',
     'EU(Infiltration = +)',
     'EU(Infiltration = + | LeakIdea = +)'

     #SAMPLE3 'P(Demoralize = + | LeakIdea = -, Infiltration = -)',
     #SAMPLE3'EU(Infiltration = +, LeakIdea = +)'

     #SAMPLE4 'P(A = -)','P(A = +, B = -)','P(C = -)','P(B = +, C = -)','P(B = + | C = -)'
     ]
'''
arr=[]
BaysDecisionArr=[]
BaysNetArray=[]
bayesNet=[]
BaysUtilityArr=[]

def readFile():
    global arr,BaysUtilityArr,BaysDecisionArr,BaysNetArray,bayesNet
    txt=open("C:\\Users\\lenovo poc\\Google Drive\\usc study material\\AI\\Assignments\\Assignment3\\HW3_samples\\HW3_samples\\sample05.txt")
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
                print "inArr=",inArr,txtread,"txtread"

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
                print "TrueFalseArr",TrueFalseArr
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

        print IntermediateArr,BaysDecisionArr
        BaysNetArray=deepcopy(FinalArr)
    print "Arr=",arr,"\n\nBayUtilArr=",BaysUtilityArr,"\n\nBaysNetArray=",BaysNetArray,"\n\nBaysDecisionArr=",BaysDecisionArr
    tempArr=[]
    for i in range(len(BaysNetArray)):
        print "^^^^Tuple i=",tuple(BaysNetArray[i])
        tempArr.append(tuple(BaysNetArray[i]))
    print tempArr
    bayesNet=BayesNet(tempArr)
    print bayesNet
    txt.close()

readFile()

outputFile="output.txt"
txt=open(outputFile,'w')

import decimal

for i in range(len(arr)):
    if arr[i][0:2]==('P('):
        print "arr[i]=",arr[i]
        outputVal=computeProbability(arr[i])
        print "**********Probability for ",arr[i]," is ",outputVal
        #rounding two nearest two decimal as round doesnot work on 0.215 giving 0.21 instea of 0.22
        txt.write(str(decimal.Decimal(str(outputVal)).quantize(decimal.Decimal('1.00'), rounding=decimal.ROUND_HALF_UP))+"\n")
        print "\n"
    elif arr[i][0:3]==('EU('):
        outputVal=computeEU(arr[i])
        print "**********Expected Utility for ",arr[i]," is ",outputVal
        txt.write(str(decimal.Decimal(str(outputVal)).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_HALF_UP))+"\n")
txt.close()

