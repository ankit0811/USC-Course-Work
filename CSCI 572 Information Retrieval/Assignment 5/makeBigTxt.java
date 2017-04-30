import java.io.*;
import java.util.*;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class makeBigTxt {
	public static void main(String args[]) throws IOException{
		File folder = new File("/home/ankit/solr-6.5.0/NYTimesData/NYTimesDownloadData");
		String regex = "[a-zA-Z]*[.]?";
		Writer fw = new FileWriter("/home/ankit/solr-6.5.0/big.txt");

		for(File file : folder.listFiles()){
			Document doc = Jsoup.parse(file, "UTF-8");
			String text = doc.body().text();
			String[] words = text.split(" ");

			for(String word : words){
				if(word.matches(regex)){
					if(words[words.length-1].length()==0)
						continue;
					if(word.charAt(word.length()-1) == '.')
						word = word.replaceAll("[.]", "");
					
					fw.write(word+" ");
				
				}
			}
		}
		fw.close();
	}
	
}