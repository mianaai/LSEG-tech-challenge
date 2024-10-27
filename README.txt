Pre-interview challenge for LSEG

Run instructions:
$ python3 <repo-root>/app/main.py --data-path <path-to-data-dir> --nb-stocks <nb-of-stock-files-to-read-per-exchange>

Output:
The app creates a dir called output in the same dir where the data dir is found.
The output dir mirrors the structure of the data dir. 

Assumptions made:
 - Data input assumptions: I assume that the first levels of the data dir are stock exchanges, and
 	that each stock eschange contain csv files each corresponding to a single stock from that exchange.
 - I don't assume that the time intervals from the different stock files are the same.
 - I get a different random interval for the prediction for each stock.
 - I assume that the data in all stock files are consecutive days.
