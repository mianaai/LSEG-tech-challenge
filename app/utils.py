#!/usr/bin/env python3

"""
Utils for the LSEG tech challenge.
"""

from copy import copy

def default_prediction_function(timeseries: list, prediction_window: int=3) -> list:
	"""
	Predict the next three values of a time series.
	Default prediction function as described in the challenge document.

	Prediction logic:
	n1 is the same as the second highest value from 0 to n
	n2 is half the difference between n and n+1 - I assume that this means n + (n - n1) / 2
	n3 is a quarter the difference between n+1 and n+2 - I assume that this means n1 + (n1 - n2) / 4

	:param timeseries: List of values
	"""
	n_val = timeseries[-1]

	ts_copy = copy(timeseries)
	ts_copy.sort()

	n1_val = ts_copy[-2]
	n2_val = n_val + (n_val - n1_val) / 2
	n3_val = n1_val + (n1_val - n2_val) / 4

	return [n1_val, n2_val, n3_val]
