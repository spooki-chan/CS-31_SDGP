$(function () {
	$("#style").selectmenu();
});

$(function () {
	$("#type").selectmenu();
});

$(function () {
	$( "#recipe" )
      .selectmenu()
      .selectmenu( "menuWidget" )
        .addClass( "overflow" );
	
});

$(function () {
	$("#slider-range").slider({
		range: true,
		min: 0,
		max: 600,
		values: [75, 350],
		slide: function (event, ui) {
			$("#amount").val(ui.values[0] + "-" + ui.values[1]);
		}
	});

	$("#amount").val($(" #slider-range").slider("values", 0) + " - " + $("#slider-range").slider("values", 1));
});


$(function () {
	$("#Search").on("click", function () {

		var recstyle = $("#style").val();
		var recipename = $("#recipe").val();
		var rectype = $("#type").val();
		var mincal = $("#slider-range").slider("option", "values")[0];
		var maxcal = $("#slider-range").slider("option", "values")[1];
  //for (var i in data.recipes)
		var output = "<ul>";
		for (var i in data.recipes) {
			if ((recstyle == data.recipes[i].style) || (recstyle == "Any"))
				if ((recipename == data.recipes[i].name) || (recipename == "Any"))
				if ((rectype == data.recipes[i].type) || (rectype == "Any"))
					if ((data.recipes[i].calorie >= mincal && data.recipes[i].calorie <= maxcal)) {
						{
							{
								{
									output += "<h2><li>" + data.recipes[i].name + "</li></h2>" + "<img src=" + data.recipes[i].picture + ">" + "<p>" + data.recipes[i].description + "</p>" + "<p class=" + data.recipes[i].name + "><button id='addFavoirite'>Add to Favourite</button></p>";
									
								}
							}
						}
					}
				
					// $("#addFavoirite").on("click", function () {


					// 	alert("hello");
					// 	var test = $(this).closest("p").attr("class");
					// 	console.log(test);



					

					// });
		}
		output += "</ul>";
		document.getElementById("Placeholder").innerHTML = output;
		$("#addFavoirite").on("click", function () {


			alert("hello");
			var test =recipename ;
			console.log(test);





		});// $("#addFavoirite").on("click", function () {


		// 	alert("hello");
		// 	var test = $(this).closest("p").attr("class");
		// 	console.log(test);





		// });
	});
});







