$(document).ready(function(){

	//Standard on page load, tab active is portfolios
	tabLoaderFunctions.portfolioTabLoader();


	
	//Click on Portfolio TAB
	$('#dashboard-tabs a[href="#portfolios"]').click(function (event) {
		event.preventDefault()
		$(this).tab('show')
		tabLoaderFunctions.portfolioTabLoader();

	})	

	//Click on Risk Profile TAB
	$('#dashboard-tabs a[href="#risk-profiles"]').click(function (event) {
		event.preventDefault()
		$(this).tab('show')
		tabLoaderFunctions.riskProfileTabLoader();
	})

	//Click on Economic Assumptions TAB
	$('#dashboard-tabs a[href="#economic"]').click(function (event) {
		event.preventDefault()
		$(this).tab('show')
	})	

	//Click on Global Scenarios TAB
	$('#dashboard-tabs a[href="#scenarios"]').click(function (event) {
		event.preventDefault()
		$(this).tab('show')
	})	

	//Click on Risk Scorecards TAB
	$('#dashboard-tabs a[href="#scorecards"]').click(function (event) {
		event.preventDefault()
		$(this).tab('show')
	})	


	//RISK PROFILE TAB JS

	//Risk Profiles table
	//View risk factors by profiles selected
	$('#main-content').on('click', '#view-risk', function() {
		var selected_ids = helperFunctions.getTableSelections('#user-risk-profiles');
		var table_data = [];

		selected_ids.forEach(function (id, index) {
			$.get( "/risk-management/risk_factors", {'risk_profile_id': id}, function(data) {
				var risk_factor_list = data.risk_factors;
				for (var idx in risk_factor_list) {
					table_data.push(risk_factor_list[idx]);
				}
				$("#user-risk-details").bootstrapTable('refresh', {
					data: [{"attribute": "1", "changing_assumption": "1", "percentage_change": "1"}]
				})
				helperFunctions.updateTableData("#user-risk-details", table_data);
			})
		})
		
	})

		


	


	//Upload CSV POST >> send JSON with name
	// $('#save-upload-csv').on("submit", function(event) {
	// 	event.preventDefault();
	// 	var data_toJson = $(this).serializeObject()
	// 	$.ajax({
	// 		url: "/portfolio/get_portfolios",
	// 		data: $(this).serialize(),
	// 		type: 'POST',
	// 		success: function( data ) {

	// 			console.log(data);


	// 			return True;
	// 		},
	// 		error : function(){
 //            $(this).html("Error!");
 //        	}
	// 	})
	// })

});



var helperFunctions = {
	getMustacheHTMLString: function(template, data) {
		var data, template, informationToLoad;
		data = data || {};
		informationToLoad = Mustache.render(template, data);
		return informationToLoad	
	},
	
	mustacheLoad: function(script_selector, loader_selector, data) {
		var data, template, informationToLoad;
		data = data || {};
		template = $(script_selector).html();
		informationToLoad = Mustache.render(template, data);
		$(loader_selector).html(informationToLoad);
	}, 

	getTableSelections: function(table_selector) {
		var data = $(table_selector).bootstrapTable('getSelections');
		var selected_ids = $.map(data, function(item) {
			return item.id;
		})
		return selected_ids;
	},

	displayTableData: function(table_selector, table_data) {
		$(table_selector).bootstrapTable({ data: table_data })
	},

	updateTableData: function(table_selector, table_data) {
		$(table_selector).bootstrapTable( 'load', { data: table_data })
	}
}



var tabLoaderFunctions = {
	portfolioTabLoader: function() {
		helperFunctions.mustacheLoad("#portfolio-template", "#main-content-load");
		$.get( "/portfolio/get_portfolios", function( data ) {	
			var temp_string, template;
			temp_string = "";
			template = $("#portfolio-load-script").html();
			data.portfolios.forEach(function (portfolio, index) {
				
				portfolio.total_loan_count = (portfolio.total_loan_count).formatNumberSeparator();
				portfolio.total_loan_balance = (portfolio.total_loan_balance).formatNumberSeparator(2);
				portfolio.average_loan_balance = (portfolio.average_loan_balance).formatNumberSeparator(2);
				portfolio.weighted_average_coupon = (portfolio.weighted_average_coupon * 100).formatNumberSeparator(3);
				portfolio.weighted_average_life_to_maturity = (portfolio.weighted_average_life_to_maturity).formatNumberSeparator();
				
				temp_string += helperFunctions.getMustacheHTMLString(template, portfolio);
			});
			$("#portfolio-load").html(temp_string);
		});
	},

	riskProfileTabLoader: function() {		
		helperFunctions.mustacheLoad("#riskProfile-template", "#main-content-load");
		helperFunctions.mustacheLoad("#risk-tables-template", "#risk-profiles-table-load");

		$.get( "/risk-management/get_risk_profiles", function( return_data ) {
			$(function () {
				if (return_data.risk_profiles.length > 0) {
					helperFunctions.displayTableData('#user-risk-profiles', return_data.risk_profiles)
				}
				else {
					helperFunctions.displayTableData('#user-risk-profiles', [{"name": ""}])
		    	}

		    	helperFunctions.displayTableData('#user-risk-details', 
		    		[{"attribute": "", "changing_assumption": "", "percentage_change": ""}])
	    	});
		});
	}
}


Number.prototype.formatNumberSeparator = function(n, x) {
	var re = '\\d(?=(\\d{' + (x || 3) + '})+' + (n > 0 ? '\\.' : '$') + ')';
	return this.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, 'g'), '$&,');
}


$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();

    console.log(this);
    console.log(a);

    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};





