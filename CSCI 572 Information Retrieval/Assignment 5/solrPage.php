<?php

error_reporting(E_ALL);
ini_set('display_errors', 1);

// make sure browsers see this page as utf-8 encoded HTML
header('Access-Control-Allow-Origin: *'); 
header('Access-Control-Allow-Methods: *');
header('Access-Control-Allow-Headers: *');
header('Content-Type: text/html; charset=utf-8');

ini_set('max_execution_time', 300);

include 'SpellCorrector.php';




//For getting the corrected spelling
function spell_correct($query){
	$wordArr = explode(" ", $query);
	$correctedWord = "";
	for($x = 0 ; $x< sizeof($wordArr) ; $x++)
		$correctedWord .= SpellCorrector::correct($wordArr[$x])." ";

	return trim($correctedWord);
}
//Spell Correction End



//For Snippet Generation
function getSnippet($file_name, $inQuery){
	$file = file_get_contents($file_name);
	$newDoc = new DOMDocument();
	$text = '';
	libxml_use_internal_errors(true);
	$newDoc->loadHTML($file);
	//First search the meta tags for snippets
	foreach($newDoc->getElementsByTagName('meta') as $meta) {
		if (strpos(strtolower($meta->getAttribute('name')), "desc" ) !== false || strpos(strtolower($meta->getAttribute('property')), "desc" ) !== false) {
			if (substr($text, -1) == '.')
				$text = $text.$meta->getAttribute('content');
			else{
				$text = $text.'.'.$meta->getAttribute('content');
			}
		}
	}
	//Second search the paragraph tag for snippet
	foreach($newDoc->getElementsByTagName('p') as $paragraph) {
		if (substr($text, -1) == '.')
			$text = $text.$paragraph->nodeValue;
		else{
			$text = $text.'.'.$paragraph->nodeValue;
		}
	}

	
	$sentences = explode('.',$text);
	$sentence_count_array = [];
	$inQuery_words = explode(' ',strtolower($inQuery));

	foreach($sentences as $sentence){
		//echo $sentence;
		//echo "1 "." ".$inQuery.strpos(strtolower($sentence),strtolower($inQuery));
		$count = array_reduce(
				array_map(
					function($value) use ($sentence){
						return array_count_values(str_word_count(strtolower($sentence), 1))[strtolower($value)] ?? 0;
					} , 
					$inQuery_words
				),
				function($count1, $count2){
					return $count1 + $count2;
				}, 
				0
			);
		$sentence_count_array[] = [$sentence,$count];
//		echo count($sentence_count_array).":".$sentence." . " .$count." " .(strpos(strtolower($sentence),strtolower($inQuery)) ? 'true' : 'false')." : ".strtolower($sentence). ":".strtolower($inQuery)."<br>";
		if ($count == count($inQuery_words))
			break;
	}
	
	//To get the most matching at the top
	usort($sentence_count_array, function($a, $b) {
		if($b[1] == $a[1]){
//			echo $b[1] . ":" . $a[1];
			return strlen($a[0]) <=> strlen($b[0]);
		}
		else{
//			echo $b[1] . ":" . $a[1];
			return $b[1] <=> $a[1];
		}
	
	});
	
/*	echo '<script language="javascript">';
	echo 'console.log($sentence_count_array)';
	echo '</script>';
*/
//	echo $sentence_count_array[0][0].":".$sentence_count_array[0][1];
	if(empty($sentence_count_array) || empty($sentence_count_array[0]) || strlen($sentence_count_array[0][0])<1 || $sentence_count_array[0][1]<1)
		return "No snippet found";
	else{
		if(str_word_count($sentence_count_array[0][0])<3){
			$pstn = strpos(strtolower($text), strtolower($sentence_count_array[0][0]));
			$st_pstn = max(0, $pstn - 30);
			$end_pstn = min(strlen($text), $pstn + strlen($sentence_count_array[0][0]) + 30);            
			$snippet = substr($text, $st_pstn, $end_pstn - $st_pstn); 
//			$snippet=substr($text,$inQuery);
			}
		else{
			$snippet = $sentence_count_array[0][0];
//			echo "1 ". $sentence_count_array[0][0];
//			echo $text;
//			echo "2 ". $sentence_count_array[0][1];
//			echo "3 ". $sentence_count_array[0][2];
		}

		return preg_replace("/\b".implode('|',$inQuery_words)."\b/i", '<b>$0</b>', $snippet)." ...";
	}
}
//End of Snippet Generation


$limit = 10;
$query = isset($_REQUEST['q']) ? $_REQUEST['q'] : false;
$results = false;
$sort=isset($_REQUEST['indexType']) ? $_REQUEST['indexType'] : false;

