$(function(){

$( "#q" ).autocomplete({
              source: function(request, response)
              { 

                var tempInput = $("#q").val().split(" ");
                var input = tempInput.pop().toLowerCase();
                var prev = "";
                for (var i = 0; i< tempInput.length; i++) {
                  prev = prev+tempInput[i] + " ";
                  }
                console.log(input);

                $.ajax({

                  url :  "http://localhost:8983/solr/nytimes/suggest?indent=on&q="+input.toLowerCase()+"&wt=json",
                  dataType: "json",
                  data: input,
                  success: function(data)
                  {

                  	var list  = [];

                    response($.map(data.suggest.suggest[input].suggestions,(function(arrdata)
                    {
                      if((arrdata.term).toLowerCase() !== input)
                      {
                        if(!/[@.~`_!#$%\^&*+=\-\[\]\\"\\'\;,\/{}|:<>\?]/g.test(arrdata.term)){
                    	list.push(prev + arrdata.term);
                    }
                  }
                      })));
                    response(list)
                  }
                });
              },

              minLength: 1
            });

});
