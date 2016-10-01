import numpy as np;
import heapq;
import matplotlib.pyplot as plt;

#Normalizing the matrix
def normalize(matrix,mean,std):
    for i in range(len(matrix)):
        matrix[i]=(matrix[i]-mean)/std;


def getMSE(predict,actual):
    sum=0.0
    for i in range(len(predict)):
        sum=sum+pow((actual[i]-predict[i]),2)/len(predict)
    return sum

#Using Analytical method
def getWeights(x,y):
    temp1=x.transpose().dot(x) # (xT * x)
    temp2=np.linalg.inv(temp1) # Inv(xT * x)
    temp3=temp2.dot(x.transpose()) # Inv(xT * x) * xT
    return temp3.dot(y); # Inv(xT * x) * xT * y


def getWeightsRidge(x,y,lambdas):
    regularization=lambdas * np.eye(np.size(x,1))
    temp1=x.transpose().dot(x) + regularization # (xT * x) + lambda||w||
    temp2=np.linalg.inv(temp1) # Inv(xT * x)
    temp3=temp2.dot(x.transpose()) # Inv(xT * x) * xT
    return temp3.dot(y); # Inv(xT * x) * xT * y



np.set_printoptions(precision=15,suppress=True);
data=np.array(np.genfromtxt("DataHw2.txt"));

test_x=np.zeros(shape=(len(data)/7+1,13));
train_x=np.zeros(shape=(len(data)-len(test_x),13));

test_y=np.zeros(shape=(len(data)/7+1,1));
train_y=np.zeros(shape=(len(data)-len(test_y),1));

print(data[0,13])
k=0;l=0;
for i in range(len(data)):
        #print i,i%7
        if i%7==0:
            test_x[k]=data[i,0:13];
            test_y[k]=data[i][13];
            k=k+1;
        else:
            train_x[l]=data[i,0:13];
            train_y[l]=data[i][13];
            l=l+1;

#Pearson correlation
print "\n*********Pearson Correlation*********\n"
PearsCorr=np.zeros(shape=(13,1))
for i in range(len(train_x[0])):
    PearsCorr[i]= np.corrcoef(train_x[:,i],train_y[:,0])[0][1]
    print "Corr for attr x(",i,"):",PearsCorr[i]


mean=np.zeros(shape=(13));
std=np.zeros(shape=(13));

for i in range(len(train_x[1])):
    mean[i]=train_x[:,i].mean();
    std[i]=train_x[:,i].std();


#Normalize Train and Test data set using mean and std of Train
normalize(train_x,mean,std);
normalize(test_x,mean,std);


#Add 1 as a bias for w0 in train and test
train_x_bias=np.insert(train_x,0,1,axis=1)
test_x_bias=np.insert(test_x,0,1,axis=1)
#computing W-lms =inv(xT * x) * xT * y
weightsTrain=getWeights(train_x_bias,train_y)
predictTrain_y=train_x_bias.dot(weightsTrain)
MSETrain=getMSE(predictTrain_y,train_y)
print "MSE for Training(LR):", MSETrain

predictTest_y=test_x_bias.dot(weightsTrain)
MSETest=getMSE(predictTest_y,test_y)
print "\n*********    MSE    *********\n"
print "MSE for Testing(LR) :", MSETest
#Ridge regression with fixed lambda
l=[0.01,0.1,1.0]
for i in range(len(l)):
    RidgeWeights=getWeightsRidge(train_x_bias,train_y,l[i]);
    predictTrain_y=train_x_bias.dot(RidgeWeights)
    MSETrain=getMSE(predictTrain_y,train_y)
    print "MSE for Training(Ridge Regressor lambda= ",l[i],"):", MSETrain
    predictTest_y=test_x_bias.dot(RidgeWeights)
    MSETest=getMSE(predictTest_y,test_y)
    print "MSE for Testing (Ridge Regressor lambda= ",l[i],"):", MSETest

