# Implemetation of SAX (Symbolic Aggregate approXimation)
## https://cs.gmu.edu/~jessica/SAX_DAMI_preprint.pdf

import string
from scipy.stats import norm
import numpy as np
import warnings

class SAX(object):

    def __init__(self, *, w = 2, k = 5):
        self.width = w
        self.number_of_symbols = k

    def transform(self, time_series):
        compressed_time_series = self._compress(time_series)
        symbolic_time_series = self._digitize(compressed_time_series)
        return symbolic_time_series

    def inverse_transform(self, symbolic_time_series):
        compressed_time_series = self._reverse_digitize(symbolic_time_series)
        time_series = self._reconstruct(compressed_time_series)
        return time_series

    def _compress(self, ts):
        return self._pca_mean(ts)

    def _pca_mean(self, ts):
        if len(ts) % self.width != 0:
            warnings.warn("Result truncates, width does not divide length")
        return [np.mean(ts[i*self.width:np.min([len(ts), (i+1)*self.width])]) for i in range(int(np.floor(len(ts)/self.width)))]

    def _digitize(self, ts):
        symbolic_ts = self._gaussian_breakpoints(ts)
        return symbolic_ts

    def _gaussian_breakpoints(self, ts):
        # Construct Breakpoints
        breakpoints = np.hstack((norm.ppf([float(a) / self.number_of_symbols for a in range(1, self.number_of_symbols)], scale=1), np.inf))
        ts_GB = ''
        for i in ts:
            for j in range(len(breakpoints)):
                if i < breakpoints[j]:
                    ts_GB += chr(97 + j)
                    break
        return ts_GB

    def _reverse_pca(self, ts):
        return np.kron(ts, np.ones([1,self.width])[0])

    def _reverse_gaussian_breakpoints(self, ts_GB):
        breakpoint_values = norm.ppf([float(a) / (2 * self.number_of_symbols) for a in range(1, 2 * self.number_of_symbols, 2)], scale=1)
        ts = []
        for i in ts_GB:
            j = int(ord(i)-97)
            ts.append(breakpoint_values[j])
        return ts

    def _reverse_digitize(self, symbolic_ts):
        return self._reverse_gaussian_breakpoints(symbolic_ts)

    def _reconstruct(self, reduced_ts):
        return self._reverse_pca(reduced_ts)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from tslearn.piecewise import SymbolicAggregateApproximation

    # Generate a random walk
    ts = np.random.normal(size = 700)
    ts = np.cumsum(ts)
    ts = ts - np.mean(ts)
    ts /= np.std(ts, ddof=1)

    n_sax_symbols = 8
    n_paa_segments = 10

    # tslearn SAX implementation
    sax = SymbolicAggregateApproximation(n_segments=n_paa_segments, alphabet_size_avg=n_sax_symbols)
    sax_dataset_inv = sax.inverse_transform(sax.fit_transform(ts))

    # Our SAX implementation
    width = len(ts) // n_paa_segments
    sax = SAX(w = width, k = n_sax_symbols)
    sax_ts = sax.transform(ts)
    recon_ts = sax.inverse_transform(sax_ts)

    plt.figure()
    plt.plot(ts, "b-", alpha=0.4)
    plt.plot(sax_dataset_inv[0].ravel(), "b-")
    plt.plot(recon_ts, 'r--')
    plt.legend(['original', 'tslearn SAX implementation', 'our SAX implementation'])
    plt.title("SAX, %d symbols" % n_sax_symbols)
    plt.show()
