import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc

from matplotlib.patches import FancyArrowPatch, ArrowStyle

# rc('text', usetex=True)
# rc('text.latex',preamble=r'\usepackage[utf8]{inputenc}')
# rc('text.latex',preamble=r'\usepackage[russian]{babel}')

visible_ticks = {
   "top": False,
   "right": False
}

from matplotlib.ticker import AutoMinorLocator

def symmetrize(field, volts, sym=True):

	isort = np.argsort(field)
	field, volts = field[isort], volts[isort]

	field_range = max(field) - min(field)
	min_field = min(field) + 1e-3*field_range
	max_field = max(field) - 1e-3*field_range
	grid_max = min(abs(min_field), max_field)

	field_grid = np.linspace(-grid_max, grid_max, 1000)
	volts_int = np.interp(field_grid, field, volts)

	if sym:
		volts_sym = 0.5*(volts_int[:] + volts_int[::-1])
	else:
		volts_sym = 0.5*(volts_int[:] - volts_int[::-1])

	return np.array([field_grid, volts_sym])

def epsilon(field, volts):
	
	ind = np.argmin(np.abs(field))
	return volts/volts[ind]-1


####################################################################################
####################################################################################
### Fe_samples
####################################################################################
####################################################################################

Fe_samples = {
	# key -- sample number, (sr content, n, mu)
	'272':	(0, 0.8, 2000),
	'366':	(0.002, 1.3, 8630),
	'363':	(0.005, 1.0, 5600),
	'365':	(0.015, 2.9, 2100),
	'370':	(0.04, 4.2, 2620),
	'367':	(0.1, 4.4, 1190),
	'371':	(0.15, 4.1, 1140)
}

X = np.array([val[0] for val in Fe_samples.values()])
n = np.array([val[1] for val in Fe_samples.values()])
mu = np.array([val[2] for val in Fe_samples.values()])

###################################################################################
## Fig setup
###################################################################################

fig = plt.figure(figsize=(16, 8), constrained_layout=False)
fig.patch.set_facecolor('white')

left_margin = 0.05
right_margin = 0.02
top_margin = 0.05
bottom_margin = 0.1
wspace = 1
hspace = 0.35

gs = fig.add_gridspec(nrows=2, ncols=5, left=left_margin, right=1-right_margin,
	bottom=bottom_margin, top=1-top_margin, wspace=wspace, hspace=hspace)

###################################################################################
## RB-curves
###################################################################################

ax_sdh = fig.add_subplot(gs[:, 2:])
ax_sdh.annotate('(c)', xy=(0.025, 1.025), xycoords='axes fraction', fontsize=20)

# Load data
RB_272 = np.transpose(np.loadtxt("RB_curves\\272.dat"))
RB_367 = np.transpose(np.loadtxt("RB_curves\\367.dat"))
RB_363 = np.transpose(np.loadtxt("RB_curves\\363.dat"))
RB_366 = np.transpose(np.loadtxt("RB_curves\\366.dat"))

# Symmetrize some curves
RB_272_x = symmetrize(RB_272[2], RB_272[1], sym=True)
RB_363_x = symmetrize(RB_363[0], RB_363[1], sym=True)
RB_366_x = symmetrize(RB_366[0], RB_366[1], sym=True)
RB_367_x = symmetrize(RB_367[0], RB_367[1], sym=True)

# Scale curves
RB_272_x[1] = epsilon(*RB_272_x)
RB_366_x[1] = epsilon(*RB_366_x)
RB_363_x[1] = epsilon(*RB_363_x)
RB_367_x[1] = epsilon(*RB_367_x)


# Setup axis
x_minor_locator = AutoMinorLocator(5)
ax_sdh.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = AutoMinorLocator(5)
ax_sdh.yaxis.set_minor_locator(y_minor_locator)

ax_sdh.set_xlim(0, 16.3)
# ax_sdh.set_ylim(0, 4.5)

ax_sdh.set_xlabel(r"Field (T)", fontsize=20)
ax_sdh.set_ylabel(" "*10+r"$\Delta\rho_{xx}(B)/\rho_{xx}(0)$", fontsize=20)
ax_sdh.tick_params(axis='both', which='major', direction='in', width=2, length=10, labelsize=15, **visible_ticks)
ax_sdh.tick_params(axis='both', which='minor', direction='in', width=1.5, length=6, labelsize=8, **visible_ticks)
# ax_sdh.tick_params(axis='y', which='major', direction='in', width=1.5, length=6, labelsize=0, **visible_ticks)

ax_sdh.plot(RB_272_x[0], RB_272_x[1], c='k', lw=1.5, label='x=0')
ax_sdh.plot(RB_366_x[0], RB_366_x[1], c='navy', lw=1.5, label='x=0.002')
ax_sdh.plot(RB_363_x[0], RB_363_x[1], c='teal', lw=1.5, label='x=0.005')
ax_sdh.plot(RB_367_x[0], RB_367_x[1], c='olive', lw=1.5, label='x=0.1')