//For handling indexes without site link
$hashmap = array();
if (($handle = fopen("/home/ankit/solr-6.5.0/NYTimesData/mapNYTimesDataFile.csv", "r")) !== FALSE) {
	while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) 
		$hashmap[$data[0]] = $data[1]; 

  fclose($handle);
}


if ($query)
{
	//maintain actual query so that it can be displayed in did you mean part
	//$oldQuery=$query;
	$CorrectedQuery=spell_correct($query);

	// The Apache Solr Client library should be on the include path
	// which is usually most easily accomplished by placing in the
	// same directory as this script ( . or current directory is a default
	// php include path entry in the php.ini)
	require_once('/home/ankit/solr-6.5.0/solr-php-client/Apache/Solr/Service.php');
	$solr = new Apache_Solr_Service('localhost', 8983, '/solr/nytimes');

	// if magic quotes is enabled then stripslashes will be needed
	if (get_magic_quotes_gpc() == 1){
		$CorrectedQuery = stripslashes($CorrectedQuery);
	}

	try{
		$additionalParameters =array('sort'=>'pageRankFile desc');
		if ($sort =='lucene')
		$results = $solr->search($CorrectedQuery, 0, $limit);

		else
		$results = $solr->search($CorrectedQuery, 0, $limit, $additionalParameters);

	}
	catch (Exception $e){
	// in production you'd probably log or email this error to an admin
	// and then show a special message to the user but for this example
	// we're going to show the full exception
		die("<html><head><title>SEARCH EXCEPTION</title><body><pre>{$e->__toString()}</pre></body></html>");
	}
}

?>


<html>
  	<head>
    		<title>PHP Solr Client Example</title>
		        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
			<link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css">
			<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
			<script type="text/javascript" src="autosuggest.js"></script>

  	</head>
  	<body>
	    

    	<form  accept-charset="utf-8" method="get">
      		<label for="q">Search:</label>
		<input id="q" name="q" type="text" value="<?php echo htmlspecialchars($query, ENT_QUOTES, 'utf-8'); ?>"/><br>
                <input type="radio" id="indexType" name="indexType" value="lucene" <?php if((isset($_REQUEST['indexType']) && $_REQUEST['indexType'] == 'lucene')) echo ' checked="checked"';?> > Lucene

                <input type="radio" id="indexType" name="indexType" value="pageRank desc" <?php if((isset($_REQUEST['indexType']) && $_REQUEST['indexType'] == 'pageRank desc')) echo ' checked="checked"';?> > PageRank<br>

      		<input type="submit"/>
    	</form>


<?php

// display results
if ($results){
	$total = (int) $results->response->numFound;
	$start = min(1, $total);
	$end = min($limit, $total);
?>
	<div><?php 
	if (strtolower($query) != strtolower($CorrectedQuery)){
		echo "Showing results for <b>".$CorrectedQuery ."</b> instead of <b>". $query ."</b>";
	};?></div><br>

	<div>Results <?php echo $start; ?> - <?php echo $end;?> of <?php echo $total; ?>:</div>

	<ol>
		<?php
		// iterate result documents
		foreach ($results->response->docs as $doc){
		?>
			<li>

				<?php if($doc->og_url == null) {
						$tempExplode=explode('/', $doc->id);
						$end = end($tempExplode);
						$doc->og_url = $hashmap[$end];
					}
				?>

				<a href="<?php echo htmlspecialchars($doc->og_url, ENT_NOQUOTES, 'utf-8'); ?>"><?php echo htmlspecialchars($doc->title, ENT_NOQUOTES, 'utf-8'); ?></a> &nbsp&nbsp&nbsp <a href="<?php echo htmlspecialchars($doc->og_url, ENT_NOQUOTES, 'utf-8'); ?>"> [<?php
					 $idArray=explode("/", $doc->id); 
	    				 $onlyId=$idArray[sizeof($idArray)-1];
					 echo htmlspecialchars($onlyId, ENT_NOQUOTES, 'utf-8'); ?>]</a><br>

				<a  href="<?php echo htmlspecialchars($doc->og_url, ENT_NOQUOTES, 'utf-8'); ?>" style="color: green; font-size=9px;"><?php echo htmlspecialchars($doc->og_url, ENT_NOQUOTES, 'utf-8'); ?></a><br>

				<?php

					// Call snippet method of php
					$snip=getSnippet($doc->id,$CorrectedQuery);
					echo $snip; 
				
				?><br><br>


			</li>
		<?php
		}
		?>
	</ol>
	<?php
}
?>
</body>
</html>
