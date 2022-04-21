$(function() {
	$("#style").selectmenu();
});

$(function() {
  $("#type").selectmenu();
});



$(function() {
  $("#slider-range").slider({
	  range:true,
	  min: 0,
	  max: 600,
	  values: [ 75, 350 ],
	  slide: function( event, ui ){
		  $("#amount").val(  ui.values[ 0 ] + "-" + ui.values[ 1 ] );
	  }
  });
  
  $("#amount").val( $(" #slider-range").slider( "values", 0 ) + " - " + $("#slider-range").slider( "values", 1 ) );
});


$(function() {
  $( "#Search" ).on("click", function(){
	  
	  var recstyle = $("#style").val();
	  var rectype = $("#type").val();
	  var mincal = $("#slider-range").slider("option", "values")[0];
	  var maxcal = $("#slider-range").slider("option", "values")[1];
	  
	  var output="<ul>";
		 for (var i in data.recipes) {
			 if (( recstyle == data.recipes[i].style) || (recstyle=="Any"))
			 if (( rectype == data.recipes[i].type) || (rectype=="Any"))
			 if (( data.recipes[i].calorie >= mincal && data.recipes[i].calorie <= maxcal ))
			 
		  
		   
			
			 {
				 {
					 {
						 {
							 output+="<h2><li>" + data.recipes[i].name +"</li></h2>" + "<img src=" + data.recipes[i].picture + ">"+"<p>"+ data.recipes[i].calorie + "</p>" + "<button><a href='" + data.recipes[i].url + "'>Visit Page</a></button><hr>";
						 } } } } }
			  output+="</ul>";
			  document.getElementById( "Placeholder" ).innerHTML = output;
		 });
  });
