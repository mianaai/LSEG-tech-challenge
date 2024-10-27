#!/usr/bin/env python3

"""

"""

from copy import deepcopy
from datetime import timedelta

import os
import sys

from stock_exchange import StockExchange


class TechChallangeLseg():
	"""
	"""

	def __init__(self,
				data_path,
				nb_of_stocks_per_exchange,
				prediction_function):
		"""
		"""
		self.__data_path = data_path
		self.__stocks = {}
		self.__nb_of_stocks_per_exchange = nb_of_stocks_per_exchange
		self.__prediction_function = prediction_function

		for stock_exch_name in os.listdir(data_path):
			st_abs_path = os.path.join(data_path, stock_exch_name)
			if not os.path.isdir(st_abs_path):
				continue

			self.__stocks[stock_exch_name] = StockExchange(st_abs_path, nb_of_stocks_per_exchange)


	def get_all_stock_timeseries(self, ts_window_len=10):
		"""
		Get a timeseries from all stocks from all stock exchanges
		"""
		for stock_exch_name, stock_exch in self.__stocks.items():
			for stock_name in self.__stocks[stock_exch_name].list_stocks():
				self.__stocks[stock_exch_name].get_stock_timeseries(stock_name, ts_window_len)

	def predict_all_stocks(self, prediction_window):
		"""
		Compute predictions for all stocks
		"""
		for stock_exch_name, stock_exch in self.__stocks.items():
			for stock_name in self.__stocks[stock_exch_name].list_stocks():
				self.__stocks[stock_exch_name].predict_stock(
					stock_name, 
					self.__prediction_function,
					prediction_window)

	def write_output(self):
		"""
		Writes the stocks and their predictions for all timeseries.
		The output dir structure mirrors that of the input dir.
		"""

		output_dir = os.path.join(self.__data_path, "..", "output")

		if not os.path.exists(output_dir):
			os.makedirs(output_dir)

		for stock_exch_name, stock_exch in self.__stocks.items():
			stock_exch_path = os.path.join(output_dir, stock_exch_name)
			if not os.path.exists(stock_exch_path):
				os.makedirs(stock_exch_path)

			for stock_name in self.__stocks[stock_exch_name].list_stocks():
				stock_file_path = os.path.join(stock_exch_path, f"{stock_name}_out.csv")

				stock = stock_exch.get_stock(stock_name)

				stock_id = stock_name
				date = stock["interval"][0]
				timeseries = stock["timeseries"]

				with open(stock_file_path, "w", encoding="utf-8") as out_file:
					for i in range(len(timeseries)):
						line = f"{stock_id},{date.strftime('%d-%m-%Y')},{timeseries[i]}\n"
						out_file.write(line)

						date += timedelta(days=1)
