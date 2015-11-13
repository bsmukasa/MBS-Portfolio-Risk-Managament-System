$(document).ready(function(){

	//Page load >> default is Overview
	navMenu.overviewSection();


//GENERAL NAVitems	
//................................................................................................................................................	
	//Overview
	$('#portfolio-nav a[href="#overview"]').click(function (event) {
		event.preventDefault();
		navMenu.overviewSection();
	})

	//Loans
	$('#portfolio-nav a[href="#loans"]').click(function (event) {
		event.preventDefault();
		navMenu.loansSection();
	})

	//Analysis
	$('#portfolio-nav a[href="#analysis"]').click(function (event) {
		event.preventDefault();
		navMenu.analysisSection();
	})


//ANALYTICS TABS	
//................................................................................................................................................	
	//Summary
	$("#portfolio-content").on("click", "#analysis-tabs-list a[href='#summary']", function (event) {
		event.preventDefault();
		$(this).tab('show')
		analyticsTab.summaryTab();
	})

	//Cash flows
	$("#portfolio-content").on("click", "#analysis-tabs-list a[href='#cash-flow']", function (event) {
		event.preventDefault();
		$(this).tab('show')
		analyticsTab.cashFlowTab();
	})

	//Graphs
	$("#portfolio-content").on("click", "#analysis-tabs-list a[href='#graphs']", function (event) {
		event.preventDefault();
		$(this).tab('show')
		analyticsTab.summaryTab();
	})


//LOANS NAV SECTION
//................................................................................................................................................	
	//Pagination control
	$("#portfolio-content").on('page-change.bs.table', "#all-loans-table", function(e, number, size) {
		var options = $("#all-loans-table").bootstrapTable('getOptions');
		var send_data = {
			"portfolio_id": globalVariable.portfolio_id, 
			limit: (options.pageNumber * options.pageSize),
			offset: options.pageSize
		};
		$.get("/portfolio/all_loans", send_data, function (data) {
			$("#all-loans-table").bootstrapTable('load', data);
		})
	})


//ANALYSIS NAV SECTION
//................................................................................................................................................	
	//Scenario selection
	$("#portfolio-content").on('page-change.bs.table', "#all-loans-table", function(e, number, size) {
		var options = $("#all-loans-table").bootstrapTable('getOptions');
		var send_data = {
			"portfolio_id": globalVariable.portfolio_id, 
			limit: (options.pageNumber * options.pageSize),
			offset: options.pageSize
		};
		$.get("/portfolio/all_loans", send_data, function (data) {
			$("#all-loans-table").bootstrapTable('load', data);
		})
	})

	//Send scenario and discount rate to run calculations model
	$("#portfolio-content").on('submit', "#form-analysis-criteria", function (event) {
		event.preventDefault();

		var buttonText = $("#run-scenario-btn").text()

		if (buttonText == "RUN") {
			$('#select-scenario-analysis').prop("disabled", true);
			$('#discount-rate').prop('readonly', true);
			$("#run-scenario-btn").text('New scenario');

			var send_data = {
				portfolio_id: globalVariable.portfolio_id,
				scenario_id: $("#select-scenario-analysis").val(),
				discount_rate: $("#discount-rate").val()
			}

			$.post("/analytics/analyze_portfolio", send_data, function (data) {
				if (data.status == "PASS") {
					helperFunctions.mustacheLoad("#analysis-tabs", "#analysis-results");
					analyticsTab.summaryTab();
				}
			})

		} else {
			$('#select-scenario-analysis').prop("disabled", false);
			$('#discount-rate').prop('readonly', false);
			$("#run-scenario-btn").text('RUN');
		}
	})


//Analytics tabs	
//................................................................................................................................................	



//$document closing
//................................................................................................................................................
});


//Loading animations according to ajax functionality
//===============================================================================================================================================
$(document).on({
    ajaxStart: function() { $("body").addClass("loading");    },
    ajaxStop: function() { $("body").removeClass("loading"); }    
});



//Global variables
//===============================================================================================================================================
globalVariable = {
	portfolio_id: window.location.pathname.split('/')[3], 
}


