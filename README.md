# TARZAN
This repository contains a python implementation of TARZAN, a fast anomaly detection
algorithm introduced in [1]. The current implementation uses either Brute Force or
McCreight method [4] to construct the suffix tree.

The authors of [3] demonstrate how SAX can be combined with TARZAN for anomaly detection.
The TARZAN function allows a SAX, 1d-SAX or ABBA constructor [2].

## Prerequisites
Install python packages:
```
pip install -r requirements.txt
```

## Testing
Run the unit tests by the following command:
```
python test_TARZAN.py -v
```

## TODO
* Improve documentation.
* Implement Ukkonen method [5].
* Store z-score in suffix tree to prevent repetitive computation. Currently edges
  contain substrings so not every substring has a node. This prevents breadth
  search as recommended in [1].

## REFERENCES
[1] Keogh, Eamonn, Stefano Lonardi, and Bill'Yuan-chi Chiu. "Finding surprising
patterns in a time series database in linear time and space." Proceedings of the
eighth ACM SIGKDD international conference on Knowledge discovery and data mining. ACM, 2002.

[2] S. Elsworth and S. Güttel. ABBA: Adaptive Brownian bridge-based symbolic
aggregation of time series, MIMS Eprint 2019.11 (<http://eprints.maths.manchester.ac.uk/2712/>),
Manchester Institute for Mathematical Sciences, The University of Manchester, UK, 2019.

[3] Lin, Jessica, Eamonn Keogh, Li Wei, and Stefano Lonardi. "Experiencing SAX:
a novel symbolic representation of time series." Data Mining and knowledge discovery
15.2 (2007): 107-144.

[4] McCreight, Edward M. "A space-economical suffix tree construction algorithm."
Journal of the ACM (JACM) 23.2 (1976): 262-272.

[5] Ukkonen, Esko. "On-line construction of suffix trees." Algorithmica 14.3 (1995): 249-260.
