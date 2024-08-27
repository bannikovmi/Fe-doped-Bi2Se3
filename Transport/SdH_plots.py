import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.cm as cm

from matplotlib.patches import FancyArrowPatch, ArrowStyle
from matplotlib.ticker import AutoMinorLocator

major_ticks_params = {
	"direction": "in",
	"width": 2,
	"length": 7,
	"labelsize": 15,
	"top": False,
	"right": False
}

minor_ticks_params = {
	"direction": "in",
	"width": 1.5,
	"length": 4,
	"labelsize": 8,
	"top": False,
	"right": False
}

def SdH_figure():

	fig = plt.figure(figsize=(16, 8), constrained_layout=False)
	fig.patch.set_facecolor('white')

	left_margin = 0.08
	right_margin = 0.02
	top_margin = 0.08
	bottom_margin = 0.1
	wspace = 0.4
	hspace = 0.4

	gs = fig.add_gridspec(nrows=3, ncols=3, left=left_margin, right=1-right_margin,
    	bottom=bottom_margin, top=1-top_margin, wspace=wspace, hspace=hspace)

	####################################################################################
	### Oscillations
	####################################################################################

	ax_osc = fig.add_subplot(gs[0:2, :])

	ax_osc.set_ylabel(r"$\dfrac{d\rho_{xx}}{dB}$ (arb. units)", fontsize=20)
	ax_osc.set_xlabel(r"$1/B$ (T$^{-1}$)", fontsize=20)
	ax_osc.tick_params(axis='y', which='major', **major_ticks_params)
	ax_osc.tick_params(axis='x', which='major', **major_ticks_params)
	ax_osc.tick_params(axis='both', which='minor', **minor_ticks_params)

	x_minor_locator = AutoMinorLocator(5)
	ax_osc.xaxis.set_minor_locator(x_minor_locator)
	ax_osc.set_yticks([])

	####################################################################################
	### Extremums
	####################################################################################
	ax_ext = fig.add_subplot(gs[2, 0])

	ax_ext.set_ylabel(r"$1/B$ (T$^{-1}$)", fontsize=20)
	ax_ext.set_xlabel(r"$\nu$", fontsize=20)
	ax_ext.tick_params(axis='y', which='major', **major_ticks_params)
	ax_ext.tick_params(axis='x', which='major', **major_ticks_params)
	ax_ext.tick_params(axis='both', which='minor', **minor_ticks_params)

	x_minor_locator = AutoMinorLocator(5)
	y_minor_locator = AutoMinorLocator(5)
	ax_ext.xaxis.set_minor_locator(x_minor_locator)
	ax_ext.yaxis.set_minor_locator(y_minor_locator)

	####################################################################################
	### Temperature dependencies
	####################################################################################
	ax_temp = fig.add_subplot(gs[2, 1])

	ax_temp.set_ylabel(r"$A(B, T)$", fontsize=20)
	ax_temp.set_xlabel(r"$T$ (K)", fontsize=20)
	ax_temp.tick_params(axis='y', which='major', **major_ticks_params)
	ax_temp.tick_params(axis='x', which='major', **major_ticks_params)
	ax_temp.tick_params(axis='both', which='minor', **minor_ticks_params)

	x_min = 0
	x_max = 35

	ax_temp.set_xlim(x_min, x_max)

	x_minor_locator = AutoMinorLocator(5)
	y_minor_locator = AutoMinorLocator(5)
	ax_temp.xaxis.set_minor_locator(x_minor_locator)
	ax_temp.yaxis.set_minor_locator(y_minor_locator)

	####################################################################################
	### Temperature dependencies
	####################################################################################
	ax_dng = fig.add_subplot(gs[2, 2])

	ax_dng.set_ylabel(r"$\ln\dfrac{A(B, T)}{R_T(B, T)}$", fontsize=20)
	ax_dng.set_xlabel(r"$1/B$ (T$^{-1}$)", fontsize=20)
	ax_dng.tick_params(axis='y', which='major', **major_ticks_params)
	ax_dng.tick_params(axis='x', which='major', **major_ticks_params)
	ax_dng.tick_params(axis='both', which='minor', **minor_ticks_params)

	# x_min = 0
	# x_max = 35

	# ax_dng.set_xlim(x_min, x_max)

	x_minor_locator = AutoMinorLocator(5)
	y_minor_locator = AutoMinorLocator(5)
	ax_temp.xaxis.set_minor_locator(x_minor_locator)
	ax_temp.yaxis.set_minor_locator(y_minor_locator)
	
	ax = [ax_osc, ax_ext, ax_temp, ax_dng]
	
	return fig, ax

