import pandas as pd
import numpy as np


def calculate_aggregate_portfolio_data(loans_list):
	all_loans_df = pd.DataFrame(list(loans_list))
	active_loans = all_loans_df[all_loans_df['current_principal_balance'] > 0]

	loans_data = calculate_total_loans_data(active_loans)
	wac = calculate_wac(active_loans)
	wal = calculate_wal(active_loans)

	result_calculations = {
		"total_loan_balance": loans_data['total_balance'],
		"total_loan_count": loans_data['total_count'],
		"avg_loan_balance": loans_data['avg_balance'],	
		"weighted_avg_coupon": wac,
		"weighted_avg_life_to_maturity": wal,
	}
	return result_calculations


def calculate_total_loans_data(active_loans):
	total_loans_balance = active_loans['current_principal_balance'].sum()
	total_loans_count = active_loans['current_principal_balance'].count()
	avg_loan_balance = total_loans_balance / total_loans_count
	
	result_dict = {
		'total_balance': total_loans_balance,
		'total_count': total_loans_count,
		'avg_balance': avg_loan_balance
	}
	return result_dict


def calculate_wac(active_loans):
	interest_rate_float = active_loans['current_interest_rate'].astype(np.dtype('float64'))
	principal_balance_float = active_loans['current_principal_balance'].astype(np.dtype('float64'))
	
	wac = np.average(interest_rate_float, weights=principal_balance_float)
	return wac


def calculate_wal(active_loans):
	remaining_term_float = active_loans['remaining_term'].astype(np.dtype('float64'))
	principal_balance_float = active_loans['current_principal_balance'].astype(np.dtype('float64'))

	wal = np.average(remaining_term_float, weights=principal_balance_float)
	return wal



# float_interest_rates_40yr = [ 0.020000, 0.021440, 0.022984, 0.024639, 0.026412, 0.028314, 0.030353,
# 	0.032538, 0.034881, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 
# 	0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392,
# 	0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 
# 	0.037392, 0.037392, 0.037392, 0.037392, 0.037392, 0.037392 ]


# def cash_flow_calculation(csv_file):
# 	portfolio = pd.read_csv(csv_file, sep=",")

# 	#Valid loans (current balance is bigger than ZERO)
# 	all_current_balance = portfolio["Current_Principal_Balance"]
# 	active_loans = portfolio[current_balance > 0]

# 	#Example of economic assumptions:
# 	assumptions_cdr = 0.08
# 	assumptions_cpr = 0.09

# 	#Example of risks profiles:
# 	florida_cdr = 0.05
# 	fico_above_750_cdr = 0.02
# 	fico_above_750_cpr = 0.15

# 	#Getting the max the valid Remaining_Term
# 	max_term = active_loans['Remaining_Term'].max()

# 	#Group fixed and float rate loans
# 	float_loans = active_loans[active_loans['Gross_Margin'] > 0]
# 	fixed_loans = active_loans[active_loans['Gross_Margin'].isnull()]