ax_sdh.legend(loc='upper left', fontsize=15)

###################################################################################
## RT-curves
###################################################################################

ax_rt = fig.add_subplot(gs[0, 0:2])
ax_rt.annotate('(a)', xy=(0.05, 1.05), xycoords='axes fraction', fontsize=20)

# Load data
RT_272 = np.transpose(np.loadtxt("RT_curves\\272.dat"))
RT_366 = np.transpose(np.loadtxt("RT_curves\\366.dat"))
RT_367 = np.transpose(np.loadtxt("RT_curves\\367.dat"))
RT_371 = np.transpose(np.loadtxt("RT_curves\\371.dat"))

# Setup axis
x_minor_locator = AutoMinorLocator(5)
ax_rt.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = AutoMinorLocator(5)
ax_rt.yaxis.set_minor_locator(y_minor_locator)

ax_rt.set_xlim(0, 300)
# ax_rt.set_ylim(0, 4.5)

ax_rt.set_xlabel(r"Temperature (K)", fontsize=20)
ax_rt.set_ylabel(r"$\rho\,($mOhm$\times$cm)", fontsize=20)
ax_rt.tick_params(axis='both', which='major', direction='in',
	width=2, length=10, labelsize=15, **visible_ticks)
ax_rt.tick_params(axis='both', which='minor', direction='in',
	width=1.5, length=6, labelsize=8, **visible_ticks)

ax_rt.plot(RT_272[0], RT_272[1], c='k', label='x=0', lw=2)
ax_rt.plot(RT_366[0], RT_366[1], c='navy', label='x=0.002', lw=2)
ax_rt.plot(RT_367[0], RT_367[1], c='olive', label='x=0.1', lw=2)
ax_rt.plot(RT_371[0], RT_371[1], c='red', label='x=0.15', lw=2)

ax_rt.legend(loc='upper left', fontsize=15)

###################################################################################
## n, mu vs T graphs
###################################################################################

ax_hall = fig.add_subplot(gs[1, 0:2])
ax_hall.annotate('(b)', xy=(0.05, 1.05), xycoords='axes fraction', fontsize=20)

x_min = -0.001

ax_hall.set_xscale(mpl.scale.FuncScale(ax_hall, (lambda x: np.sqrt(x-x_min), lambda x: x_min+x**2)))
x_minor_locator = AutoMinorLocator(5)
ax_hall.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = AutoMinorLocator(5)
ax_hall.yaxis.set_minor_locator(y_minor_locator)

ax_hall.set_xlim(x_min, 0.17)
ax_hall.set_ylim(0, 5)
ax_hall.set_xticks([0, 0.05, 0.1, 0.15])

ax_hall.set_xlabel(r"Nominal FeSe concentration $x$", fontsize=20)
ax_hall.set_ylabel(r"$n_{Hall}\,(10^{19}$cm$^{-3})$", fontsize=20)
ax_hall.tick_params(axis='both', which='major', direction='in', width=2, length=10, labelsize=15, **visible_ticks)
ax_hall.tick_params(axis='both', which='minor', direction='in', width=1.5, length=6, labelsize=8, **visible_ticks)

# ax_hall.annotate('', xy=(0.00001, 1.5), xytext=(0.006, 1.5), arrowprops=dict(facecolor='black', shrink=0.05))

ax_hall.scatter(X, n, s=80, marker='s', ec='k', fc='k', lw=2) 
ax_hall.plot(X, n, ls=':', c='k', lw=1)

# Mobilities

ax_mu = ax_hall.twinx()
ax_mu.set_ylabel(r"$\mu\,$($10^3$cm$^2$/(V$\times$s))", fontsize=20, color='red')

ax_mu.set_ylim(0, 12)
ax_mu.set_yscale(mpl.scale.FuncScale(ax_hall, (lambda x: np.sqrt(x), lambda x: x**2)))
y_minor_locator = AutoMinorLocator(5)
ax_mu.yaxis.set_minor_locator(y_minor_locator)

ax_mu.tick_params(axis='y', which='major', direction='in', width=2, length=7, labelsize=15, colors='red')
ax_mu.tick_params(axis='y', which='minor', direction='in', width=0, length=4, labelsize=8, colors='red')
ax_mu.spines['right'].set_color('red')
ax_mu.set_yticks([0, 1, 2.5, 5, 10])

ax_mu.scatter(X, 1e-3*mu, s=100, marker='^', c='r') 
ax_mu.plot(X, 1e-3*mu, ls='--', c='r', lw=1)

# ax_mu.annotate('', xy=(0.16, 2), xytext=(0.07, 2), arrowprops=dict(facecolor='black', shrink=0.05))

fig.tight_layout()

fig.savefig('Fe_transport.png')
plt.show()