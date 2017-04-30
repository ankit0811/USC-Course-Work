import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class ExternalLinks {
	public static void main(String args[]) throws Exception {
		Map<String, String> HMUrlToId = new HashMap<String, String>();
		Map<String, String> HMIdToUrl = new HashMap<String, String>();
		BufferedReader br = null;
		String line = "";
		String cvsSplitBy = ",";

		br = new BufferedReader(new FileReader("/home/ankit/solr-6.5.0/NYTimesData/mapNYTimesDataFile.csv"));
		while ((line = br.readLine()) != null) {

			// use comma as separator
			String[] words = line.split(cvsSplitBy);
			String url = words[1].trim();
			String id = words[0].trim();
			HMUrlToId.put(url, id);
			HMIdToUrl.put(id, url);

		}
		br.close();
		//System.out.println(HMUrlToId.toString());
		//System.out.println(HMIdToUrl.toString());
		
		
		
		File dir = new File("/home/ankit/solr-6.5.0/NYTimesData/NYTimesDownloadData/");
		Set<String> edges=new HashSet<String>();
		
		for (File file: dir.listFiles()){
		//	System.out.println("file="+file.getName());
		//	System.out.println("HashMap Value="+HMIdToUrl.get(file.getName()));
			
			Document doc = Jsoup.parse(file, "UTF-8", HMIdToUrl.get(file.getName()));
			Elements links = doc.select("a[href]");

			print("\nLinks: (%d)", links.size());
			for (Element src : links) {
				if (HMUrlToId.get(src.attr("abs:href")) != null)
					edges.add((file.getName().toString()+" "+ HMUrlToId.get(src.attr("abs:href"))));
			}

		}
		
		
		BufferedWriter bw = null;
		FileWriter fw = null;
		fw = new FileWriter("edgeList.txt");
		bw = new BufferedWriter(fw);
		
		for (String s: edges){
			bw.write(s);
			bw.newLine();
		}
		
		bw.close();
	}
	

	

	private static void print(String msg, Object... args) {
		System.out.println(String.format(msg, args));
	}

	private static String trim(String s, int width) {
		if (s.length() > width)
			return s.substring(0, width + 1);
		else
			return s;
	}

}