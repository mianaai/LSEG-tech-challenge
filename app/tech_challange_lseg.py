#!/usr/bin/env python3

"""

"""

from copy import deepcopy
from datetime import timedelta
from random import randint

import os
import sys

from stock_exchange import StockExchange


class TechChallangeLseg():
	"""
	"""

	def __init__(self, data_path, nb_of_stocks_per_exchange=1):
		"""
		"""
		self.__data_path = data_path
		self.__stocks = {}
		self.__nb_of_stocks_per_exchange = nb_of_stocks_per_exchange

		for stock_exch_name in os.listdir(data_path):
			st_abs_path = os.path.join(data_path, stock_exch_name)
			if not os.path.isdir(st_abs_path):
				continue

			self.__stocks[stock_exch_name] = StockExchange(st_abs_path, nb_of_stocks_per_exchange)


	def get_all_stock_timeseries(self, timeseries_len=10):
		"""
		Get a timeseries from all stocks from all stock exchanges

		:return dict: 
		{
			"Stock Exchange Name": {
				"Stock Name": {
					"start_date": Datetime Object,
					"end_date": Datetime Object,
					"timeseries": List
				},
				...
			},
			...
		}
		"""
		all_stocks = {}

		for stock_exch_name, stock_exch in self.__stocks.items():
			all_stocks[stock_exch_name] = {}
			for stock_name in self.__stocks[stock_exch_name].list_stocks():
				# Get random start date
				interval = self.__stocks[stock_exch_name].get_date_interval(stock_name)
				interval_days = (interval["end_date"] - interval["start_date"]).days - timeseries_len

				if interval_days < 0:
					raise Exception(f"Not enough datapoints in stock {stock_name} of exchange {stock_exch_name} to get timeseries of length {timeseries_len}")

				start_date = interval["start_date"] + timedelta(days=randint(0, interval_days + 1))

				all_stocks[stock_exch_name][stock_name] = self.__stocks[stock_exch_name].get_stock_timeseries(
					stock_name, start_date, timeseries_len)

		return all_stocks

	def predict_stock(self, all_stocks):
		"""
		Compute predictions for all stocks

		:return dict: 
		{
			"Stock Exchange Name": {
				"Stock Name": {
					"start_date": Datetime Object,
					"end_date": Datetime Object,
					"timeseries": List (updated)
				},
				...
			},
			...
		}
		"""
		all_stocks_predicted = deepcopy(all_stocks)

		for stock_exch_name in all_stocks_predicted:
			for stock_name in all_stocks_predicted[stock_exch_name]:
				prediction = StockExchange.get_prediction(
					all_stocks_predicted[stock_exch_name][stock_name]["timeseries"])

				all_stocks_predicted[stock_exch_name][stock_name]["timeseries"].extend(prediction)
				all_stocks_predicted[stock_exch_name][stock_name]["end_date"] += timedelta(days=len(prediction))

		return all_stocks_predicted

	def write_output(self, all_stocks_predicted):
		"""
		Writes the stocks and their predictions for all timeseries.
		The output dir structure mirrors that of the input dir.

		:param all_stocks_predicted: Dict of timeseries with predictions from all stocks.
		"""

		output_dir = os.path.join(self.__data_path, "..", "output")

		if not os.path.exists(output_dir):
			os.makedirs(output_dir)

		for stock_exch_name in all_stocks_predicted:
			stock_exch_path = os.path.join(output_dir, stock_exch_name)
			if not os.path.exists(stock_exch_path):
				os.makedirs(stock_exch_path)

			for stock_name in all_stocks_predicted[stock_exch_name]:
				stock_file_path = os.path.join(stock_exch_path, f"{stock_name}_out.csv")

				stock_id = stock_name
				date = all_stocks_predicted[stock_exch_name][stock_name]["start_date"]
				timeseries = all_stocks_predicted[stock_exch_name][stock_name]["timeseries"]

				with open(stock_file_path, "w", encoding="utf-8") as out_file:
					for i in range(len(timeseries)):
						line = f"{stock_id},{date.strftime('%d-%m-%Y')},{timeseries[i]}\n"
						date += timedelta(days=1)
						out_file.write(line)