#Ridge with diff lambda values
'''binRowNos=np.zeros(shape=(44,10))
data_i=0;
"""for i in range(len(binRowNos)):
    for j in range(10):
        if (data_i>=len(train_x)):
            binRowNos[i][j]=-999;
        else:
            binRowNos[i][j]=data_i;
        data_i=data_i+1;
"""

for j in range(10):
    for i in range(len(binRowNos)):
        if (j>=3 and i >= len(binRowNos)-1 ):
            binRowNos[i][j]=-999;
        else:
            binRowNos[i][j]=data_i;
            data_i=data_i+1;


print binRowNos
#exit(1)
#train_x_ridge=train_x[binRowNos[0]]
tryLambda=0.0001
incr=0;
diffLambdaMSE=[];
while (tryLambda <= 10.0):
    MSETest=0#np.zeros(shape=(10,1))
    MSETrain=0#np.zeros(shape=(10,1))

    for j in range(10):
        cv_x_ridge=np.zeros(shape=(44,13))-999
        cv_y_ridge=np.zeros(shape=(44,1))-999
        train_x_ridge=np.zeros(shape=(433,13))-999
        train_y_ridge=np.zeros(shape=(433,1))-999

        k=0;
        l=0;

        for i in range(len(train_x)):
            if (k< len(binRowNos) and i==binRowNos[k][j] and binRowNos[k][j]!=-999):
                cv_x_ridge[k]=train_x[i];
                cv_y_ridge[k]=train_y[i];
                k=k+1;
            else:
                train_x_ridge[l]=train_x[i];
                train_y_ridge[l]=train_y[i];
                l=l+1;


        train_x_bias=np.insert(train_x_ridge[0:l-1],0,1,axis=1)
        #print train_x_ridge,len(train_x_ridge),len(train_x_ridge[1]),"%%%%%%%%%%%",train_x_bias,len(train_x_bias),len(train_x_bias[1])
        #print train_x_ridge[300:]
        RidgeWeights=getWeightsRidge(train_x_bias,train_y_ridge[0:l-1],tryLambda);
        predictTrain_y=train_x_bias.dot(RidgeWeights)
        TrainMSE=getMSE(predictTrain_y,train_y_ridge[0:l-1]);
        MSETrain=MSETrain+TrainMSE
        #print "for j=",j,"TrainMSE=",TrainMSE

        test_x_bias=np.insert(cv_x_ridge[0:k-1],0,1,axis=1)
        predictTest_y=test_x_bias.dot(RidgeWeights)
        TestMSE=getMSE(predictTest_y,cv_y_ridge[0:k-1]);
        MSETest=MSETest+TestMSE
        #print "TestMSE=",TestMSE


    print "For lambda=",tryLambda, " Avg train MSE=" , MSETrain/10, MSETest/10
    #exit(1)
    tryLambda=tryLambda+0.5
    #print "tryLambda=",tryLambda

#exit(1)

tryLambda=0.0001
incr=0;
diffLambdaMSE=[];
while (tryLambda <=10):
    RidgeWeights=getWeightsRidge(train_x_bias,train_y,tryLambda);
    predictTrain_y=train_x_bias.dot(RidgeWeights)
    MSETrain=getMSE(predictTrain_y,train_y)
    #print "MSE for Training(Ridge Regressor lambda= ",l[i],"):", MSETrain
    predictTest_y=test_x_bias.dot(RidgeWeights)
    MSETest=getMSE(predictTest_y,test_y)
    diffLambdaMSE.append([incr,tryLambda,MSETrain[0],MSETest[0]])
    incr=incr+1;
    tryLambda=tryLambda+0.5

print diffLambdaMSE[:][0];
x=[]
y=[]
for i in range(len(diffLambdaMSE)):
    x.append(diffLambdaMSE[i][0])
    y.append(diffLambdaMSE[i][2])
print x,y
plt.scatter(x,y)
'''


# Section 3 Feature Selection
#*******************      a      *******************#
maxIdx=heapq.nlargest(4, range(len(PearsCorr)), abs(PearsCorr).take)
featureTrain_x_a=train_x[:,maxIdx]
featureTest_x_a=test_x[:,maxIdx]

#Add 1 as a bias for w0 in train and test
featureTrain_x_bias=np.insert(featureTrain_x_a,0,1,axis=1)
featureTest_x_bias=np.insert(featureTest_x_a,0,1,axis=1)
#computing W-lms =inv(xT * x) * xT * y
weightsTrain=getWeights(featureTrain_x_bias,train_y)
predictTrain_y=featureTrain_x_bias.dot(weightsTrain)
MSETrain=getMSE(predictTrain_y,train_y)
#print "MSE for 4 features Training(LR):", MSETrain