//Functions to load NAV Menu
//===============================================================================================================================================
navMenu = {

	//Overview section load
	overviewSection: function() {
		helperFunctions.mustacheLoad("#portfolio-overview-script", "#portfolio-content");
		$.get("/portfolio/port_loans_status", {"portfolio_id": globalVariable.portfolio_id}, function (data) {
			helperFunctions.displayTableData("#status-summary-table", data.data);
		})
		$.get("/portfolio/fico_summary", {"portfolio_id": globalVariable.portfolio_id}, function (data) {
			helperFunctions.displayTableData("#fico-summary-table", data.data);
		})
	},

	//Loans section load
	loansSection: function() {
		helperFunctions.mustacheLoad("#loans-script", "#portfolio-content");

		$("#all-loans-table").bootstrapTable({
			height: 700,
			url: "/portfolio/all_loans",
			method: 'GET',
			queryParams: function (params) {
				return {"portfolio_id": globalVariable.portfolio_id, limit: params.limit, offset: params.offset};
			},
			cache: true,
			striped: true,
			pagination: true,
			sidePagination: 'server',
			pageSize: 30,
			pageList: "[20, 100, 200, 500]",
			search: false,
			showColumns: false,
			clickToSelect: false,
			uniqueId: "id",
			columns: [
				{
					field: 'state',
					checkbox: true,
					align: 'center',
					valign: 'middle',
				}, {
					field: 'bank_loan_id',
					title: 'Loan ID',
					align: 'center',
					sortable: false,
				}, {
					field: 'property_type_code',
					title: 'Property Type',
					align: 'center',
					sortable: false,				
				}, {
					field: 'occupancy_code',
					title: 'Occupancy',
					align: 'center',
					sortable: false,
				}, {
					field: 'product_type',
					title: 'Product Type',
					align: 'center',
					sortable: false,
				}, {
					field: 'purpose',
					title: 'Purpose',
					align: 'center',
					sortable: false,
				}, {
					field: 'mortgage_type',
					title: 'Mortgage Type',
					align: 'center',
					sortable: false,
				}, {
					field: 'lien_position',
					title: 'Lien Position',
					align: 'center',
					sortable: false,
				}, {
					field: 'original_rate',
					title: 'ORATE',
					align: 'center',
					sortable: false,
				}, {
					field: 'original_appraisal_amount',
					title: 'Original Appraisal Amount',
					align: 'center',
					sortable: false,
				}, {
					field: 'original_date',
					title: 'Origination Date',
					align: 'center',
					sortable: false,
				}, {
					field: 'first_payment_date',
					title: 'First Payment Date',
					align: 'center',
					sortable: false,
				}, {
					field: 'original_term',
					title: 'Original Term',
					align: 'center',
					sortable: false,
				}, {
					field: 'remaining_term',
					title: 'Remaining Term',
					align: 'center',
					sortable: false,
				}, {
					field: 'amortized_term',
					title: 'Amortized Term',
					align: 'center',
					sortable: false,
				}, {
					field: 'pmi_insurance',
					title: 'PMI',
					align: 'center',
					sortable: false,
				}, {
					field: 'city',
					title: 'City',
					align: 'center',
					sortable: false,
				}, {
					field: 'us_state',
					title: 'State',
					align: 'center',
					sortable: false,
				}, {
					field: 'zipcode',
					title: 'Zipcode',
					align: 'center',
					sortable: false,
				}, {
					field: 'fico',
					title: 'FICO',
					align: 'center',
					sortable: false,
				}, {
					field: 'gross_margin',
					title: 'Gross Margin',
					align: 'center',
					sortable: false,
				}, {
					field: 'lcap',
					title: 'LCap',
					align: 'center',
					sortable: false,
				}, {
					field: 'lfloor',
					title: 'LFloor',
					align: 'center',
					sortable: false,			
				}, {
					field: 'icap',
					title: 'ICap',
					align: 'center',
					sortable: false,
				}, {
					field: 'pcap',
					title: 'PCap',
					align: 'center',
					sortable: false,
				}, {
					field: 'IO_term',
					title: 'IO Term',
					align: 'center',
					sortable: false,
				}, {
					field: 'interest_reset_interval',
					title: 'Interest Reset Interval',
					align: 'center',
					sortable: false,
				}, {
					field: 'reset_index',
					title: 'Reset Index',
					align: 'center',
					sortable: false,
				}, {
					field: 'first_index_rate_adjustment_date',
					title: '1st Interest Rate Adjustment Date',
					align: 'center',
					sortable: false,	
				}, {
					field: 'first_recast_or_next_recast',
					title: '1st Recast/Next Recast',
					align: 'center',
					sortable: false,	
				}, {
					field: 'recast_frequency',
					title: 'Recast Frequency',
					align: 'center',
					sortable: false,	
				}, {
					field: 'recast_cap',
					title: 'Recast Cap',
					align: 'center',
					sortable: false,	
				}, {
					field: 'negam_initial_minimum_payment_period',
					title: 'Negam Initial Minimun Payment Period',
					align: 'center',
					sortable: false,	
				}, {
					field: 'negam_payment_reset_frequency',
					title: 'Negam Payment Reset Frequency',
					align: 'center',
					sortable: false,	
				}, {
					field: 'status',
					title: 'status',
					align: 'center',
					sortable: false,	
				}, {
					field: 'deferred_balance',
					title: 'Deferred Balance',
					align: 'center',
					sortable: false,
				}, {
					field: 'modification_date',
					title: 'Modification Date',
					align: 'center',
					sortable: false,	
				}, {
					field: 'foreclosure_referral_date',
					title: 'Foreclosure Referral Date',
					align: 'center',
					sortable: false,	
				}, {
					field: 'current_property_value',
					title: 'Current Property Value',
					align: 'center',
					sortable: false,	
				}, {
					field: 'current_value_date',
					title: 'Current Value Date',
					align: 'center',
					sortable: false,	
				}, {
					field: 'current_principal_balance',
					title: 'Current Principal Balance',
					align: 'center',
					sortable: false,					
				}, {
					field: 'current_interest_rate',
					title: 'Current Interest Rate',
					align: 'center',
					sortable: false,					
				}, {
					field: 'last_payment_received',
					title: 'Last Payment Received',
					align: 'center',
					sortable: false,					
				}, {
					field: 'current_FICO_score',
					title: 'Current FICO',
					align: 'center',
					sortable: false,					
				}, {
					field: 'BK_flag',
					title: 'BK Flag',
					align: 'center',
					sortable: false,					
				}, {
					field: 'MSR',
					title: 'MSR',
					align: 'center',
					sortable: false,					
				}, {
					field: 'senior_lien_balance',
					title: 'Senior Lien Balance',
					align: 'center',
					sortable: false,					
				}, {
					field: 'senior_lien_balance_date',
					title: 'Senior Lien Balance Date',
					align: 'center',
					sortable: false,					
				}, {
					field: 'second_lien_piggyback_flag',
					title: '2nd Lien Piggyback Flag',
					align: 'center',
					sortable: false,					
				}, {
					field: 'junior_lien_balance',
					title: 'Junior Lien Balance',
					align: 'center',
					sortable: false,					
				}, {
					field: 'junior_lien_balance_date',
					title: 'Junior Lien Balance',
					align: 'center',
					sortable: false,					
				}, {
					field: 'SF',
					title: 'SF',
					align: 'center',
					sortable: false,
				}
			]
		});
	},

	//Analysis section load
	analysisSection: function () {
		$.get("/risk_management/scenarios", function (data) {
			helperFunctions.mustacheLoad("#analysis-script", "#portfolio-content", data);
		})
	}

}


