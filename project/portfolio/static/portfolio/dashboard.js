$(document).ready(function(){

	//Standard on page load, tab active is portfolios
	tabLoaderFunctions.portfolioTabLoader();

//................................................................................................................................................	
	//GENERAL TABS 

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
		tabLoaderFunctions.scenariosTabLoader();
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



	//TO DO!!!!
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
				$('.modal-backdrop').remove();
				var new_risk_profile_data = return_data.new_risk_profile;
				helperFunctions.mustacheLoad("#riskProfile-creation-template", "#main-content-load", new_risk_profile_data);
				var empty_factor_data = [{"attribute": "", "changing_assumption": "", "percentage_change": ""}];
				helperFunctions.displayTableData("#risk-factors-edit-table", empty_factor_data);
				var empty_conditional_data = [{"conditional": "", "value":""}];
				helperFunctions.displayTableData("#all-conditionals-table", empty_conditional_data);
			}
		})		
	});
		

	//Complete new attribute form based on attribute selection
	$('#main-content').on('change',"#select-risk-factor-attribute", function() {
		var selected_attribute = $("#select-risk-factor-attribute").val();
		$.get("/risk_management/factor_attribute", {"attribute": selected_attribute}, function(return_data) {
			var return_choices = return_data.attribute_choices
			var choices_array = [];
			if (return_choices.length > 0) {
				for (var k in return_choices) {
					choices_array.push(return_choices[k][0]);	
				}
				helperFunctions.mustacheLoad("#empty-conditionals", "#range-conditionals-loader");
				helperFunctions.mustacheLoad("#equal-choices-conditionals", "#equal-conditionals-loader", choices_array);
			}
			else {
				helperFunctions.mustacheLoad("#empty-conditionals", "#equal-conditionals-loader");
				helperFunctions.mustacheLoad("#range-conditionals", "#range-conditionals-loader");
			}
		})
	});


	//Save new attribute
	$('#main-content').on('submit', "#new-risk-factor", function(event) {
		event.preventDefault();

		var risk_profile_id = $(".risk-profile-name-id").attr("id");
		$('<input />').attr('type','hidden')
			.attr('name', "risk_profile_id")
			.attr('value', risk_profile_id)
			.appendTo('#new-risk-factor');

		var formData = $("#new-risk-factor").serialize();
		$.post("/risk_management/add_risk_factor", formData, function(return_data) {
			if (return_data.status == "OK") {
				$.get("/risk_management/get_risk_factors", {"risk_profile_id": risk_profile_id}, function(return_data) {
					helperFunctions.removeModal("#new-factor-modal");
					var data = return_data.risk_factors;
					helperFunctions.updateTableData("#risk-factors-edit-table", data);
				})
			}
		})
	})


	//View risk attribute conditionals
	$('#main-content').on('click', '#view-conditional', function() {
		var selected_ids = helperFunctions.getTableSelections('#risk-factors-edit-table');
		var table_data = [];

		selected_ids.forEach(function (id, index) {
			$.get( "/risk_management/risk_factor_conditionals", {"risk_factor_id": id}, function(data) {
				var attribute_conditionals = data.risk_conditionals;
				for (var idx in attribute_conditionals) {
					table_data.push(attribute_conditionals[idx])	
				}
				helperFunctions.updateTableData("#all-conditionals-table", table_data);
			})
		})	
	})
	


//................................................................................................................................................
	//ASSUMPTIONS TAB

	//Create new assumption
	$('#main-content').on('submit',"#form-new-assumption", function(event) {
		event.preventDefault();
		var form_data = $("#form-new-assumption")
		$.ajax({
    		url: '/risk_management/assumption_profile',
    		type: 'POST',
	    	data: form_data.serialize(),
    		success: function(data) {
    			if (data.status == "OK") {
  		  			$(this).modal('hide');
    				$('body').removeClass('modal-open');
    				$('.modal-backdrop').remove();
    				tabLoaderFunctions.assumptionsTabLoader();
    			}
    		}
    	})
	})


	//View selected assumption
	$('#main-content').on('click', '#view-assumption', function() {
		var selected_assumption = helperFunctions.getTableSelections('#assumptions-table');
		$.get("/risk_management/assumption_profile", {"id": selected_assumption[0]}, function(return_data) {
			var assumption_details = return_data.assumption_profiles[0];
			helperFunctions.mustacheLoad("#assumptions-details-script", "#assumption-details-loader", assumption_details);
		})
	})


