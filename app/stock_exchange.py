#!/usr/bin/env python3

"""
StockExchange class implementation.
"""

import json
import os
import csv

from datetime import datetime, timedelta
from random import randint
from typing import Callable


class StockExchange():
	"""
	Class which handles a single stock exchange.
	"""

	def __init__(self, data_path: str, nb_of_stocks_per_exchange: int):
		"""
		Reads all the stocks from a single stock exchange.
		We assume that the values in each csv files are in consecutive days.

		:param data_path: String. Absolute path to the directory from the local filesystem
			containing the stock values as csv files.
		:param nb_of_stocks_per_exchange: number of stocks to read per exchange.
		"""

		self.__data_path = data_path
		self.__stocks = {}

		for stock_fn in os.listdir(data_path):
			# Only read the first nb_of_stocks_per_exchange files from this stock exchange
			if nb_of_stocks_per_exchange <= 0:
				break
			nb_of_stocks_per_exchange -= 1

			stock_abspath = os.path.join(data_path, stock_fn)

			if not os.path.isfile(stock_abspath):
				continue

			stock_name = stock_fn.partition('.')[0]

			self.__stocks[stock_name] = {
				"data": None,
				"interval" : None
			}

			# First, only read the first and last line to get the start_date and end_date.
			# I assume that the datapoints in each stock files are consecutive days.
			with open(stock_abspath, "rb") as stock_file:
				# Read the first line to get the first date.
				first_line = stock_file.readline().decode().split(',')
				try:
					start_date = datetime.strptime(first_line[1], "%d-%m-%Y")
				except (ValueError, IndexError):
					raise Exception(f"Unexpected input in stock {stock_name}")

				# Move file cursor to the last line of the file.
				try:
					stock_file.seek(-2, os.SEEK_END)
					while stock_file.read(1) != b"\n":
						stock_file.seek(-2, os.SEEK_CUR)
				except OSError:
					stock_file.seek(0)

				last_line = stock_file.readline().decode().split(',')

				# Read the last line the get the last date.
				try:
					end_date = datetime.strptime(last_line[1], "%d-%m-%Y")
				except (ValueError, IndexError):
					raise Exception(f"Unexpected input in stock {stock_name}")

				# Assuming that the values in the files are consecutive days
				self.__stocks[stock_name]["interval"] = (start_date, end_date)

	def get_random_interval_for_stock(self, stock_name: str, ts_window_len: int) -> tuple:
		"""
		Get the start and end dates for a random interval of a given length for a given stock.

		:param stock_name: String. Name of the stock (e.g. FLTR, GSK)
		:param ts_window_len: Length of the timeseries window we want to extract, in days.
		"""
		start_date, end_date = self.__stocks[stock_name]["interval"]
		interval_days = (end_date - start_date).days - ts_window_len

		if interval_days < 0:
			raise Exception(f"Not enough datapoints in stock {stock_name} to get timeseries of length {ts_window_len}")

		start_date += timedelta(days=randint(0, interval_days + 1))
		end_date = start_date + timedelta(days=ts_window_len-1)

		return (start_date, end_date)

	def list_stocks(self) -> list:
		"""
		:return List: List containing all the stock names from this exchange.
		"""
		return list(self.__stocks.keys())

	def get_stock_timeseries(self, stock_name: str, ts_window_len: int=10, start_date: datetime=None):
		"""
		Returns the consecutive values of a stock given the start date and length in days.
		If a start date is not provided, choose a random one.

		:param stock_name: String. Name of the stock (e.g. FLTR, GSK)
		:param ts_window_len: Int. Length of the timeseries to return
		"""

		# Get a random interval if a start date was not provided.
		if not start_date:
			start_date, end_date = self.get_random_interval_for_stock(stock_name, ts_window_len)
		else:
			end_date = start_date + timedelta(days=ts_window_len-1)

		stock_file_path = os.path.join(self.__data_path, f"{stock_name}.csv")

		# Check if the file exists
		if not os.path.exists(stock_file_path):
			raise Exception(f"Stock file {stock_file_path} does not exist.")

		# Read the stock file line by line, save only the interval [start_date, end_date)
		# Possible improvement: to avoid reading the entire file into memory, we could
		# only read the desired interval. To do this we would need to find the location of the
		# line corresponding with start_date. 
		# If the lines all had the same length (nb of chars), this would be easy: compute the offset
		# from the number of days and the length of the lines.
		# Since the lines can vary in length, another solution would be to do a binary search of the start_date.
		# Did not implement this due to a lack of time.
		with open(stock_file_path, "r", encoding="utf-8") as stock_file:
			lines = csv.reader(stock_file)
			timeseries = []

			for line in lines:
				try:
					stock_id = line[0]
					date = datetime.strptime(line[1], "%d-%m-%Y")
					value = float(line[2])
				except (ValueError, IndexError):
					raise Exception(f"Unexpected input in stock {stock_name}, line: {line}")

				if date > end_date:
					break

				if date >= start_date:
					timeseries.append(value)

			if len(timeseries) < ts_window_len:
				raise Exception(f"Invalid start date {start_date} given for stock {stock_name}")

			self.__stocks[stock_name] = {
				"timeseries": timeseries,
				"interval": (start_date, end_date)
			}

	def predict_stock(self,
		stock_name: str,
		stock_prediction_function: Callable[[list, int], list],
		prediction_window: int=3):
		"""
		Predict the next values of a given stock using a given prediction function.
		
		:param stock_name: String. Name of the stock (e.g. FLTR, GSK)
		:param stock_prediction_function: function used to predict the next values of a stock.
		:param prediction_window: Number of values to predict.
		"""
		prediction = stock_prediction_function(
			self.__stocks[stock_name]["timeseries"],
			prediction_window=prediction_window)

		self.__stocks[stock_name]["timeseries"].extend(prediction)
		start_date, end_date = self.__stocks[stock_name]["interval"]
		end_date += timedelta(days=prediction_window)
		self.__stocks[stock_name]["interval"] = (start_date, end_date)

	def get_stock(self, stock_name: str) -> dict:
		"""
		:return dict:
		{
			"timeseries": List,
			"interval": (datetime_object, datetime_object)
		}
		"""
		return self.__stocks[stock_name]
