import re;
import PorterStemmer1;

P=PorterStemmer1.PorterStemmer1()

def removeStopWords(featureList):

    listOfStopWords=["", "-", "!", ",", ".", ":",
                     "a", "able", "about", "all", "also", "am", "an", "and", "any", "as", "are", "at",
                     "be", "before", "bit", "but", "by",
                     "can",
                     "did", "do"
                     "etc", "even",
                     "find", "for", "from",
                     "get", "go",
                     "have", "had", "he", "her", "him", "hotel", "how",
                     "i", "if", "in", "is", "it", "its",
                     "make", "me", "my",
                     "of", "on", "only", "or", "our",
                     "so",
                     "than", "that", "the", "their", "there", "these", "they", "things", "this", "to", "too",
                     "you", "youll", "your",
                     "us", "up",
                     "was", "want", "we", "were", "what", "when", "where", "which", "whom", "why", "will", "with", "who"]
    deleteCount=0





    for i in range(len(featureList)):
        featureList[i-deleteCount]=re.sub('[^a-zA-Z ]','',featureList[i-deleteCount] )
        if P.stem(featureList[i-deleteCount].lower(), 0, len(featureList[i-deleteCount].lower())-1) in listOfStopWords or str(featureList[i-deleteCount]).isdigit() or featureList[i-deleteCount].lower().strip() in listOfStopWords :

            featureList.remove(featureList[i-deleteCount])
            deleteCount=deleteCount+1
        else:

            featureList[i-deleteCount]=P.stem(featureList[i-deleteCount].lower(), 0, len(featureList[i-deleteCount].lower())-1);
    return featureList
