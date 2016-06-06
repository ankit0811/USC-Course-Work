import sys
import re
import itertools
import copy

def printarray(arr):
    for i in range(len(arr)):
        tmp=''
        for j in range(len(arr[i])):
            tmp=tmp + str(arr[i][j]) + " "
        print tmp



#Reading Input file as Is without removing anything
def readFile():
    global Qry,KB
    txt=open(sys.argv[1])
    Qry=txt.readline().strip()
    print "Qry=",Qry
    NoKB=int(txt.readline())
    KB=[]
    for i in range(NoKB):
        statement=txt.readline().strip()
        if statement.find('=>')<>-1:
            tmp=statement.split('=>')

            tmp0=tmp[0].strip().split(" && ")
            tmp1=tmp[1].strip()
            tmp=[]
            for j in range(len(tmp0)):
                tmp.append(tmp0[j])
            tmp.append(tmp1)
        else:
            tmp=[statement]


        KB.append(tmp)
    print KB
    printarray(KB)


def isVariable(x):
    if type(x) is list :
        return False
    if str(x[0]).islower():
        return True
    return False


def isCompound(x):
    if type(x) is list:
        return False
    if x.find('(')<>-1:
        return True
    return False


def getArgsOp(x):
    #print "In getArgsOp x=",x
    op=x[0:x.index('(')]
    if x[x.index('(')+1:x.index(')')].find(', ')==-1:
        args=x[x.index('(')+1:x.index(')')]
    else:
        args=x[x.index('(')+1:x.index(')')].split(', ')

    return op,args

def extend(s, var, val):
    s2 = s.copy()
    s2[var] = val
    return s2


def unify_var(var, x, s):
    #print "Called unify var"
    if var in s:
        return unify(s[var], x, s)
    else:
        return extend(s, var, x)


def unify(x,y,theta):

    if theta==Failure:
        return Failure
    elif x==y:
        return theta
    elif isVariable(x):
        return unify_var(x,y,theta)
    elif isVariable(y):
        return unify_var(y,x,theta)
    elif isCompound(x) and isCompound(y):
        x_op,x_args=getArgsOp(x)
        y_op,y_args=getArgsOp(y)
        return unify(x_args,y_args,unify(x_op,y_op,theta))
    elif type(x) is list and type(y) is list :
        return unify(x[1:],y[1:],unify(x[0],y[0],theta))
    else:
        return str(Failure)



def fetchRulesForGoals(KB,goal):
    tmp=[]
    for i in range(len(KB)):
        if isCompound(KB[i][len(KB[i])-1]) and isCompound(goal):
            x_op,x_arg=getArgsOp(KB[i][len(KB[i])-1])
            y_op,y_arg=getArgsOp(goal)
            if x_op==y_op:
                #Original One
                tmp.append(KB[i])


    print "Tmp from fetchRulesForGoals= ",goal,tmp
    return tmp

counter = itertools.count()

#Changed localVarMap from local to standardize definition to global
def standardize(rule):
   # print "In standardization rule=",rule
    localVarMap={}  #Changed localVarMap from local to standardize definition to global
    print "Counter=",counter


    for i in range(len(rule)):
        if isCompound(rule[i]):
            x_op,x_args=getArgsOp(rule[i])
            tmp=x_op+"("
            if isinstance(x_args,list):
                for j in range(len(x_args)):
                    if isVariable(x_args[j]):
                        if localVarMap.get(x_args[j]) is None:
                            localVarMap.__setitem__(x_args[j],x_args[j]+str(counter.next()))
                        x_args[j]=localVarMap.get(x_args[j])
                    print "localVarMap=",localVarMap,x_args[j],localVarMap.get(x_args[j])

                    if j==len(x_args)-1:
                        tmp=tmp+x_args[j]+')'
                    else:
                        tmp=tmp+x_args[j]+", "
            else:
                if isVariable(x_args):
                    if localVarMap.get(x_args) is None:
                        localVarMap.__setitem__(x_args,x_args+str(counter.next()))
                    x_args=localVarMap.get(x_args)
                tmp=tmp+x_args+')'

            rule[i]=tmp
    return rule




def getRhsLhs(rule):
    if len(rule)==1:
        return rule[0],[]
    else:
        return rule[len(rule)-1],rule[0:len(rule)-1]



def subst(theta,x):
    #print "In subst",theta,x
    if isCompound(x):
        x_op,x_arg=getArgsOp(x)
        #print "xargs=",x_arg
        tmp="("
        if isinstance(x_arg,list):
            for i in range(len(x_arg)):
                getval=theta.get(x_arg[i])
                if getval is None:
                    getval=x_arg[i]
                if i==len(x_arg)-1:

                    tmp=tmp+getval+')'
                else:
                    tmp=tmp+getval+', '
        else:
            getval=theta.get(x_arg)
            if getval is None:
                tmp=tmp+x_arg+')'
            else:
                tmp=tmp+getval+')'
        #print "in After Subst:",tmp
    return x_op+tmp


