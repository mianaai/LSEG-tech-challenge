#!/usr/bin/env python3

"""

"""

from copy import copy

def default_prediction_function(timeseries, prediction_window=3):
	"""
	Predict the next three values of a time series.

	:param timeseries: List of values
	"""
	n_val = timeseries[-1]

	ts_copy = copy(timeseries)
	ts_copy.sort()

	n1_val = ts_copy[-2]
	n2_val = n1_val + (n_val - n1_val) / 2
	n3_val = n2_val + (n1_val - n2_val) / 4

	return [n1_val, n2_val, n3_val]
