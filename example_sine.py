import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
from textwrap import wrap
from myfigure import myfigure

from TARZAN import TARZAN
from ABBA import ABBA
from SAX import SAX
from oneD_SAX import oneD_SAX

linspace = np.linspace(-np.pi/2, 8*np.pi-np.pi/2, 100)
healthy = np.sin(linspace)
healthy = list(healthy)

ts = healthy*2 + healthy[0:25]
ts_x = healthy + [ts[0]]*22 + healthy

mu = np.mean(ts+ts_x)
s = np.std(ts+ts_x)

ts -= mu
ts /= s
ts_x -= mu
ts_x /= s

# Full phase of sine wave every 25 time points
sax = SAX(w=5, k=9)
onedsax = oneD_SAX(w=5, k_slope=3, k_intercept=3)
abba = ABBA(tol=0.13687, scl=1, min_k=3, max_k=9, verbose=0) #0.15 #0.4

fig, (ax1, ax2, ax3, ax4, ax5) = myfigure(nrows=5, ncols=1, fig_ratio=0.71,  fig_scale=1)
plt.subplots_adjust(left=0.15, bottom=None, right=0.95, top=None, wspace=None, hspace=None)
ax1.set_xticks([], minor=False)
ax1.set_ylabel('R', rotation='horizontal', labelpad=20)
ax2.set_xticks([], minor=False)
ax2.set_ylabel('X', rotation='horizontal', labelpad=20)
ax3.set_xticks([], minor=False)
ax3.set_ylabel('SAX', rotation='horizontal', labelpad=35)
ax4.set_xticks([], minor=False)
ax4.set_ylabel('1d-SAX', rotation='horizontal', labelpad=35)
ax5.set_ylabel('ABBA', rotation='horizontal', labelpad=35)

# Reference time series
ax1.plot(ts)
ax1.axis([0, len(ts), -3, 3])

# Anomalous time series
ax2.plot(ts_x)
ax2.axis([0, len(ts), -3, 3])
ax2.axvspan(99, 125, color='grey', alpha=0.5)

# SAX
score = TARZAN(ts, ts_x, l=3, method=sax, relative=True)
ax3.plot(score, 'r')
ax3.axis([0, len(ts), 0, max(score)+0.5])
ax3.axhline(0.8, color='k', linestyle='--')
ax3.axvspan(99, 125, color='grey', alpha=0.5)

# 1D-SAX
score = TARZAN(ts, ts_x, l=3, method=onedsax, relative=True)
ax4.plot(score, 'r')
ax4.axis([0, len(ts), 0, max(score)+0.5])
ax4.axhline(0.8, color='k', linestyle='--')
ax4.axvspan(99, 125, color='grey', alpha=0.5)

# ABBA
score = TARZAN(ts, ts_x, l=2, method=abba, relative=True)
ax5.plot(score, 'r')
ax5.axis([0, len(ts), 0.0, max(score)+0.5])
ax5.axhline(0.3, color='k', linestyle='--')
ax5.axvspan(99, 125, color='grey', alpha=0.5)

# Save plot

plt.savefig('plots/sine_anomaly_detection.pdf')

# Plot reference data and anomaly data
fig, (ax1, ax2) = myfigure(nrows=2, ncols=1, fig_ratio=0.71,  fig_scale=1)
ax1.plot(ts)
ax1.axis([0, len(ts), -3, 3])
ax2.plot(ts_x)
ax2.axis([0, len(ts), -3, 3])
plt.savefig('plots/sine.pdf')