def fol_bc_and(KB,goals,theta):
    global tempqry,ruleLength,notPrint
    print "In And Goal==",goals," Theta==",theta
    if theta==Failure:
        if notPrint==False and ruleLength==0:
            if OutputArray[len(OutputArray)-1]<>['False',tempqry]:#ruleLength==0:
                OutputArray.append(['False',tempqry])
        return
    elif len(goals)==0:
        yield theta
    else:
        first,rest=goals[0],goals[1:]
        sub=subst(theta,first)
        for theta1 in fol_bc_or(KB,sub,theta):
            for theta2 in fol_bc_and(KB,rest,theta1):
                yield theta2


"""
def fol_bc_and1(KB, goals, theta, goal):
	global strOuputPreviously
	global strPrintPreviously
	global queriesAskedSoFar
	if theta is None:
		pass
	elif not goals:
		goal = subst(theta, goal)
		strGoal = "%s" %(goal)
		strPrintReady = replaceVarByScore(goal)
		print "True: %s" %(strGoal)
		OutputArray.append(["True",strPrintReady])
		strPrintPreviously = strGoal
		strOuputPreviously = strPrintReady

		yield theta
	else:
		first, rest = goals[0], goals[1:]
		strFirst = "%s" %(first)
        print "Goals=",goals,"first=",first
        sen = subst(theta, first)
        for arg in sen.args:
            if arg in theta:
                sen = subst(theta, sen)
		strSen = "%s" %(sen)
        thetas = fol_bc_or(KB, sen, theta)
        for theta1 in thetas:
			hasItGotSomeValues = True
			thetasForAND = fol_bc_and(KB, rest, theta1, goal)
			for theta2 in thetasForAND:
				yield theta2

"""

def fol_bc_or(KB,goal,theta):
    global tempqry,ruleLength,QryAskdSoFar
    qryPrint=replaceVarByScore(goal)

    if len(OutputArray)==0:
        OutputArray.append(['Ask',subst(theta,goal)])
        QryAskdSoFar.append(qryPrint)
    else:
        if OutputArray[len(OutputArray)-1][1]<>subst(theta,goal):
            OutputArray.append(['Ask',subst(theta,goal)])
            QryAskdSoFar.append(qryPrint)

    ruleLength=len(fetchRulesForGoals(KB,goal))
    if ruleLength==0:
        if OutputArray[len(OutputArray)-1][1]<>['False',subst(theta,goal)]:
            OutputArray.append(['False',subst(theta,goal)])
    for rules in fetchRulesForGoals(KB,goal):
        notPrint=False
        ruleLength=ruleLength-1

        rule=standardize(rules)
        rhs,lhs=getRhsLhs(rule)
        tempqry=subst(theta,goal)


        """if len(OutputArray)-1>0:
            if OutputArray[len(OutputArray)-1][1]<>subst(theta,goal) :
                OutputArray.append(['Ask',subst(theta,goal)])
        else:
            OutputArray.append(['Ask',subst(theta,goal)])"""
        if OutputArray[len(OutputArray)-1][1]<>subst(theta,goal) :
            if replaceVarByScore(tempqry) in QryAskdSoFar:
                thetaUnify=unify(rhs,goal,theta)
                print "thetaUnify=",thetaUnify,goal,replaceVarByScore(tempqry)
                if thetaUnify <> "False":
                    OutputArray.append(['Ask',subst(theta,goal)])
                    QryAskdSoFar.append(replaceVarByScore(tempqry))
                else:
                    notPrint=True
            else:
                OutputArray.append(['Ask',subst(theta,goal)])
                QryAskdSoFar.append(replaceVarByScore(tempqry))
        print "!!!!QryAskedSoFar=",QryAskdSoFar
        for theta1 in fol_bc_and(KB,lhs,unify(rhs,goal,theta)):
            if theta1.__contains__(Failure)==False:
                OutputArray.append(['True',subst(theta1,goal)])
            tmpgoal=subst(theta,goal)
            if chkQryToStp==tmpgoal:
                yield theta1
                raise StopIteration

            print "Theta1 BC OR=",theta1

            yield theta1


