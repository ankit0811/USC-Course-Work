import java.io.IOException;
import java.util.*;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class InvertedIndexJob {
	public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException
	{
		if(args.length != 2)
		{
			System.err.println("Usage : Word Count <input path> <output path>");
			System.exit(-1);
		}
		@SuppressWarnings("deprecation")
		Job job =new Job();
	    job.setJarByClass(InvertedIndexJob.class);
	    
	    job.setJobName("InvertedIdx");
	    job.getConfiguration().set("mapreduce.output.textoutputformat.separator", " \t ");
	    FileInputFormat.addInputPath(job, new Path(args[0]));
	    FileOutputFormat.setOutputPath(job, new Path(args[1]));
	    job.setMapperClass(TokenizerMapper.class);
	    job.setReducerClass(IntSumReducer.class);
	    
	    job.setOutputKeyClass(Text.class);
	    job.setOutputValueClass(LongWritable.class);
	    
	    job.waitForCompletion(true);
	    
	  }
	
}

class IntSumReducer extends Reducer<Text,LongWritable,Text,Text>
{
	public void reduce(Text key, Iterable<LongWritable> values,Context context) throws IOException, InterruptedException 
    {
	    HashMap<Long,Long> hm=new HashMap<Long,Long>();
	    int sum = 0;
	    for (LongWritable val : values) {
            if(hm.containsKey(val.get()))
                hm.put(val.get(), hm.get(val.get())+1);
	    	else
                hm.put(val.get(), (long)1);
	      
            String s="";
            for (Map.Entry<Long, Long> entry : hm.entrySet()) 
                s=s+" "+entry.getKey()+":"+entry.getValue();
	    	  
            Text tt=new Text(s);
            context.write(key, tt);
	    }
}

class TokenizerMapper  extends Mapper<Object, Text, Text, LongWritable>
{

 
    private Text word = new Text();

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException 
    {
        String line =value.toString();
        StringTokenizer itr = new StringTokenizer(line);
        long docID=Long.parseLong(itr.nextToken());
        LongWritable one = new LongWritable(docID);
        
        while (itr.hasMoreTokens()) {
            word.set(itr.nextToken());
            context.write(word, one);
        }
    }
}