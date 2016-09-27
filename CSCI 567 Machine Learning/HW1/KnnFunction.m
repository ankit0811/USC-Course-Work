function f=KnnFunction(KnnDataSet,DataSet,ActualOut,K)
    clearvars ResultTest;
	for i=1:size(KnnDataSet,1);
%    for i=4:4
        clearvars minValues,modeVal=[0,0,0,0,0,0,0];chkList=0;
        l=1;
        temp2=KnnDataSet(i,:);
        for k=1:K
            [val,idx]=min(KnnDataSet(i,:));
            KnnDataSet(i,idx)=Inf;
            minValues(l,1)=val;
            minValues(l,2)=DataSet(idx,11);
            modeVal(DataSet(idx,11))=modeVal(DataSet(idx,11))+1;
            minValues(l,3)=idx;
            l=l+1;
            
        end
        KnnDataSet(i,:)=temp2;
        temp2=0;
        maxVal=max(modeVal);
        modeValList=(modeVal==maxVal);
        i1=1;
        for m=1:length(modeValList);
           if modeValList(m)==1
              chkList(i1,1)=m;
              i1=i1+1;
           end
        end
        t=ismember(minValues(:,2,:),chkList);
        test1=minValues(t,1);
        
        val=min(minValues(t,1));
        [val, idx] = ismember(val, minValues(:,1,:));
        ResultTest(i,1)=ActualOut(i,11);
        ResultTest(i,2)=minValues(idx,2);
        ResultTest(i,3)=(ResultTest(i,2)==ResultTest(i,1));
        
    end
    f=[K,sum(ResultTest(:,3)),size(ResultTest,1),100*sum(ResultTest(:,3))/size(ResultTest,1)];
end