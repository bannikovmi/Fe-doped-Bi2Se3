import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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

####################################################################################
####################################################################################
### Fe_samples
####################################################################################
####################################################################################

Fe_samples = {
	# key -- sample number, (sr content, c, c_err, a, a_err)
	'272':	(0, 28.6343, 0, 4.1395, 0),
	'366':	(0.002, 28.63393, 0.00469, 4.14079,	4.0052E-4),
	'363':	(0.005, 28.6307, 0, 4.14003, 6.88165E-4),
	'365':	(0.015, 28.62972, 0.00175, 4.13983,	6.38553E-4),
	'370':	(0.04, 28.6255, 0, 4.13945,	0.00643),
	'367':	(0.1, 28.6333, 0, 4.14035, 7.07107E-5),
	'371':	(0.15, 28.62785, 0.00658, 4.14045, 4.94975E-4)
}

X = np.array([val[0] for val in Fe_samples.values()])
C = np.array([val[1] for val in Fe_samples.values()])
C_err = np.array([val[2] for val in Fe_samples.values()])
A = np.array([val[3] for val in Fe_samples.values()])
A_err = np.array([val[4] for val in Fe_samples.values()])

####################################################################################
### Load data
####################################################################################
diffr_367 = np.transpose(np.loadtxt("data\\367\\367_Diffr.txt"))
diffr_370 = np.transpose(np.loadtxt("data\\370\\370_Diffr_Poly.txt"))
diffr_371 = np.transpose(np.loadtxt("data\\371\\371_Diffr.txt"))

####################################################################################
### Figure and grids
####################################################################################

fig = plt.figure(figsize=(14, 8), constrained_layout=False)
fig.patch.set_facecolor('white')
small_margin = 0.05
large_margin = 0.1

gs_left = fig.add_gridspec(nrows=6, ncols=3, left=large_margin, right=1-small_margin,
	bottom=large_margin, top=1-small_margin, wspace=0.4, hspace=0)
gs_middle = fig.add_gridspec(nrows=6, ncols=3, left=large_margin, right=1-small_margin,
	bottom=large_margin, top=1-small_margin, wspace=0.4, hspace=1.5)
gs_right = fig.add_gridspec(nrows=6, ncols=3, left=large_margin, right=1-0.75*small_margin,
	bottom=large_margin, top=1-small_margin, wspace=0.4, hspace=1.5)

####################################################################################
### 2 theta/omega - scans
####################################################################################

ax_272scan = fig.add_subplot(gs_left[0:2, 0])
ax_367scan = fig.add_subplot(gs_left[2:4, 0])
ax_371scan = fig.add_subplot(gs_left[4:6, 0])

ax_272scan.tick_params(axis='y', which='major', direction='in', width=2, length=7, labelsize=20, **visible_ticks)
ax_272scan.tick_params(axis='x', which='major', direction='in', width=2, length=7, labelsize=0, **visible_ticks)
ax_272scan.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)
ax_272scan.set_xlim(0, 95)

ax_367scan.set_ylabel("Intensity (counts/s)", fontsize=25)
ax_367scan.tick_params(axis='y', which='major', direction='in', width=2, length=7, labelsize=20, **visible_ticks)
ax_367scan.tick_params(axis='x', which='major', direction='in', width=2, length=7, labelsize=0, **visible_ticks)
ax_367scan.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)
ax_367scan.set_xlim(0, 95)

ax_371scan.tick_params(axis='both', which='major', direction='in', width=2, length=7, labelsize=20, **visible_ticks)
ax_371scan.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)
ax_371scan.set_xlabel(r"$2\theta/\omega$ $(^{\circ})$", fontsize=25)
ax_371scan.set_xlim(0, 95)

x_minor_locator = AutoMinorLocator(5)
ax_272scan.xaxis.set_minor_locator(x_minor_locator)
ax_367scan.xaxis.set_minor_locator(x_minor_locator)
ax_371scan.xaxis.set_minor_locator(x_minor_locator)
ax_272scan.set_xticks(np.arange(0, 95, 15))
ax_367scan.set_xticks(np.arange(0, 95, 15))
ax_371scan.set_xticks(np.arange(0, 95, 15))

y_minor_locator = AutoMinorLocator(5)
ax_272scan.yaxis.set_minor_locator(y_minor_locator)
ax_367scan.yaxis.set_minor_locator(y_minor_locator)
ax_371scan.yaxis.set_minor_locator(y_minor_locator)

ax_272scan.annotate('(a)', xy=(0.05, 0.85), xycoords='axes fraction', fontsize=20)
ax_367scan.annotate('(b)', xy=(0.05, 0.85), xycoords='axes fraction', fontsize=20)
ax_371scan.annotate('(c)', xy=(0.05, 0.85), xycoords='axes fraction', fontsize=20)