predictTest_y=featureTest_x_bias.dot(weightsTrain)
MSETest=getMSE(predictTest_y,test_y)
#print "MSE for 4 features Testing(LR) :", MSETest

print "\n*********Feature Selection a.*********\nTop 4 features\n"
for i in range(len(maxIdx)):
    print "Feature No",maxIdx[i]+1, "with corr value as ",PearsCorr[maxIdx[i]]
print "Training LR MSE:",MSETrain
print "Testing LR MSE:",MSETest



#*******************      b      *******************#
print "\n*********Feature Selection b.*********\n"
featuresSelectedTillNow=heapq.nlargest(1, range(len(PearsCorr)), abs(PearsCorr).take)

featureTrain_x_b=train_x[:,featuresSelectedTillNow]
featureTest_x_b=test_x[:,featuresSelectedTillNow]

#Add 1 as a bias for w0 in train and test
featureTrain_xb_bias=np.insert(featureTrain_x_b,0,1,axis=1)
featureTest_xb_bias=np.insert(featureTest_x_b,0,1,axis=1)
#computing W-lms =inv(xT * x) * xT * y
weightsTrain=getWeights(featureTrain_xb_bias,train_y)
predictTrain_yb=featureTrain_xb_bias.dot(weightsTrain)
MSETrain=getMSE(predictTrain_yb,train_y)
print "MSE for 1 features",[val+1 for val in featuresSelectedTillNow],"Training(LR):", MSETrain
residual_b=train_y-predictTrain_yb


AllFeaturesForResidualCorr=range(13);
for i in range(3):
    dictCorr={};

    for ftr in featuresSelectedTillNow:
        #print "$$$",featuresSelectedTillNow,ftr,AllFeaturesForResidualCorr
        if (ftr in AllFeaturesForResidualCorr):
            AllFeaturesForResidualCorr.remove(ftr);
    for j in AllFeaturesForResidualCorr:
        dictCorr[j]=abs(np.corrcoef(train_x[:,j],residual_b[:,0])[0][1])

    featuresSelectedTillNow.append(max(dictCorr.iteritems(), key=lambda k: k[1])[0])
    featureTrain_x_b=train_x[:,featuresSelectedTillNow]
    featureTest_x_b=test_x[:,featuresSelectedTillNow]
    #print featureTrain_x_b
    #Add 1 as a bias for w0 in train and test
    featureTrain_xb_bias=np.insert(featureTrain_x_b,0,1,axis=1)
    #computing W-lms =inv(xT * x) * xT * y
    weightsTrain=getWeights(featureTrain_xb_bias,train_y)
    predictTrain_yb=featureTrain_xb_bias.dot(weightsTrain)
    MSETrain=getMSE(predictTrain_yb,train_y)

    featureTest_xb_bias=np.insert(featureTest_x_b,0,1,axis=1)
    predictTest_yb=featureTest_xb_bias.dot(weightsTrain)
    MSETest=getMSE(predictTest_yb,test_y)

    print "MSE for",i+2,"features", [val+1 for val in featuresSelectedTillNow],"Training(LR):", MSETrain,"Testing(LR):",MSETest
    residual_b=train_y-predictTrain_yb





#print AllFeaturesForResidualCorr
#print dictCorr


#******************* Brute Force *******************#
BruteForceDict={}
keyFeature=""
for i in range(len(train_x[0])):
    for j in range(i,len(train_x[0])):
        for k in range(j,len(train_x[0])):
            for l in range(k,len(train_x[0])):
                if (i<j and j<k and k<l ):
                    bruteForceIdx=[i,j,k,l]
                    #print len(train_x[0]),i,j,k,l
                    keyFeature=i,j,k,l
                    bruteForceTrain_x=train_x[:,bruteForceIdx]

                    #Add 1 as a bias for w0 in train and test
                    bruteForceTrain_x_bias=np.insert(bruteForceTrain_x,0,1,axis=1)
                    #computing W-lms =inv(xT * x) * xT * y
                    weightsTrain=getWeights(bruteForceTrain_x_bias,train_y)
                    bruteForcePredictTrain_y=bruteForceTrain_x_bias.dot(weightsTrain)
                    BruteForceDict[keyFeature]=getMSE(bruteForcePredictTrain_y,train_y)[0]
                    #print "MSE for 4 features Training(LR):", MSETrain

