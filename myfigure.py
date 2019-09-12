import numpy as np
import matplotlib as mpl
import matplotlib.font_manager

def myfigure(nrows=1, ncols=1, fig_ratio=0.71, fig_scale=1):
    """
    Parameters
    ----------
    nrows - int
        Number of rows (subplots)

    ncols - int
        Number of columns (subplots)

    fig_ratio - float
        Ratio between height and width

    fig_scale - float
        Scaling which magnifies font size

    Returns
    -------
    fig - matplotlib figure handle

    ax -  tuple of matplotlib axis handles

    Example
    -------
    from util import myfigure
    fig, (ax1, ax2) = myfigure(nrows=2, ncols=1)
    """
    size = 7

    l = 13.2/2.54
    fig, ax = mpl.pyplot.subplots(nrows=nrows, ncols=ncols, figsize=(l/fig_scale, l*fig_ratio/fig_scale), dpi=80*fig_scale, facecolor='w', edgecolor='k')
    mpl.pyplot.subplots_adjust(left=0.11*fig_scale, right=1-0.05*fig_scale, bottom=0.085*fig_scale/fig_ratio, top=1-0.05*fig_scale/fig_ratio)

    # Use tex and correct font

    mpl.rcParams['font.serif'] = ['computer modern roman']
    mpl.rcParams['mathtext.fontset'] = 'custom'
    mpl.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
    mpl.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
    mpl.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
    mpl.rcParams['font.size'] = size

    # MATLAB default (see MATLAB Axes Properties documentation)
    mpl.rcParams['legend.fontsize'] = size

    # remove margine padding on axis
    mpl.rcParams['axes.xmargin'] = 0
    mpl.rcParams['axes.ymargin'] = 0

    mpl.pyplot.tight_layout(pad=1.3) # padding

    # Save fig with transparent background
    mpl.rcParams['savefig.transparent'] = True

    # Make legend frame border black and face white
    mpl.rcParams['legend.edgecolor'] = 'k'
    mpl.rcParams['legend.facecolor'] = 'w'
    mpl.rcParams['legend.framealpha'] = 1

    # Change colorcycle to MATLABS
    c = mpl.cycler(color=['#0072BD', '#D95319', '#EDB120', '#7E2F8E', '#77AC30', '#4DBEEE', '#A2142F'])

    if isinstance(ax, np.ndarray):
        for axi in ax:
            axi.set_prop_cycle(c) # color cycle
            axi.xaxis.label.set_size(1.1*size) # xaxis font size
            axi.yaxis.label.set_size(1.1*size) # yaxis font size
            axi.tick_params(axis='both', which='both', labelsize=size, direction='in') # fix ticks
    else:
        ax.set_prop_cycle(c) # color cycle
        ax.tick_params(axis='both', which='both', labelsize=size, direction='in') # fix ticks
        ax.xaxis.label.set_size(1.1*size) # xaxis font size
        ax.yaxis.label.set_size(1.1*size) # yaxis font size

    return fig, ax
