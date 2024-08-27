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
diffr_272 = np.transpose(np.loadtxt("data\\272\\272_Diffr.txt"))
diffr_367 = np.transpose(np.loadtxt("data\\367\\367_Diffr.txt"))
diffr_370 = np.transpose(np.loadtxt("data\\370\\370_Diffr_Poly.txt"))
diffr_371 = np.transpose(np.loadtxt("data\\371\\371_Diffr.txt"))

scan_272 = np.transpose(np.loadtxt("data\\272\\Bi2Se3_272_(0015)_phi_220.2_(2q_w).txt"))
scan_363 = np.transpose(np.loadtxt("data\\363-s1\\363-s1_(0015)_(2q_w).txt"))
scan_367 = np.transpose(np.loadtxt("data\\367\\367_(0015)_X_-2.6_(2q_w).txt"))
scan_371 = np.transpose(np.loadtxt("data\\371\\371_(0015)_X_0.84_(2q_w).txt"))

####################################################################################
### Figure and grids
####################################################################################

fig = plt.figure(figsize=(16, 8), constrained_layout=False)
fig.patch.set_facecolor('white')
left_margin = 0.07
right_margin = 0.02
top_margin = 0.05
bottom_margin = 0.1
wspace = 1
hspace = 0.5

gs = fig.add_gridspec(nrows=4, ncols=5, left=left_margin, right=1-right_margin,
	bottom=bottom_margin, top=1-top_margin, wspace=wspace, hspace=hspace)
gs_tight = fig.add_gridspec(nrows=10, ncols=5, left=left_margin, right=1-right_margin,
	bottom=bottom_margin, top=1-top_margin, wspace=wspace, hspace=0.2)

####################################################################################
### Full scans
####################################################################################

ax_diffr = fig.add_subplot(gs[:, 0:3])
ax_diffr.annotate('(a)', xy=(0.025, 0.95), xycoords='axes fraction', fontsize=20)

ax_diffr.set_ylabel("Intensity (a. u.)", fontsize=20)
ax_diffr.set_xlabel(r"$2\theta/\omega (^{\circ})$", fontsize=20)
ax_diffr.tick_params(axis='y', which='major', direction='in', width=2, length=7, labelsize=15, **visible_ticks)
ax_diffr.tick_params(axis='x', which='major', direction='in', width=2, length=7, labelsize=15, **visible_ticks)
ax_diffr.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)
ax_diffr.set_ylim(-0.3, 3.3)

ax_diffr.set_xticks(np.arange(0, 91, 10))
ax_diffr.set_xlim(6, 85)
x_minor_locator = AutoMinorLocator(5)
ax_diffr.xaxis.set_minor_locator(x_minor_locator)
ax_diffr.set_yticks([])

ax_diffr.plot(diffr_272[0], diffr_272[1]/max(diffr_272[1]), c='k', label=r"$x=0$")
ax_diffr.plot(diffr_367[0], diffr_367[1]/max(diffr_367[1])+1.1, c='olive', label=r"$x=0.1$")
ax_diffr.plot(diffr_371[0], diffr_371[1]/max(diffr_371[1])+2.2, c='red', label=r"$x=0.15$")

# ax_diffr.set_yscale('log')
ax_diffr.legend(loc="upper right", fontsize=15)

shifts = [3, 5, 5, 6, 6.5, 6, 5, 4]
for i in range(1, 9):
	ax_diffr.annotate(f'(00{3*i})', xy=(50/5*i-shifts[i-1], -0.18), fontsize=15)

# ####################################################################################
# ### 2 theta-omega scans
# ####################################################################################
ax_scan = fig.add_subplot(gs[0:2, 3:])
ax_scan.annotate('(b)', xy=(0.05, 0.9), xycoords='axes fraction', fontsize=20)

ax_scan.tick_params(axis='both', which='major', direction='in', width=2, length=7, labelsize=15, **visible_ticks)
ax_scan.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)
ax_scan.set_xlabel(r"$2\theta/\omega$ $(^{\circ})$", fontsize=20)
ax_scan.set_ylabel(r"Normalized Intensity", fontsize=20)

