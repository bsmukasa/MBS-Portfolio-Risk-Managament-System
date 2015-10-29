$(document).ready(function(){

	//Get portfolios
	$.get( "/portfolio/get_portfolios", function( data ) {
		var temp_string, template;
		temp_string = "";
		template = $("#portfolio-load-script").html();

		data.portfolios.forEach(function (portfolio, index) {
			console.log(portfolio);
			
			temp_string += helperFunctions.mustacheLoad(template, portfolio);
			
		});

		$("#portfolio-load").html(temp_string);


	});
	
	

});


var helperFunctions = {
	mustacheLoad: function(template, data) {
		var data, template, informationToLoad;
		data = data || {};
		informationToLoad = Mustache.render(template, data);
		return informationToLoad	
	}
}
