#!/usr/bin/env python3

"""

"""

import argparse
import os

from stock_exchange import StockExchange
from tech_challange_lseg import TechChallangeLseg

DATA_PATH = os.path.join(os.path.abspath("."), "..", "data")


def main():
	"""
	"""
	parser = argparse.ArgumentParser(description='What the program does')
	parser.add_argument("--data-path", dest="data_path", type=str,
						help="",
						default=DATA_PATH)
	parser.add_argument("--nb-stocks", dest="nb_stocks", type=int,
						help="The number of stocks to read from each exchange",
						default=1)
	args = parser.parse_args()
	
	st = TechChallangeLseg(args.data_path, args.nb_stocks)
	st.get_all_stock_timeseries()
	st.predict_all_stocks(prediction_window=3)
	st.write_output()


if __name__ == '__main__':
	main()

