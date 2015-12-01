import pandas as pd
import numpy as np


def calculate_aggregate_portfolio_data(loans_list):
    all_loans_df = pd.DataFrame(list(loans_list))
    active_loans = all_loans_df[all_loans_df['current_principal_balance'] > 0]

    loans_data = calculate_total_loans_data(active_loans)
    wac = calculate_wac(active_loans)
    wal = calculate_wal(active_loans)

    result_calculations = {
        "total_loan_balance": float(loans_data['total_balance']),
        "total_loan_count": int(loans_data['total_count']),
        "avg_loan_balance": float(loans_data['avg_balance']),
        "weighted_avg_coupon": float(wac),
        "weighted_avg_life_to_maturity": float(wal),
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


def loans_status_summary(loans_query_result):
    loans_df = pd.DataFrame(list(loans_query_result))
    active_loans = loans_df[loans_df['current_principal_balance'] > 0]

    if any(active_loans.status == 'CURRENT'):
        current_balance = active_loans.groupby('status')['current_principal_balance'].sum()['CURRENT']
        current_count = active_loans.groupby('status')['current_principal_balance'].count()['CURRENT']
    else:
        current_balance = 0
        current_count = 0

    if any(active_loans.status == '90 DPD'):
        dpd90_balance = active_loans.groupby('status')['current_principal_balance'].sum()['90 DPD']
        dpd90_count = active_loans.groupby('status')['current_principal_balance'].count()['90 DPD']
    else:
        dpd90_balance = 0
        dpd90_count = 0

    if any(active_loans.status == 'FC'):
        fc_balance = active_loans.groupby('status')['current_principal_balance'].sum()['FC']
        fc_count = active_loans.groupby('status')['current_principal_balance'].count()['FC']
    else:
        fc_balance = 0
        fc_count = 0

    if any(active_loans.status == '60 DPD'):
        dpd60_balance = active_loans.groupby('status')['current_principal_balance'].sum()['60 DPD']
        dpd60_count = active_loans.groupby('status')['current_principal_balance'].count()['60 DPD']
    else:
        dpd60_balance = 0
        dpd60_count = 0

    if any(active_loans.status == 'REO'):
        reo_balance = active_loans.groupby('status')['current_principal_balance'].sum()['REO']
        reo_count = active_loans.groupby('status')['current_principal_balance'].count()['REO']
    else:
        reo_balance = 0
        reo_count = 0

    if any(active_loans.status == 'REPERF'):
        reperf_balance = active_loans.groupby('status')['current_principal_balance'].sum()['REPERF']
        reperf_count = active_loans.groupby('status')['current_principal_balance'].count()['REPERF']
    else:
        reperf_balance = 0
        reperf_count = 0

    if any(active_loans.status == '30 DPD'):
        dpd30_balance = active_loans.groupby('status')['current_principal_balance'].sum()['30 DPD']
        dpd30_count = active_loans.groupby('status')['current_principal_balance'].count()['30 DPD']
    else:
        dpd30_balance = 0
        dpd30_count = 0

    if any(active_loans.status == 'REM'):
        rem_balance = active_loans.groupby('status')['current_principal_balance'].sum()['REM']
        rem_count = active_loans.groupby('status')['current_principal_balance'].count()['REM']
    else:
        rem_balance = 0
        rem_count = 0

    if any(active_loans.status == 'CLAIM'):
        claim_balance = active_loans.groupby('status')['current_principal_balance'].sum()['CLAIM']
        claim_count = active_loans.groupby('status')['current_principal_balance'].count()['CLAIM']
    else:
        claim_balance = 0
        claim_count = 0

    result = {
        "CURRENT": {"balance": str(current_balance), "count": str(current_count)},
        "90 DPD": {"balance": str(dpd90_balance), "count": str(dpd90_count)},
        "FC": {"balance": str(fc_balance), "count": str(fc_count)},
        "60 DPD": {"balance": str(dpd60_balance), "count": str(dpd60_count)},
        "REO": {"balance": str(reo_balance), "count": str(reo_count)},
        "REPERF": {"balance": str(reperf_balance), "count": str(reperf_count)},
        "30 DPD": {"balance": str(dpd30_balance), "count": str(dpd30_count)},
        "REM": {"balance": str(rem_balance), "count": str(rem_count)},
        "CLAIM": {"balance": str(claim_balance), "count": str(claim_count)}
    }
    return result


def fico_summary(loans_query_result):
    loans_df = pd.DataFrame(list(loans_query_result))

    max_fico = loans_df['current_FICO_score'].max()
    min_fico = loans_df['current_FICO_score'].min()

    df = loans_df[np.isfinite(loans_df['current_FICO_score'])]
    fico = df['current_FICO_score'].astype(np.dtype('float64'))
    balance = df['current_principal_balance'].astype(np.dtype('float64'))
    wa_fico = np.average(fico, weights=balance)

    result = {"max_fico": max_fico, "min_fico": min_fico, "wa_fico": int(wa_fico)}

    return result