# Plot SAX representations for both time series
fig, (ax1, ax2) = myfigure(nrows=2, ncols=1, fig_ratio=0.71,  fig_scale=1)
fig.subplots_adjust(hspace=1)
ax1.plot(ts)
str = sax.transform(ts)
recon_SAX_R = sax.inverse_transform(str)
ax1.plot(recon_SAX_R)
ax1.axis([0, len(ts), -3, 3])
ax1.set_title("\n".join(wrap(str, 120)), fontsize=6)
ax2.plot(ts_x)
str = sax.transform(ts_x)
recon_SAX_X = sax.inverse_transform(str)
ax2.plot(recon_SAX_X)
ax2.axis([0, len(ts), -3, 3])
ax2.set_title("\n".join(wrap(str, 120)), fontsize=6)
plt.savefig('plots/sine_SAX.pdf')

# Plot 1d-SAX representations for both time series
fig, (ax1, ax2) = myfigure(nrows=2, ncols=1, fig_ratio=0.71,  fig_scale=1)
fig.subplots_adjust(hspace=1)
ax1.plot(ts)
str = onedsax.transform(ts)
recon_1dSAX_R = onedsax.inverse_transform(str)
ax1.plot(recon_1dSAX_R)
ax1.axis([0, len(ts), -3, 3])
ax1.set_title("\n".join(wrap(str, 120)), fontsize=6)
ax2.plot(ts_x)
str = onedsax.transform(ts_x)
recon_1dSAX_X = onedsax.inverse_transform(str)
ax2.plot(recon_1dSAX_X)
ax2.axis([0, len(ts), -3, 3])
ax2.set_title("\n".join(wrap(str, 120)), fontsize=6)
plt.savefig('plots/sine_oneD-SAX.pdf')

# Plot ABBA representations for both time series
pieces1 = abba.compress(ts)
pieces2 = abba.compress(ts_x)
pieces = np.vstack([pieces1, pieces2])
length_ref = len(pieces1)
symbolic_ts, centers = abba.digitize(pieces)
print('ABBA length:', length_ref)
r = symbolic_ts[0:length_ref]
x = symbolic_ts[length_ref::]

fig, (ax1, ax2) = myfigure(nrows=2, ncols=1, fig_ratio=0.71,  fig_scale=1)
fig.subplots_adjust(hspace=1)
ax1.plot(ts)
recon_ABBA_R = abba.inverse_transform(r, centers, ts[0])
ax1.plot(recon_ABBA_R)
ax1.axis([0, len(ts), min([min(recon_ABBA_R), min(ts)]), max([max(recon_ABBA_R), max(ts)])])
ax1.set_title("\n".join(wrap(r, 120)), fontsize=6)
ax2.plot(ts_x)
recon_ABBA_X = abba.inverse_transform(x, centers, ts_x[0])
ax2.plot(recon_ABBA_X)
ax2.axis([0, len(ts), min([min(recon_ABBA_X), min(ts_x)]), max([max(recon_ABBA_X), max(ts_x)])])
ax2.set_title("\n".join(wrap(x, 120)), fontsize=6)
plt.savefig('plots/sine_ABBA.pdf')


fig, (ax1, ax2) = myfigure(nrows=2, ncols=1, fig_ratio=0.71,  fig_scale=1)
plt.subplots_adjust(left=0.1, bottom=None, right=0.95, top=0.9, wspace=None, hspace=None)
ax1.plot(ts, 'k', label='original')
ax1.plot(recon_SAX_R, '--', label='SAX')
ax1.plot(recon_1dSAX_R, '-.', label='1D-SAX')
ax1.plot(recon_ABBA_R, ':', label='ABBA')
ax1.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, 1.2))
ax1.axis([0, 225, -2, 2])
ax2.plot(ts_x, 'k', label='original')
ax2.plot(recon_SAX_X, '--', label='SAX')
ax2.plot(recon_1dSAX_X, '-.', label='1D-SAX')
ax2.plot(recon_ABBA_X, ':', label='ABBA')
ax1.set_xticks([], minor=False)
ax1.set_ylabel('R', rotation='horizontal', labelpad=15)
ax2.set_ylabel('X', rotation='horizontal', labelpad=15)
ax2.axis([0, 225, -2, 2])
plt.savefig('plots/sine_symbolic_rep.pdf')