'''                 bruteForcePredictTest_y=bruteForceTest_x.dot(weightsTrain)
                    MSETest=getMSE(bruteForcePredictTest_y,test_y)
                    #print "MSE for 4 features Testing(LR) :", MSETest
'''
#print BruteForceDict

bruteForceFeatureSelected=min(BruteForceDict.iteritems(), key=lambda k: k[1])[0]
bruteForceTrainValue=min(BruteForceDict.iteritems(), key=lambda k: k[1])[1]
bruteForceTrain_x=train_x[:,bruteForceFeatureSelected]
bruteForceTrain_x_bias=np.insert(bruteForceTrain_x,0,1,axis=1)
bruteForceTest_x=test_x[:,bruteForceFeatureSelected]
bruteForceTest_x_bias=np.insert(bruteForceTest_x,0,1,axis=1)

#computing W-lms =inv(xT * x) * xT * y
weightsTrain=getWeights(bruteForceTrain_x_bias,train_y)

#print "MSE for 4 features Training(LR):", MSETrain

bruteForcePredictTest_y=bruteForceTest_x_bias.dot(weightsTrain)
MSETest=getMSE(bruteForcePredictTest_y,test_y)
print "\n\n********* Brute Force *********\n\nMSE for Brute Force features ",[group+1 for group in bruteForceFeatureSelected],"Training (LR):",bruteForceTrainValue,"Testing(LR) :", MSETest




#******************* Polynomial Feature Expansion *******************#
print "\n******************* Polynomial Feature Expansion *******************\n"
extraPolyFeaturesTrain=np.zeros(shape=(433,91))
extraPolyFeaturesTest=np.zeros(shape=(len(test_x),91))

l=0

for i in range(13):
    for j in range(i,13):
        extraPolyFeaturesTrain[:,l]=np.multiply(train_x[:,i],train_x[:,j])
        extraPolyFeaturesTest[:,l]=np.multiply(test_x[:,i],test_x[:,j])
        l=l+1;
print len(extraPolyFeaturesTest)

mean=np.zeros(shape=(len(extraPolyFeaturesTrain[0])));
std=np.zeros(shape=(len(extraPolyFeaturesTrain[0])));
for i in range(len(extraPolyFeaturesTrain[1])):
    mean[i]=extraPolyFeaturesTrain[:,i].mean();
    std[i]=extraPolyFeaturesTrain[:,i].std();

normalize(extraPolyFeaturesTrain,mean,std)

mean=np.zeros(shape=(len(extraPolyFeaturesTest[0])));
std=np.zeros(shape=(len(extraPolyFeaturesTest[0])));

for i in range(len(extraPolyFeaturesTest[1])):
    mean[i]=extraPolyFeaturesTest[:,i].mean();
    std[i]=extraPolyFeaturesTest[:,i].std();
normalize(extraPolyFeaturesTest,mean,std)

#print len(extraPolyFeaturesTrain),len(extraPolyFeaturesTrain[0]),len(extraPolyFeaturesTest),len(extraPolyFeaturesTest[0]),
train_x=np.hstack([train_x,extraPolyFeaturesTrain])
test_x=np.hstack([test_x,extraPolyFeaturesTest])

#print len(train_x),len(train_x[0]),len(test_x),len(test_x[0])

print len(test_x[0])
train_x_bias=np.insert(train_x,0,1,axis=1)
test_x_bias=np.insert(test_x,0,1,axis=1)

print len(test_x[0]),len(train_x[0]),len(test_x_bias[0])
#computing W-lms =inv(xT * x) * xT * y
weightsTrain1=getWeights(train_x_bias,train_y)
predictTrain_y1=train_x_bias.dot(weightsTrain1)
MSETrain1=getMSE(predictTrain_y1,train_y)
print "MSE for Training(LR):", MSETrain1
predictTest_y1=test_x_bias.dot(weightsTrain1)
MSETest1=getMSE(predictTest_y1,test_y)
print "MSE for Testing(LR) :",MSETest1
