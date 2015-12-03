$(document).ready(function(){

	//Page load >> default is Overview
	navMenu.overviewSection();


//GENERAL NAVitems
//................................................................................................................................................	
	//Overview
    var $portfolio_nav = $('#portfolio-nav');
    $portfolio_nav.find('a[href="#overview"]').click(function (event) {
		event.preventDefault();
		navMenu.overviewSection();
	});

	//Loans
	$portfolio_nav.find('a[href="#loans"]').click(function (event) {
		event.preventDefault();
		navMenu.loansSection();
	});

	//Analysis
	$portfolio_nav.find('a[href="#analysis"]').click(function (event) {
		event.preventDefault();
		navMenu.analysisSection();
	});


//ANALYTICS TABS	
//................................................................................................................................................	
	//Summary
    var $portfolio_content = $("#portfolio-content");
    $portfolio_content.on("click", "#analysis-tabs-list a[href='#summary']", function (event) {
		event.preventDefault();
		$(this).tab('show');
		analyticsTab.summaryTab();
	});

	//Cash flows
	$portfolio_content.on("click", "#analysis-tabs-list a[href='#cash-flow']", function (event) {
		event.preventDefault();
		$(this).tab('show');
		analyticsTab.cashFlowTab();
	});

	//Graphs
	$portfolio_content.on("click", "#analysis-tabs-list a[href='#graphs']", function (event) {
		event.preventDefault();
		$(this).tab('show');
		analyticsTab.graphsTab();
	});


//LOANS NAV SECTION
//................................................................................................................................................	
	//Pagination control
	$portfolio_content.on('page-change.bs.table', "#all-loans-table", function() {
		var options = $("#all-loans-table").bootstrapTable('getOptions');
		var send_data = {
			"portfolio_id": globalVariable.portfolio_id, 
			limit: (options.pageNumber * options.pageSize),
			offset: options.pageSize
		};
		$.get("/portfolio/all_loans", send_data, function (data) {
			$("#all-loans-table").bootstrapTable('load', data);
		})
	});


//ANALYSIS NAV SECTION
//................................................................................................................................................	
	//Scenario selection
	$portfolio_content.on('page-change.bs.table', "#all-loans-table", function() {
		var options = $("#all-loans-table").bootstrapTable('getOptions');
		var send_data = {
			"portfolio_id": globalVariable.portfolio_id, 
			limit: (options.pageNumber * options.pageSize),
			offset: options.pageSize
		};
		$.get("/portfolio/all_loans", send_data, function (data) {
			$("#all-loans-table").bootstrapTable('load', data);
		})
	});

	//Send scenario and discount rate to run calculations model
	$portfolio_content.on('submit', "#form-analysis-criteria", function (event) {
		event.preventDefault();

        var $run_scenario_btn = $("#run-scenario-btn");
        var $select_scenario_analysis = $('#select-scenario-analysis');
        var $discount_rate = $('#discount-rate');

        var buttonText = $run_scenario_btn.text();
        if (buttonText == "RUN") {
			$select_scenario_analysis.prop("disabled", true);
			$discount_rate.prop('readonly', true);
			$run_scenario_btn.text('New scenario');
			Cookies.remove("summary_data");

			var send_data = {
				portfolio_id: globalVariable.portfolio_id,
				scenario_id: $select_scenario_analysis.val(),
				discount_rate: $discount_rate.val()
			};

			$.post("/analytics/analyze_portfolio", send_data, function (data) {
				if (data.status == "PASS") {
					helperFunctions.mustacheLoad("#analysis-tabs", "#analysis-results");
					analyticsTab.summaryTab();
				}
			})

		} else {
			$select_scenario_analysis.prop("disabled", false);
			$discount_rate.prop('readonly', false);
			$run_scenario_btn.text('RUN');
			Cookies.remove("summary_data");
		}
	});


//ANALYTICS >> GRAPHS TAB
//................................................................................................................................................	
	//Button to generate graphs
	$portfolio_content.on("click", "#btn-cf-principal", function (event) {
		event.preventDefault();

		console.log(globalVariable.principal_graph_data);



		// var data = {
		// 	labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
		// 	series: [[5, 2, 4, 2, 0], [2,5,3,1,2]]
		// };
		// new Chartist.Line('.ct-chart', data);


	});


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
	graphs_payments_data: undefined
};


//Functions to load NAV Menu
//===============================================================================================================================================
navMenu = {

	//Overview section load
	overviewSection: function() {
		helperFunctions.mustacheLoad("#portfolio-overview-script", "#portfolio-content");
		$.get("/portfolio/port_loans_status", {"portfolio_id": globalVariable.portfolio_id}, function (data) {
			helperFunctions.displayTableData("#status-summary-table", data.data);
		});
		$.get("/portfolio/fico_summary", {"portfolio_id": globalVariable.portfolio_id}, function (data) {
			helperFunctions.displayTableData("#fico-summary-table", data.data);
		})
	},

	//Loans section load
	loansSection: function() {
		helperFunctions.mustacheLoad("#loans-script", "#portfolio-content");

		//noinspection JSUnusedGlobalSymbols
        $("#all-loans-table").bootstrapTable({
            height: 700,
			url: "/portfolio/all_loans",
			method: 'GET',
			queryParams: function (params) {
				return { portfolio_id: globalVariable.portfolio_id, limit: params.limit, offset: params.offset }
			},
			cache: true,
			striped: true,
			pagination: true,
			sidePagination: 'server',
			pageSize: 30,
			pageList: "[50, 100, 200, 500]",
			search: false,
			showColumns: false,
			clickToSelect: false,
			uniqueId: "id",
			columns: [
				{
					field: 'state',
					checkbox: true,
					align: 'center',
					valign: 'middle'
				}, {
					field: 'bank_loan_id',
					title: 'Loan ID',
					align: 'center',
					sortable: false
				}, {
					field: 'property_type_code',
					title: 'Property Type',
					align: 'center',
					sortable: false
				}, {
					field: 'occupancy_code',
					title: 'Occupancy',
					align: 'center',
					sortable: false
				}, {
					field: 'product_type',
					title: 'Product Type',
					align: 'center',
					sortable: false
				}, {
					field: 'purpose',
					title: 'Purpose',
					align: 'center',
					sortable: false
				}, {
					field: 'mortgage_type',
					title: 'Mortgage Type',
					align: 'center',
					sortable: false
				}, {
					field: 'lien_position',
					title: 'Lien Position',
					align: 'center',
					sortable: false
				}, {
					field: 'original_rate',
					title: 'ORATE',
					align: 'center',
					sortable: false
				}, {
					field: 'original_appraisal_amount',
					title: 'Original Appraisal Amount',
					align: 'center',
					sortable: false
				}, {
					field: 'original_date',
					title: 'Origination Date',
					align: 'center',
					sortable: false
				}, {
					field: 'first_payment_date',
					title: 'First Payment Date',
					align: 'center',
					sortable: false
				}, {
					field: 'original_term',
					title: 'Original Term',
					align: 'center',
					sortable: false
				}, {
					field: 'remaining_term',
					title: 'Remaining Term',
					align: 'center',
					sortable: false
				}, {
					field: 'amortized_term',
					title: 'Amortized Term',
					align: 'center',
					sortable: false
				}, {
					field: 'pmi_insurance',
					title: 'PMI',
					align: 'center',
					sortable: false
				}, {
					field: 'city',
					title: 'City',
					align: 'center',
					sortable: false
				}, {
					field: 'us_state',
					title: 'State',
					align: 'center',
					sortable: false
				}, {
					field: 'zipcode',
					title: 'Zipcode',
					align: 'center',
					sortable: false
				}, {
					field: 'fico',
					title: 'FICO',
					align: 'center',
					sortable: false
				}, {
					field: 'gross_margin',
					title: 'Gross Margin',
					align: 'center',
					sortable: false
				}, {
					field: 'lcap',
					title: 'LCap',
					align: 'center',
					sortable: false
				}, {
					field: 'lfloor',
					title: 'LFloor',
					align: 'center',
					sortable: false
				}, {
					field: 'icap',
					title: 'ICap',
					align: 'center',
					sortable: false
				}, {
					field: 'pcap',
					title: 'PCap',
					align: 'center',
					sortable: false
				}, {
					field: 'IO_term',
					title: 'IO Term',
					align: 'center',
					sortable: false
				}, {
					field: 'interest_reset_interval',
					title: 'Interest Reset Interval',
					align: 'center',
					sortable: false
				}, {
					field: 'reset_index',
					title: 'Reset Index',
					align: 'center',
					sortable: false
				}, {
					field: 'first_index_rate_adjustment_date',
					title: '1st Interest Rate Adjustment Date',
					align: 'center',
					sortable: false
				}, {
					field: 'first_recast_or_next_recast',
					title: '1st Recast/Next Recast',
					align: 'center',
					sortable: false
				}, {
					field: 'recast_frequency',
					title: 'Recast Frequency',
					align: 'center',
					sortable: false
				}, {
					field: 'recast_cap',
					title: 'Recast Cap',
					align: 'center',
					sortable: false
				}, {
					field: 'negam_initial_minimum_payment_period',
					title: 'Negam Initial Minimum Payment Period',
					align: 'center',
					sortable: false
				}, {
					field: 'negam_payment_reset_frequency',
					title: 'Negam Payment Reset Frequency',
					align: 'center',
					sortable: false
				}, {
					field: 'status',
					title: 'status',
					align: 'center',
					sortable: false
				}, {
					field: 'deferred_balance',
					title: 'Deferred Balance',
					align: 'center',
					sortable: false
				}, {
					field: 'modification_date',
					title: 'Modification Date',
					align: 'center',
					sortable: false
				}, {
					field: 'foreclosure_referral_date',
					title: 'Foreclosure Referral Date',
					align: 'center',
					sortable: false
				}, {
					field: 'current_property_value',
					title: 'Current Property Value',
					align: 'center',
					sortable: false
				}, {
					field: 'current_value_date',
					title: 'Current Value Date',
					align: 'center',
					sortable: false
				}, {
					field: 'current_principal_balance',
					title: 'Current Principal Balance',
					align: 'center',
					sortable: false
				}, {
					field: 'current_interest_rate',
					title: 'Current Interest Rate',
					align: 'center',
					sortable: false
				}, {
					field: 'last_payment_received',
					title: 'Last Payment Received',
					align: 'center',
					sortable: false
				}, {
					field: 'current_FICO_score',
					title: 'Current FICO',
					align: 'center',
					sortable: false
				}, {
					field: 'BK_flag',
					title: 'BK Flag',
					align: 'center',
					sortable: false
				}, {
					field: 'MSR',
					title: 'MSR',
					align: 'center',
					sortable: false
				}, {
					field: 'senior_lien_balance',
					title: 'Senior Lien Balance',
					align: 'center',
					sortable: false
				}, {
					field: 'senior_lien_balance_date',
					title: 'Senior Lien Balance Date',
					align: 'center',
					sortable: false
				}, {
					field: 'second_lien_piggyback_flag',
					title: '2nd Lien Piggyback Flag',
					align: 'center',
					sortable: false
				}, {
					field: 'junior_lien_balance',
					title: 'Junior Lien Balance',
					align: 'center',
					sortable: false
				}, {
					field: 'junior_lien_balance_date',
					title: 'Junior Lien Balance',
					align: 'center',
					sortable: false
				}, {
					field: 'SF',
					title: 'SF',
					align: 'center',
					sortable: false
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

};


//Functions to load ANALYTICS TABS
//===============================================================================================================================================
analyticsTab = {

	//Load summary tab
	summaryTab: function () {
		var send_data = {
			portfolio_id: globalVariable.portfolio_id,
			scenario_id: $("#select-scenario-analysis").val(),
			discount_rate: $("#discount-rate").val()
		};

		var cookieSummary = Cookies.getJSON("summary_data");
	
		if (cookieSummary == undefined) {
			console.log("no break")
			$.get("/analytics/get_analysis_summary", send_data, function (data) {
            /**
             * @typedef {Object} data
             * @property {string} portfolio_balance
             * @property {string} yield_irr
             * @property {string} weighted_average_life
             * @property {string} original_cdr
             * @property {string} weighted_average_cdr
             * @property {string} original_cpr
             * @property {string} weighted_average_cpr
             * @property {string} original_recovery
             * @property {string} weighted_average_recovery
             *
             * @type {{price, npv, total_remaining_balance, yield: string, wa_avg_life, assumption_cdr, wa_cdr, assumption_cpr, wa_cpr, assumption_recovery, wa_recovery}}
             */
	            var summaryObj = {
					price: (data.price).formatNumberSeparator(2),
					npv: (data.npv).formatNumberSeparator(2),
					total_remaining_balance: (data.portfolio_balance).formatNumberSeparator(2),
					yield: (data.yield_irr).formatNumberSeparator(2) + "%",
					wa_avg_life: data.weighted_average_life.formatNumberSeparator(2),
					assumption_cdr: (data.original_cdr).formatNumberSeparator(2),
					wa_cdr: (data.weighted_average_cdr).formatNumberSeparator(2),
					assumption_cpr: (data.original_cpr).formatNumberSeparator(2),
					wa_cpr: (data.weighted_average_cpr).formatNumberSeparator(2),
					assumption_recovery: (data.original_recovery).formatNumberSeparator(2),
					wa_recovery: (data.weighted_average_recovery).formatNumberSeparator(2)
				};

				Cookies.set("summary_data", summaryObj);
				helperFunctions.mustacheLoad("#summary-tab", "#analysis-tab-content", summaryObj);
			})
		} else {
			helperFunctions.mustacheLoad("#summary-tab", "#analysis-tab-content", cookieSummary);
		}		
	},

	//Load cash flows tab
	cashFlowTab: function () {
		var send_data = {
			"portfolio_id": globalVariable.portfolio_id,
			"scenario_id": $("#select-scenario-analysis").val(),
			"discount_rate": $("#discount-rate").val()
		};
		$.get("/analytics/get_aggregate_cash_flows", send_data, function (data) {
            /**
             * @typedef {Object} data
             * @property {string} aggregate_cash_flows
             *
             * @type {Object}
             */
            var evaluated_data = eval(data.aggregate_cash_flows);
			helperFunctions.mustacheLoad("#cash-flow-tab", "#analysis-tab-content");
			$("#cash-flow-table").bootstrapTable({
				cache: false,
				data: evaluated_data,
				height: 800,
				striped: true,
				pagination: true,
				pageSize: 50,
				pageList: [30, 50, 100, 250, 500],
				columns: [
					{
						field: 'period',
						title: 'Period',
						align: 'center',
						sortable: false
					}, {
						field: 'start_balance',
						title: 'Starting Balance',
						align: 'center',
						sortable: false
					}, {					
						field: 'scheduled_principal',
						title: 'Scheduled Principal',
						align: 'center',
						sortable: false
					}, {					
						field: 'unscheduled_principal',
						title: 'Unscheduled Principal',
						align: 'center',
						sortable: false
					}, {					
						field: 'interest',
						title: 'Interest Payments',
						align: 'center',
						sortable: false
					}, {					
						field: 'defaults',
						title: 'Defaults',
						align: 'center',
						sortable: false
					}, {					
						field: 'losses',
						title: 'Losses',
						align: 'center',
						sortable: false
					}, {
						field: 'recovery',
						title: 'Recovery',
						align: 'center',
						sortable: false
					}
				]
			})
		})
	},

	//Load graphs tab
	graphsTab: function () {
		helperFunctions.mustacheLoad("#graphs-tab", "#analysis-tab-content");
		var send_data = {
			portfolio_id: globalVariable.portfolio_id,
			scenario_id: $("#select-scenario-analysis").val(),
			discount_rate: $("#discount-rate").val()
		};
		$.get("/analytics/principal_graph_data", send_data, function (data) {
			globalVariable.graphs_payments_data = data;
		})

	}
};


//Global helper functions
//===============================================================================================================================================
helperFunctions = {

	//Loads mustache template (params: script selector, loader selector and data to be inserted)
	mustacheLoad: function(script_selector, loader_selector, insert_data) {
		var data, template, informationToLoad;
		data = insert_data || {};
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
};


//General functions
//===============================================================================================================================================
//Formatting numbers: 100,000,000.55
Number.prototype.formatNumberSeparator = function(n, x) {
	var re = '\\d(?=(\\d{' + (x || 3) + '})+' + (n > 0 ? '\\.' : '$') + ')';
	return this.toFixed(Math.max(0, ~~n)).replace(new RegExp(re, 'g'), '$&,');
};


















