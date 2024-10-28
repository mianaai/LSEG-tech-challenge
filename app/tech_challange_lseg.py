#!/usr/bin/env python3

"""
TechChallangeLseg class implementation.
"""

from copy import deepcopy
from datetime import timedelta, datetime
from typing import Callable

import os
import sys

from stock_exchange import StockExchange


class TechChallangeLseg():
	"""
	Class which handles the 
	"""

	def __init__(self,
				 data_path: str,
				 nb_of_stocks_per_exchange: int):
		"""
		Initialise a StockExchange object for each dir in the data dir.

		:param data_path: Absolute path to the root of the data directory.
		:param nb_of_stocks_per_exchange: number of stocks to read per exchange.
		"""
		self.__data_path = data_path
		self.__stocks = {}
		self.__nb_of_stocks_per_exchange = nb_of_stocks_per_exchange

		for stock_exch_name in os.listdir(data_path):
			st_abs_path = os.path.join(data_path, stock_exch_name)
			if not os.path.isdir(st_abs_path):
				continue

			# Initialise a StockExchange object for each stock exchange.
			self.__stocks[stock_exch_name] = StockExchange(st_abs_path, nb_of_stocks_per_exchange)

	def get_all_stock_timeseries(self, ts_window_len: int=10, start_date: datetime=None):
		"""
		Retrieve a timeseries for all stocks from all stock exchanges

		:param ts_window_len: Length of the timeseries window we want to extract, in days.
		:param start_date: Start date of the timeseries.
		"""
		for stock_exch_name, stock_exch in self.__stocks.items():
			for stock_name in self.__stocks[stock_exch_name].list_stocks():
				self.__stocks[stock_exch_name].get_stock_timeseries(
					stock_name, ts_window_len, start_date)

	def predict_all_stocks(self, prediction_function: Callable[[list, int], list], prediction_window: int):
		"""
		Compute predictions for all stocks
		:param prediction_function: Function used to predict the next values of a time series.
		"""
		for stock_exch_name, stock_exch in self.__stocks.items():
			for stock_name in self.__stocks[stock_exch_name].list_stocks():
				self.__stocks[stock_exch_name].predict_stock(
					stock_name, 
					prediction_function,
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
