from itertools import chain
import pandas as pd


class LoanPortfolio:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.loan_df = pd.read_csv(csv_file)
