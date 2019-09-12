# TARZAN
This repository contains a Python implementation of TARZAN, a fast anomaly detection
algorithm introduced in [1]. The current implementation uses either a brute force or
the McCreight method [4] for constructing the suffix tree.

The authors of [3] demonstrate how SAX can be combined with TARZAN for anomaly detection.
The TARZAN function allows a SAX, 1d-SAX, or ABBA constructor [2].

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
* Current implementation not linear! Store z-score in suffix tree to prevent repetitive
  computation. Currently edges contain substrings so not every substring has a node.
  This prevents breadth search as recommended in [1].
* Improve documentation.
* Implement Ukkonen method [5].

## REFERENCES
[1] E. Keogh, S. Lonardi, and B. Chiu: "Finding surprising
patterns in a time series database in linear time and space." Proceedings of the
8th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2002.

[2] S. Elsworth and S. Güttel: "ABBA: Adaptive Brownian bridge-based symbolic
aggregation of time series." MIMS Eprint 2019.11 (<http://eprints.maths.manchester.ac.uk/2712/>),
Manchester Institute for Mathematical Sciences, The University of Manchester, UK, 2019.

[3] J. Lin,E. Keogh, L. Wei, and S. Lonardi: "Experiencing SAX:
a novel symbolic representation of time series." Data Mining and Knowledge Discovery,
15(2):107--144, 2007.

[4] E. M. McCreight: "A space-economical suffix tree construction algorithm."
Journal of the ACM, 23(2):262--272, 1976.

[5] E. Ukkonen: "On-line construction of suffix trees." Algorithmica 14(3):249-260, 1995.
