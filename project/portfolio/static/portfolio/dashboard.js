$(document).ready(function(){

	//Standard on page load, tab active is portfolios
	tabLoaderFunctions.portfolioTabLoader();

//................................................................................................................................................	
	//PORTFOLIO TABS

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
		tabLoaderFunctions.assumptionsTabLoader();
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


//................................................................................................................................................
	//PORTFOLIO TAB

	//Upload new portfolio
	$('#main-content').on('submit',"#save-upload-csv", function(event) {
		event.preventDefault();
		var data = new FormData($('#save-upload-csv').get(0));
		$.ajax({
    		url: '/portfolio/get_portfolios',
    		type: 'POST',
	    	data: data,
	    	cache: false,
	    	processData: false,
	    	contentType: false,
    		success: function(data) {
    			if (data.status == "OK") {
    				$(this).modal('hide');
    				$('body').removeClass('modal-open');
    				$('.modal-backdrop').remove();

    				tabLoaderFunctions.portfolioTabLoader();

    			}
    		}
		});
	})



//................................................................................................................................................
	//RISK PROFILE TAB

	//Risk Profiles & Risk Factors table  >>  View risk factors by profiles selected
	$('#main-content').on('click', '#view-risk', function() {
		var selected_ids = helperFunctions.getTableSelections('#user-risk-profiles');
		var table_data = [];

		selected_ids.forEach(function (id, index) {
			$.get( "/risk_management/get_risk_factors", {'risk_profile_id': id}, function(data) {
				var risk_factor_list = data.risk_factors;
				for (var idx in risk_factor_list) {
					table_data.push(risk_factor_list[idx]);
				}
				$("#user-risk-details").bootstrapTable('refresh', {
					data: [{"attribute": "", "changing_assumption": "", "percentage_change": ""}]
				})
				helperFunctions.updateTableData("#user-risk-details", table_data);
			})
		})	
	})

	//Popover with Risk Conditionals
	$('#main-content').on('click-row.bs.table', '#user-risk-details', function(event, row, $element) {
		$.get( "/risk_management/get_risk_factor_conditionals", {'risk_factor_id': row.id}, 
			function( return_data ) {

				$($element).popover({
					trigger: 'manual',
					placement: 'left',
					content: 'TEST'
				})
				$($element).popover('show');

		})

	})

	//Save new risk profile name
	$('#main-content').on('submit',"#new-risk-profile-name", function(event) {
		event.preventDefault();
		var data = $("#new-risk-profile-name").serialize();
		$.post("/risk_management/create_risk_profile", data, function(return_data) {
			if (return_data.status == 'OK') {

			}
		})		
	});
		



	

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
				portfolio.average_loan_balance = parseFloat(portfolio.average_loan_balance).formatNumberSeparator(2);
				portfolio.weighted_average_coupon = parseFloat(portfolio.weighted_average_coupon * 100).formatNumberSeparator(3);
				portfolio.weighted_average_life_to_maturity = parseFloat(portfolio.weighted_average_life_to_maturity).formatNumberSeparator(2);
				
				temp_string += helperFunctions.getMustacheHTMLString(template, portfolio);
			});
			$("#portfolio-load").html(temp_string);
		});
	},

	riskProfileTabLoader: function() {		
		helperFunctions.mustacheLoad("#riskProfile-template", "#main-content-load");
		helperFunctions.mustacheLoad("#risk-tables-template", "#risk-profiles-table-load");

		$.get( "/risk_management/get_risk_profiles", function( return_data ) {
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
	},

	assumptionsTabLoader: function() {
		helperFunctions.mustacheLoad("#assumptions-template", "#main-content-load");
		helperFunctions.mustacheLoad("#assumptions-table-template", "#assumptions-table-load");

		$.get( "/risk_management/get_assumption_profiles", function( return_data ) {
			$(function () {
				if (return_data.assumption_profiles.length > 0) {
					helperFunctions.displayTableData('#user-assumptions-table', return_data.assumption_profiles)
				}
				else {
					helperFunctions.displayTableData('#user-assumptions-table', [{"name": ""}])
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





