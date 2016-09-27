function y =NaiveBayesGaussian_HW1_5b()
filename = 'train.txt';
train = csvread(filename);
filename = 'test.txt';
test = csvread(filename);

% Clear temporary variables
clearvars predictGlasswithY predictGlasswithoutY trainGlasswithY trainGlasswithoutY filename delimiter formatSpec fileID dataArray ans;



%% Get Class value whihc is column no 11.
% Get mean, variance and probability for each class
glassList=train(:,11,:);

for i=1:7
    keyIndex=(glassList==i);
    glass=train(keyIndex,:);
    mean1(i,:)=mean(glass());
    var1(i,:)=var(glass());
    countY(i,:)=size(glass);
end


%% Test Data
for i=1:18
    for k=1:7
        prob=1;
        for j=2:10
            prob=prob*((1/sqrt(2*pi*var1(k,j)))*(exp(-power(test(i,j)-mean1(k,j),2)/(2*var1(k,j)))));
        end
            predictGlasswithoutY(i,k)=prob;
            predictGlasswithY(i,k)=prob*(countY(k,1)/(sum(countY(:,1))));
            
    end
     [val,idx]=max(predictGlasswithY(i,:));
     %Get predicted class value
     predictGlasswithY(i,10)=idx;
     %Get expected class value
     predictGlasswithY(i,11)=test(i,11);
     %For accuracy check predicted=expected
     predictGlasswithY(i,12)=predictGlasswithY(i,10)==predictGlasswithY(i,11);
end   

disp('Test Accuracy=');
disp(100*sum(predictGlasswithY(:,12,:)/18))

%Training data

for i=1:196
    for k=1:7
        prob=1;
        for j=2:10
            prob=prob*((1/sqrt(2*pi*var1(k,j)))*(exp(-power(train(i,j)-mean1(k,j),2)/(2*var1(k,j)))));
        end
            trainGlasswithoutY(i,k)=prob;
            trainGlasswithY(i,k)=prob*(countY(k,1)/(sum(countY(:,1))));
            
    end
     [val,idx]=max(trainGlasswithY(i,:));
     %Get predicted class value
     trainGlasswithY(i,10)=idx;
     %Get expected class value
     trainGlasswithY(i,11)=train(i,11);
     %For accuracy check predicted=expected
     trainGlasswithY(i,12)=trainGlasswithY(i,10)==trainGlasswithY(i,11);
end   

disp('Train Accuracy=');
disp(100*sum(trainGlasswithY(:,12,:)/196))
end