# ax_272scan.plot(diffr_370[0], diffr_370[1], c='k')
ax_367scan.plot(diffr_367[0], diffr_367[1], c='k')
ax_371scan.plot(diffr_371[0], diffr_371[1], c='k')

ax_367scan.set_yscale('log')
ax_371scan.set_yscale('log')

####################################################################################
### Rocking curves
####################################################################################

ax_rock = fig.add_subplot(gs_middle[0:3, 1])
ax_scanHD = fig.add_subplot(gs_middle[3:6, 1])

ax_rock.tick_params(axis='both', which='major', direction='in', width=2, length=7, labelsize=20, **visible_ticks)
ax_rock.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)
ax_rock.set_xlabel(r"$\Delta\omega$ $(^{\circ})$", fontsize=25)
ax_rock.set_ylabel(r"Intensity (counts/s)", fontsize=25)
ax_rock.set_xlim(-1, 1)

x_minor_locator = AutoMinorLocator(5)
y_minor_locator = AutoMinorLocator(5)
ax_rock.xaxis.set_minor_locator(x_minor_locator)
ax_rock.yaxis.set_minor_locator(y_minor_locator)

ax_scanHD.tick_params(axis='both', which='major', direction='in', width=2, length=7, labelsize=20, **visible_ticks)
ax_scanHD.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)
ax_scanHD.set_xlabel(r"$2\theta/\omega$ $(^{\circ})$", fontsize=25)
ax_scanHD.set_ylabel(r"Normalized Intensity", fontsize=25)
ax_scanHD.set_xlim(-1, 1)

ax_scanHD.xaxis.set_minor_locator(x_minor_locator)
ax_scanHD.yaxis.set_minor_locator(y_minor_locator)

ax_rock.annotate('(d)', xy=(0.05, 0.9), xycoords='axes fraction', fontsize=20)
ax_scanHD.annotate('(e)', xy=(0.05, 0.9), xycoords='axes fraction', fontsize=20)

####################################################################################
### c-axis and a-axis
####################################################################################

ax_c = fig.add_subplot(gs_right[0:3, 2])
ax_a = fig.add_subplot(gs_right[3:6, 2])

ax_c.annotate('(f)', xy=(0.05, 0.9), xycoords='axes fraction', fontsize=20)
ax_a.annotate('(g)', xy=(0.05, 0.9), xycoords='axes fraction', fontsize=20)

x_min = -1e-4
x_max = 0.16
# c-axis
ax_c.set_xscale(mpl.scale.FuncScale(ax_c, (lambda x: np.sqrt(x-x_min), lambda x: x_min+x**2)))
x_minor_locator = AutoMinorLocator(5)
ax_c.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = AutoMinorLocator(5)
ax_c.yaxis.set_minor_locator(y_minor_locator)

ax_c.set_xlabel(r"Nominal FeSe concentration", fontsize=25)
ax_c.set_ylabel(r"$c\,(\mathring{A})$ ", fontsize=20)
ax_c.tick_params(axis='both', which='major', direction='in', width=2, length=7, labelsize=20, **visible_ticks)
ax_c.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)

# ax_c.errorbar(X, C, yerr=C_err, capsize=3, marker='s', markersize=10, c='k')
ax_c.scatter(X, C, s=80, marker='s', ec='k', fc='w', lw=2) 

ax_c.set_xlim(x_min, x_max)
ax_c.set_xticks([0, 0.05, 0.1, 0.15])
ax_c.set_ylim(28.624, 28.636)

# a-axis

ax_a.set_xscale(mpl.scale.FuncScale(ax_a, (lambda x: np.sqrt(x-x_min), lambda x: x_min+x**2)))
x_minor_locator = AutoMinorLocator(5)
ax_a.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = AutoMinorLocator(5)
ax_a.yaxis.set_minor_locator(y_minor_locator)

ax_a.set_xlabel(r"Nominal FeSe concentration", fontsize=25)
ax_a.set_ylabel(r"$a\,(\mathring{A})$ ", fontsize=25)
ax_a.tick_params(axis='both', which='major', direction='in', width=2, length=7, labelsize=20, **visible_ticks)
ax_a.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)

# ax_a.errorbar(X, A, yerr=A_err, ecolor='k', fmt='ob', capsize=3)
ax_a.scatter(X, A, s=80, marker='s', ec='k', fc='w', lw=2) 

ax_a.set_xlim(x_min, x_max)
ax_a.set_xticks([0, 0.05, 0.1, 0.15])
ax_a.set_ylim(4.1385, 4.1415)

fig.savefig('Fe_x-ray.png')
# fig.savefig('Fe_x-ray.pdf')
plt.show()

