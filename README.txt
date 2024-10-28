Pre-interview challenge for LSEG

Run instructions:
$ python3 <repo-root>/app/main.py --nb-stocks <nb-of-stock-files-to-read-per-exchange> [--data-path <path-to-data-dir> --start-date <%d-%m-%Y> --ts-window-len int]


Implementation details

Assumptions made:
 - Data input assumptions: I assume that the first levels of the data dir are stock exchanges, and
 	that each stock eschange contain csv files each corresponding to a single stock from that exchange.
 - I assume that the data in all stock files are consecutive days.
 - I get a different random interval for the prediction for each stock.
 - I don't assume that the time intervals from the different stock files are the same.

Repo structure:
root
	app
		__init__.py
		main.py
		tech_challange_lseg.py
		stock_exchange.py
		utils.py
	data
		LSE
		NASDAQ
		NYSE

main.py - is the entry point, it instantiates a TechChallangeLseg object.
tech_challange_lseg.py - implements the TechChallangeLseg class. This handles multiple stock exchanges,
	it can trigger operations for all of them (read, predict), it can write the prediction outputs.
stock_exchange.py - implements the StockExchange class. This handles a single stock exchange.
	It can read the data for a stock, it can run prediction for a stock.
utils.py - defines the default_prediction_function function.

Output:
The app creates a dir called output in the same dir where the data dir is found.
The output dir mirrors the structure of the data dir. 