//Functions to load ANALYTICS TABS
//===============================================================================================================================================
analyticsTab = {

	//Load summary tab
	summaryTab: function () {
		//TODO >> get data and load script
		// $.get("URL ROUTE", {"portfolio_id": globalVariable.portfolio_id}, function (data) {
		// 	LOAD MUSTACHE WITH DATA
		// })

		//DELETE LATER
		var testData = {
			price: "1,500,000",
			npv: "100,0000,000",
			total_remaining_balance: "87,000,440.90",
			yield: "5.4",
			wa_avg_life: "278",
			assumption_cpr: "7.8",
			wa_cpr: "6.5",
			assumption_cdr: "13.5",
			wa_cdr: "9.95",
			assumption_recovery: "77.90",
			wa_recovery: "65"
		}
		helperFunctions.mustacheLoad("#summary-tab", "#analysis-tab-content", testData)
	},

	//Load cash flows tab
	cashFlowTab: function () {
		var send_data = {
			"portfolio_id": globalVariable.portfolio_id,
			"scenario_id": $("#select-scenario-analysis").val(),
			"discount_rate": $("#discount-rate").val()
		}
		$.get("/analytics/get_aggregate_cash_flows", send_data, function (data) {
			//GETTING AN ERROR WHEN EXECUTING DJANGO VIEW
		})
		//GET CASH FLOWS
		// helperFunctions.mustacheLoad("#cash-flow-tab", "#analysis-tab-content", data)
	}
}


//Global helper functions
//===============================================================================================================================================
helperFunctions = {

	//Loads mustache template (params: script selector, loader selector and data to be inserted)
	mustacheLoad: function(script_selector, loader_selector, data) {
		var data, template, informationToLoad;
		data = data || {};
		template = $(script_selector).html();
		informationToLoad = Mustache.render(template, data);
		$(loader_selector).html(informationToLoad);
	},

	//Activate bootstrap table (params: table selector, table data(eg: [{number: 1}])
	displayTableData: function(table_selector, table_data) {
		$(table_selector).bootstrapTable({ data: table_data });
	},

	//Update values on bootstrap table (params: table selector, table data(eg: [{number: 1}])
	updateTableData: function(table_selector, table_data) {
		$(table_selector).bootstrapTable( 'load', { data: table_data })
	}
}























