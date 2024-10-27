#!/usr/bin/env python3

"""
Entry point to LSEG tech challenge.
"""

from datetime import datetime
import argparse
import os

from tech_challange_lseg import TechChallangeLseg
from utils import default_prediction_function

DATA_PATH = os.path.join(os.path.abspath("."), "..", "data")


def main():
	"""
	Entry point to LSEG tech challenge.
	"""
	parser = argparse.ArgumentParser(description='What the program does')
	parser.add_argument("--data-path", dest="data_path", type=str,
						help="",
						default=DATA_PATH)
	parser.add_argument("--nb-stocks", dest="nb_stocks", type=int,
						help="The number of stocks to read from each exchange",
						default=1)
	parser.add_argument("--start-date", dest="start_date", type=str,
						help="Start date for the timeseries interval in %d-%m-%Y format.",
						default=None)
	parser.add_argument("--ts-window-len", dest="ts_window_len", type=int,
						help="Size of the timeseries window, in days.",
						default=10)
	args = parser.parse_args()
	start_date = None
	if args.start_date:
		start_date = datetime.strptime(args.start_date, "%d-%m-%Y")
	
	st = TechChallangeLseg(
		data_path=args.data_path,
		nb_of_stocks_per_exchange=args.nb_stocks)
	st.get_all_stock_timeseries(
		ts_window_len=args.ts_window_len,
		start_date=start_date)
	st.predict_all_stocks(
		prediction_function=default_prediction_function,
		prediction_window=3)
	st.write_output()


if __name__ == '__main__':
	main()