//................................................................................................................................................
//$document closing
});


//===============================================================================================================================================
//Global helper functions
var helperFunctions = {

	//Return mustache string to be applied in html (params: template selector and data to be inserted)
	getMustacheHTMLString: function(template, data) {
		var data, template, informationToLoad;
		data = data || {};
		informationToLoad = Mustache.render(template, data);
		return informationToLoad	
	},
	
	//Loads mustache template (params: script selector, loader selector and data to be inserted)
	mustacheLoad: function(script_selector, loader_selector, data) {
		var data, template, informationToLoad;
		data = data || {};
		template = $(script_selector).html();
		informationToLoad = Mustache.render(template, data);
		$(loader_selector).html(informationToLoad);
	}, 

	//Get items selected in a table (params: table selector)
	getTableSelections: function(table_selector) {
		var data = $(table_selector).bootstrapTable('getSelections');
		var selected_ids = $.map(data, function(item) {
			return item.id;
		})
		return selected_ids;
	},

	//Activate bootstrap table (params: table selector, table data(eg: [{number: 1}])
	displayTableData: function(table_selector, table_data) {
		$(table_selector).bootstrapTable({ data: table_data })
	},

	//Update values on bootstrap table (params: table selector, table data(eg: [{number: 1}])
	updateTableData: function(table_selector, table_data) {
		$(table_selector).bootstrapTable( 'load', { data: table_data })
	},

	//Removes modal background (params: modal selector)
	removeModal: function(modal_selector) {
  		$(modal_selector).modal('hide');
		$('body').removeClass('modal-open');
		$('.modal-backdrop').remove();		
	}
}


//Function to load each tab on dashboard page
var tabLoaderFunctions = {

	//Portfolio tab
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

	//Risk Profile tab
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

	//Assumptions tab
	assumptionsTabLoader: function() {
		helperFunctions.mustacheLoad("#assumptions-template", "#main-content-load");

		$.get( "/risk_management/assumption_profile", function( return_data ) {
			$(function () {
				if (return_data.assumption_profiles.length > 0) {
					helperFunctions.displayTableData('#assumptions-table', return_data.assumption_profiles);
				}
				else {
					helperFunctions.displayTableData('#assumptions-table', [{"name": ""}]);
		    	}
		    	helperFunctions.mustacheLoad("#assumptions-details-script", "#assumption-details-loader");
	    	});
		});
	},

	//Scenarios tab
	scenariosTabLoader: function () {
		helperFunctions.mustacheLoad("#scenarios-template", "#main-content-load");
		helperFunctions.displayTableData('#scenario-risk-profiles-table', [{"name": ""}]);

		//TODO >> get user's scenarios (Scenarios API not done)
		

	}
}


//Formating numbers: 100,000,000.55
Number.prototype.formatNumberSeparator = function(n, x) {
	var re = '\\d(?=(\\d{' + (x || 3) + '})+' + (n > 0 ? '\\.' : '$') + ')';
	return this.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, 'g'), '$&,');
}


//RISK PROFILE PAGE >> Show risk factor details when clicking "+"
function detailFormatter(index, row) {
    var html = [];
    $.each(row, function (key, value) {
    	if (key == "id") {
			$.ajax({
	    		url: "/risk_management/risk_factor_conditionals",
	    		type: 'GET',
		    	data: {"risk_factor_id": value},
		    	async: false,
		    	success: function(data) {
		    		var conditional_result = data.risk_conditionals;
		    		for (var idx in conditional_result) {
    					obj_conditional = conditional_result[idx];
    					html.push('<p><b>' + 'Conditional' + ':</b> ' + '  ' + obj_conditional['conditional'] + '  ' + obj_conditional['value']);
    				}
    			}
    		})
		}
	})
    return html.join('');
}


//Loading animations according to ajax functionality
$(document).on({
    ajaxStart: function() { $("body").addClass("loading"); },
    ajaxStop: function() { $("body").removeClass("loading"); }    
});

