function knn=KNN_HW1_5c()
%% test 
filename = 'train.txt';
train = csvread(filename);
filename = 'test.txt';
test = csvread(filename);
%% Get Mean, and std

%Train data set
Knn_Mean=mean(train(:,2:10));
Knn_Std=std(train(:,2:10));
NormTrain=bsxfun(@minus,train(:,2:10),Knn_Mean);
NormTrain=bsxfun(@rdivide,NormTrain,Knn_Std);

% Test data set
NormTest=bsxfun(@minus,test(:,2:10),Knn_Mean);
NormTest=bsxfun(@rdivide,NormTest,Knn_Std);
%NormTrain=train(:,2:10)
%NormTest=test(:,2:10)

%% Calculate the Knn matrix for manhattan and euclidian distance (L1, L2)
for i=1:196;
   for j=1:196;
       if i == j;
           Knn2MatrixTrain(i,j)=NaN;
           Knn1MatrixTrain(i,j)=NaN;
       else
           Knn2MatrixTrain(i,j)=sqrt(sum((NormTrain(i,:)-NormTrain(j,:)).^ 2));
           Knn1MatrixTrain(i,j)=sum(abs(NormTrain(i,:)-NormTrain(j,:)));
       end;
       
   end;
end;


for i=1:18;
   for j=1:196;
           Knn2MatrixTest(i,j)=sqrt(sum((NormTest(i,:)-NormTrain(j,:)).^ 2));
           Knn1MatrixTest(i,j)=sum(abs(NormTest(i,:)-NormTrain(j,:)));
   end;
end;

K=[1,3,5,7];
for i=1:length(K);
    OutputK2Test(i,:)=KnnFunction(Knn2MatrixTest,train,test,K(i));
    OutputK1Test(i,:)=KnnFunction(Knn1MatrixTest,train,test,K(i));
    OutputK2Train(i,:)=KnnFunction(Knn2MatrixTrain,train,train,K(i));
    OutputK1Train(i,:)=KnnFunction(Knn1MatrixTrain,train,train,K(i));
end


disp('++++++++++++++++++++++++Test Result++++++++++++++++++++++++');
disp('For L2');
disp('"K" "SampleClassified" "Total Sample" "Accuracy"');
disp(OutputK2Test)
disp('For L1');
disp('"K" "SampleClassified" "Total Sample" "Accuracy"');
disp(OutputK1Test)
disp('++++++++++++++++++++++++Train Result++++++++++++++++++++++++');
disp('For L2');
disp('"K" "SampleClassified" "Total Sample" "Accuracy"');
disp(OutputK2Train)
disp('For L1');
disp('"K" "SampleClassified" "Total Sample" "Accuracy"');
disp(OutputK1Train)
end