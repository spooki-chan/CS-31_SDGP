

    
    $(function() {
        $( ".addFavourites" ).on("click", function(){

            $(this).attr('disabled', true);
            var recipeID = $(this).closest("p").attr("id");
            var recipeName = $(this).closest("p").attr("class");
            console.log(recipeID);
            console.log(recipeName);

        });
    });