"""
def fol_bc_or1(KB, goal, theta):
    global strOuputPreviously
    global strPrintPreviously
    global queriesAskedSoFar
    strPrintReady = replaceVarByScore(goal)
    strGoal = "%s" %(goal)
    if strGoal != strPrintPreviously and strPrintReady != strOuputPreviously:
        print "Ask: %s" %(goal)
        OutputArray.append(['Ask',strPrintReady])
        queriesAskedSoFar.append(strPrintReady)
        strPrintPreviously = strGoal
        strOuputPreviously = strPrintReady


    rules = fetchRulesForGoals(KB,goal)
    for i in range(0, len(rules)):
        rule = rules[i]
        stdExpr = standardize(rule)
        lhs, rhs = getRhsLhs(rule)#parse_definite_clause(standardize_variables(rule))
        thetaBeforeAnd = unify(rhs, goal, theta)
        strGoal = "%s" %(goal)
        noNeedToPrintThisFalseStatement = False
        if not lhs:
            strPrintReady = replaceVarByScore(goal)
            strGoal = "%s" %(goal)
            if strGoal != strPrintPreviously and strPrintReady != strOuputPreviously:
                if strPrintReady in queriesAskedSoFar:
                    thetaUnify = unify(rhs, goal, theta)
                    if thetaUnify is not None:
                        print "Ask: %s" %(goal)
                        OutputArray.append(['Ask',strPrintReady])
                        queriesAskedSoFar.append(strPrintReady)
                        strPrintPreviously = strGoal
                        strOuputPreviously = strPrintReady
                    else:
                        noNeedToPrintThisFalseStatement = True
                else:
                    print "Ask: %s" %(goal)
                    OutputArray.append(['Ask',strPrintReady])
                    queriesAskedSoFar.append(strPrintReady)
                    strPrintPreviously = strGoal
                    strOuputPreviously = strPrintReady

        thetasBeforeAND = fol_bc_and(KB, lhs, thetaBeforeAnd, goal)
        hasItGotSomeValues = False
        for theta1 in thetasBeforeAND:
            hasItGotSomeValues = True
            goal = subst(theta, goal)
            strGoal = "%s" %(goal)
            if strGoal == chkQryToStp:
                yield theta1
                raise StopIteration
            yield theta1
        if hasItGotSomeValues == False:
            if i == len(rules)-1:
                thetaUnify = unify(rhs, goal, theta)
                unsubGoal = copy.deepcopy(goal)
                if noNeedToPrintThisFalseStatement == False:
                    goal = subst(theta, goal)
                    strPrintReady = replaceVarByScore(goal)
                    strGoal = "%s" %(goal)
                    print "False: %s" %(goal)
                    OutputArray.append(["False:",strPrintReady])
                    strPrintPreviously = strGoal
                    strOuputPreviously = strPrintReady
                    queriesFalseSoFar.append(strPrintReady)
            else:
                strPrintReady = replaceVarByScore(goal)
                strGoal = "%s" %(goal)
                if strGoal != strPrintPreviously and strPrintReady != strOuputPreviously:
                    print "Ask: %s" %(goal)
                    OutputArray.append(['Ask',strPrintReady])
                    queriesAskedSoFar.append(strPrintReady)
                    strPrintPreviously = strGoal
                    strOuputPreviously = strPrintReady
"""


def fol_bc_ask(KB,query):
    return fol_bc_or(KB,query,{})


def replaceVarByScore(x):
    if isCompound(x):
        x_op,x_args=getArgsOp(x)
        tmp=x_op+'('
        if isinstance(x_args,list):
            for i in range(len(x_args)):
                if isVariable(x_args[i]):
                    x_args[i]='_'
                if i==len(x_args)-1:
                    tmp=tmp+x_args[i]+')'
                else:
                    tmp=tmp+x_args[i]+', '
        else:
            if isVariable(x_args):
                x_args='_'
            tmp=tmp+str(x_args)+')'
        return tmp
    return x
QryAskdSoFar=[]
strOuputPreviously = ""
strPrintPreviously = ""

queriesAskedSoFar=[]
queriesFalseSoFar=[]
KB=[]
Qry=[]
OutputArray=[]
readFile()
Failure='False'
query=[]
ruleLength=0
chkQryToStp=""
tempqry=""
FinalOutDecide='True'
notPrint=False

if Qry.find('&&'):
    query=Qry.split(' && ')
else:
    query.append(Qry)


for i in range(len(query)):
    chkQryToStp=query[i]
    print "chkQryToStp=",query[i]
    if FinalOutDecide=='True':
        t=fol_bc_ask(KB,query[i])
        for k in t:
            print "from bc ask",k
    else:
        break
    if len(OutputArray)==0:
        OutputArray.append(["Ask",query[i]])

    FinalOutDecide=OutputArray[len(OutputArray)-1][0]

    if FinalOutDecide not in ('True','False'):
        FinalOutDecide ='False'

    x_op,x_args=getArgsOp(OutputArray[len(OutputArray)-1][1])
    y_op,y_args=getArgsOp(query[i])
    if x_op<>y_op or OutputArray[len(OutputArray)-1][0] not in ('False','True'):
        OutputArray.append([FinalOutDecide,query[i]])

printarray(OutputArray)

outputFile="output.txt"
txt=open(outputFile,'w')
for i in range(len(OutputArray)):
    tmp=""
    tmp=tmp+str(OutputArray[i][0])+": "+replaceVarByScore(OutputArray[i][1])
    txt.write(tmp+"\n")
txt.write(FinalOutDecide)
txt.close()

