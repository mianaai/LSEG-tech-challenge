#!/usr/bin/env python3

"""

"""

import copy
from datetime import datetime, timedelta
import json
import os
import csv


class StockExchange():
	"""
	Class which handles a single stock exchange.
	"""

	def __init__(self, data_path, nb_of_stocks_per_exchange):
		"""
		Reads all the stocks from a single stock exchange.
		We assume that the values in each csv files are in consecutive days.

		:param data_path: String. Absolute path to the directory from the local filesystem
			containing the stock values as csv files.
		"""

		# TODO: lazy reading of the time interval
		self.__stocks = {}

		for stock_fn in os.listdir(data_path):
			if nb_of_stocks_per_exchange <= 0:
				break
			nb_of_stocks_per_exchange -= 1

			stock_abspath = os.path.join(data_path, stock_fn)
			if not os.path.isfile(stock_abspath):
				continue

			stock_name = stock_fn.partition('.')[0]

			self.__stocks[stock_name] = {
				"data": {},
				"interval" : None
			}

			with open(stock_abspath, "r", encoding="utf-8") as stock_file:
				stock_data = csv.reader(stock_file)
				start_date = None
				end_date = None
				for line in stock_data:

					try:
						date = datetime.strptime(line[1], "%d-%m-%Y")
						value = float(line[2])
					except (ValueError, IndexError):
						raise Exception(f"Unexpected input in stock {stock_name}")

					if not start_date:
						start_date = date
					elif date < start_date:
						start_date = date

					if not end_date:
						end_date = date
					elif date > end_date:
						end_date = date

					self.__stocks[stock_name]["data"][date] = value

				# Assuming that the values in the files are consecutive days
				self.__stocks[stock_name]["interval"] = {
					"start_date": start_date,
					"end_date": end_date
				}

	def get_date_interval(self, stock_name):
		"""
		"""
		return self.__stocks[stock_name]["interval"]

	def list_stocks(self):
		"""
		:return List: List containing all the stock names from this exchange.
		"""
		return list(self.__stocks.keys())

	def get_stock_timeseries(self, stock_name, start_date, timeseries_len=10):
		"""
		Returns the consecutive values of a stock given the start date and length in days.

		:param stock_name: String. Name of the stock (e.g. FLTR, GSK)
		:param timeseries_len: Int. Length of the timeseries to return
		:param start_date: Datetime Object. Date of the first element in the time series
		:return dict: return the timeseries and time interval in the following format:
		{
			"start_date": Datetime Object,
			"end_date": Datetime Object,
			"timeseries": List
		}
		"""

		end_date = start_date + timedelta(days=timeseries_len)

		timeseries = []
		# todo: better implementation
		for date, value in self.__stocks[stock_name]["data"].items():
			if start_date <= date and date < end_date:
				timeseries.append(value)

			if date >= end_date:
				break

		return {
			"start_date" : start_date,
			"end_date" : end_date,
			"timeseries" : timeseries
		}

	@staticmethod
	def get_prediction(timeseries):
		"""
		Predict the next three values of a time series.

		:param timeseries: List of values
		"""
		n_val = timeseries[-1]

		ts_copy = copy.copy(timeseries)
		ts_copy.sort()

		n1_val = ts_copy[-2]
		n2_val = n1_val + (n_val - n1_val) / 2
		n3_val = n2_val + (n1_val - n2_val) / 4

		return [n1_val, n2_val, n3_val]