x_minor_locator = AutoMinorLocator(5)
y_minor_locator = AutoMinorLocator(5)
ax_scan.xaxis.set_minor_locator(x_minor_locator)
ax_scan.yaxis.set_minor_locator(y_minor_locator)
ax_scan.set_xlim([47.575, 47.645])
ax_scan.set_ylim([0, 1.1])

ax_scan.plot(scan_272[0], scan_272[1]/max(scan_272[1]), c='k', label='x=0')
ax_scan.plot(scan_363[0], scan_363[1]/max(scan_363[1]), c='teal', label='x=0.005')
ax_scan.plot(scan_367[0], scan_367[1]/max(scan_367[1]), c='olive', label='x=0.1')
ax_scan.plot(scan_371[0], scan_371[1]/max(scan_371[1]), c='red', label='x=0.15')

ax_scan.legend(loc="upper right", fontsize=15)

# ####################################################################################
# ### c-axis and a-axis parametres
# ####################################################################################
ax_c = fig.add_subplot(gs_tight[6:8, 3:])
ax_a = fig.add_subplot(gs_tight[8:, 3:])
ax_c.annotate('(c)', xy=(0.05, 0.1), xycoords='axes fraction', fontsize=20)
ax_a.annotate('(d)', xy=(0.05, 0.1), xycoords='axes fraction', fontsize=20)

x_min = -1e-4
x_max = 0.16

# c-axis
ax_c.set_xscale(mpl.scale.FuncScale(ax_c, (lambda x: np.sqrt(x-x_min), lambda x: x_min+x**2)))
# x_minor_locator = AutoMinorLocator(5)
# ax_c.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = AutoMinorLocator(5)
ax_c.yaxis.set_minor_locator(y_minor_locator)
ax_c.set_xlim(x_min, x_max)
ax_c.set_ylim(28.624, 28.636)
ax_c.set_xticks([0, 0.01, 0.05, 0.1, 0.15])
ax_c.set_xticks(np.concatenate([np.arange(0, 0.011, 0.002), np.arange(0, 0.15, 0.01)]), minor=True)

ax_c.set_ylabel(r"$c\,(\mathring{A})$ ", fontsize=20)
ax_c.tick_params(axis='both', which='major', direction='in', width=2, length=7, labelsize=15, **visible_ticks)
ax_c.tick_params(axis='x', labelsize=0)
ax_c.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)

ax_c.scatter(X, C, s=80, marker='d', ec='r', fc='w', lw=2) 
ax_c.axvline(x=0.07, lw=2, ls='--', c='k')

c_line = ([0, 0.04], [28.634, 28.625])
ax_c.plot(c_line[0], c_line[1], ls='--', lw=2, c='k')

# a-axis
ax_a.set_xscale(mpl.scale.FuncScale(ax_a, (lambda x: np.sqrt(x-x_min), lambda x: x_min+x**2)))
# x_minor_locator = AutoMinorLocator(5)
# ax_a.xaxis.set_minor_locator(x_minor_locator)
y_minor_locator = AutoMinorLocator(5)
ax_a.yaxis.set_minor_locator(y_minor_locator)
ax_a.set_xlim(x_min, x_max)
# ax_a.set_ylim(28.624, 28.636)

ax_a.set_xlabel(r"Nominal FeSe concentration", fontsize=20)
ax_a.set_ylabel(r"$a\,(\mathring{A})$ ", fontsize=20)
ax_a.tick_params(axis='both', which='major', direction='in', width=2, length=7, labelsize=15, **visible_ticks)
ax_a.tick_params(axis='both', which='minor', direction='in', width=1.5, length=4, labelsize=8, **visible_ticks)

ax_a.set_xticks([0, 0.01, 0.05, 0.1, 0.15])
ax_a.set_xticks(np.concatenate([np.arange(0, 0.011, 0.002), np.arange(0, 0.15, 0.01)]), minor=True)
ax_a.set_ylim(4.1385, 4.1415)
ax_a.scatter(X, A, s=80, marker='d', ec='r', fc='w', lw=2) 

fig.savefig('Fe_x-ray.png')
# fig.savefig('Fe_x-ray.pdf')
plt.show()

