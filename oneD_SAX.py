# Impementation of 1D-SAX
## https://link.springer.com/chapter/10.1007/978-3-642-41398-8_24

from sklearn import linear_model
from scipy.stats import norm
import numpy as np

class oneD_SAX(object):
    def __init__(self, *, w=2, k_slope=5, k_intercept=5):
        self.width = w
        self.k_slope = k_slope
        self.k_intercept = k_intercept

    def transform(self, time_series):
        compressed_time_series = self._compress(np.array(time_series))
        symbolic_time_series = self._digitize(compressed_time_series)
        return symbolic_time_series

    def inverse_transform(self, symbolic_time_series):
        compressed_time_series = self._reverse_digitize(symbolic_time_series)
        time_series = self._reconstruct(compressed_time_series)
        return time_series

    def _compress(self, time_series):
        # See (1) in paper
        pieces = np.empty([0,2]) # gradient, intercept
        for i in range(int(np.floor(len(time_series)/self.width))):
            t = np.arange(i*self.width, np.min([len(time_series), (i+1)*self.width]))
            Tbar = np.mean(t)
            V = time_series[t]
            Vbar = np.mean(V)
            s = np.dot(t-Tbar, V)/np.dot(t-Tbar, t-Tbar)
            b = Vbar - s*Tbar
            a = 0.5*s*(t[0]+t[-1]) + b
            pieces = np.vstack([pieces, np.array([s, a])])
        return pieces

    def _digitize(self, compressed_time_series):
        # Construct Breakpoints
        breakpoints_slope = np.hstack((norm.ppf([float(a) / self.k_slope for a in range(1, self.k_slope)], scale = np.sqrt(0.03/self.width)), np.inf))
        breakpoints_intercept = np.hstack((norm.ppf([float(a) / self.k_intercept for a in range(1, self.k_intercept)], scale = 1), np.inf))

        symbolic_time_series = ''

        for [grad, c] in compressed_time_series:
            for i in range(len(breakpoints_slope)):
                if grad < breakpoints_slope[i]:
                    cnt1 = i
                    break
            for j in range(len(breakpoints_intercept)):
                if c < breakpoints_intercept[j]:
                    cnt2 = j
                    break
            symbolic_time_series += chr((cnt1)*self.k_intercept + cnt2 + 97)
        return symbolic_time_series

    def _reverse_digitize(self, symbolic_time_series):

        # Breakpoint midpoints
        slope_values = norm.ppf([float(a) / (2 * self.k_slope) for a in range(1, 2 * self.k_slope, 2)], scale=np.sqrt(0.03/self.width))
        intercept_values = norm.ppf([float(a) / (2 * self.k_intercept) for a in range(1, 2 * self.k_intercept, 2)], scale=1)

        compressed_time_series = np.empty([0,2])
        for letter in symbolic_time_series:
            j = (ord(letter) - 97) % self.k_intercept
            i = (ord(letter) - 97) // self.k_intercept
            compressed_time_series = np.vstack([compressed_time_series, np.array([slope_values[i], intercept_values[j]])])
        return compressed_time_series


    def _reconstruct(self, compressed_time_series):
        time_series = []
        for s,a in compressed_time_series:
            x = (np.array([range(0,self.width)]))[0]
            x = x - np.mean(x)
            y = s*x + a
            time_series = time_series + y.tolist()
        return time_series


if __name__ == "__main__":
    """
    Compare 1d-SAX implementation against tslearn implementation.
    """
    import matplotlib.pyplot as plt
    from tslearn.piecewise import OneD_SymbolicAggregateApproximation

    # Generate a random walk
    ts = np.random.normal(size = 700)
    ts = np.cumsum(ts)
    ts = ts - np.mean(ts)
    ts /= np.std(ts, ddof=1)
    print('length of ts', len(ts))

    n_sax_symbols_avg = 8
    n_sax_symbols_slope = 8
    n_paa_segments = 10

    # 1d-SAX transform
    one_d_sax = OneD_SymbolicAggregateApproximation(n_segments=n_paa_segments, alphabet_size_avg=n_sax_symbols_avg,
                                                    alphabet_size_slope=n_sax_symbols_slope, sigma_l=np.sqrt(0.03/(np.floor(len(ts)/n_paa_segments))))
    one_d_sax_dataset_inv = one_d_sax.inverse_transform(one_d_sax.fit_transform(ts))

    # Our oneD_SAX
    width = len(ts) // n_paa_segments
    onedsax = oneD_SAX(w = width, k_slope = n_sax_symbols_slope, k_intercept = n_sax_symbols_avg)
    onedsax_ts = onedsax.transform(ts)
    recon_onedsax = onedsax.inverse_transform(onedsax_ts)

    # plot
    plt.figure()
    plt.plot(ts, "b-", alpha=0.4)
    plt.plot(one_d_sax_dataset_inv[0].ravel(), "b-")
    plt.plot(recon_onedsax, 'r--')
    plt.legend(['original', 'tslearn 1D-SAX implementation', 'our 1D-SAX implementation'])
    plt.title("1dSAX, (%d, %d) symbols" % (n_sax_symbols_avg, n_sax_symbols_slope))
    plt.show()
