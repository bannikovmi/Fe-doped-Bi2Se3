import os

import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc

from matplotlib.patches import FancyArrowPatch, ArrowStyle

from scipy.optimize import curve_fit

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

density = 6.82 # [g/cm^3]

samples = {
   "272": {
      'x': 0,
      'mass': 0.03,
      'data': {},
      'max_y': 0.024,
      },
   "365": {
    'x': 0.015,
      'mass': 0.03,
      'data': {},
      'max_y': 0.2,
   },
   "367": {
    'x': 0.1,
      'mass': 0.03,
      'data': {},
      'max_y': 0.5,
   },
   "370": {
      'x': 0.04,
      'mass': 0.03,
      'data': {},
      'max_y': 1
   }
}

aem = 1.66e-24

m_Fe = 55.845 * aem
m_Se = 78.96 * aem
m_Bi = 208.98 * aem

mu_B = 927e-23 # emu

###################################################################################
## Fig setup
###################################################################################

fig = plt.figure(figsize=(8, 8), constrained_layout=False)
fig.patch.set_facecolor('white')

left_margin = 0.15
right_margin = 0.15
top_margin = 0.03
bottom_margin = 0.12
wspace = 1
hspace = 0

gs = fig.add_gridspec(nrows=3, ncols=1, left=left_margin, right=1-right_margin,
   bottom=bottom_margin, top=1-top_margin, wspace=wspace, hspace=hspace)

##############################################################################################
## Load data
##############################################################################################
for num in samples:
   
   data_dir = num

   for ind, fname in enumerate(os.listdir(data_dir)):

      temp = fname.split('.')[0].split('=')[1]
      samples[num]['data'][temp] = np.loadtxt(
         f"{data_dir}\\{fname}", delimiter='\t').transpose()

      length = len(samples[num]['data'][temp]) # 3 cols in some files, 2 in others

      samples[num]['data'][temp][0] *= 1e-4 # Convert Oe to T
      samples[num]['data'][temp][length-1] /= samples[num]['mass'] # Calculate moment per unit mass
      samples[num]['data'][temp][length-1] *= density # Convert to magnetization

      x = float(samples[num]['x'])
      if x != 0:
         mu = m_Fe + 2*m_Bi/x + (3+x)*m_Se/x
         samples[num]['N_Fe'] = samples[num]['mass'] / mu

##############################################################################################
## Configure axes
##############################################################################################
max_field = 4

# Sample 272
ax_272 = fig.add_subplot(gs[0, 0])
ax_272.annotate('(a)', xy=(0.02, 0.85), xycoords='axes fraction', fontsize=20)
ax_272.annotate('x=0', xy=(0.1, 0.85), xycoords='axes fraction', fontsize=20)

ax_272.set_xlabel(r"Field (T)", fontsize=20)
# ax_272.set_ylabel(r"Magnetization (A/m)", fontsize=20)
ax_272.tick_params(axis='both', which='major', direction='in',
   width=2, length=10, labelsize=15, **visible_ticks)
ax_272.tick_params(axis='both', which='minor', direction='in',
   width=1.5, length=6, labelsize=8, **visible_ticks)
ax_272.tick_params(axis='x', which='major', direction='in',
   width=0, length=6, labelsize=0, **visible_ticks)

ax_272.set_xlim(-max_field, max_field)
ax_272.set_ylim(-samples['272']['max_y'], samples['272']['max_y'])

# Sample 365
ax_365 = fig.add_subplot(gs[1, 0])
ax_365.annotate('(b)', xy=(0.02, 0.85), xycoords='axes fraction', fontsize=20)
ax_365.annotate('x=0.015', xy=(0.1, 0.85), xycoords='axes fraction', fontsize=20)

ax_365_tw = ax_365.twinx()

ax_365.set_xlabel(r"Field (T)", fontsize=20)
ax_365.set_ylabel(r"Magnetization ($10^3$ A/m)", fontsize=20)
ax_365.tick_params(axis='both', which='major', direction='in',
   width=2, length=10, labelsize=15, **visible_ticks)
ax_365.tick_params(axis='both', which='minor', direction='in',
   width=1.5, length=6, labelsize=8, **visible_ticks)
ax_365.tick_params(axis='x', which='major', direction='in',
   width=0, length=6, labelsize=0, **visible_ticks)

ax_365_tw.tick_params(axis='y', which='major', direction='in',
   width=2, length=10, labelsize=15)
ax_365_tw.tick_params(axis='y', which='minor', direction='in',
   width=1.5, length=6, labelsize=8)
ax_365_tw.set_ylabel(r"Magnetic moment per Fe atom ($\mu_B$)", fontsize=20)
ax_365_tw.yaxis.set_label_coords(1.1, 0)

ax_365.set_xlim(-max_field, max_field)
ax_365.set_ylim(-samples['365']['max_y'], samples['365']['max_y'])

per_atom_lim = samples['365']['max_y'] * samples['365']['mass'] / (
   density * mu_B * samples['365']['N_Fe'])
ax_365_tw.set_ylim(-per_atom_lim, per_atom_lim)

# Sample 367
ax_367 = fig.add_subplot(gs[2, 0])
ax_367.annotate('(c)', xy=(0.02, 0.85), xycoords='axes fraction', fontsize=20)
ax_367.annotate('x=0.1', xy=(0.1, 0.85), xycoords='axes fraction', fontsize=20)

ax_367_tw = ax_367.twinx()

ax_367.set_xlabel(r"Field (T)", fontsize=20)
ax_367.tick_params(axis='both', which='major', direction='in',
   width=2, length=10, labelsize=15, **visible_ticks)
ax_367.tick_params(axis='both', which='minor', direction='in',
   width=1.5, length=6, labelsize=8, **visible_ticks)

ax_367_tw.tick_params(axis='y', which='major', direction='in',
   width=2, length=10, labelsize=15)
ax_367_tw.tick_params(axis='y', which='minor', direction='in',
   width=1.5, length=6, labelsize=8)

ax_367.set_xlim(-max_field, max_field)
ax_367.set_ylim(-samples['367']['max_y'], samples['367']['max_y'])

per_atom_lim = samples['367']['max_y'] * samples['367']['mass'] / (
   density * mu_B * samples['367']['N_Fe'])
ax_367_tw.set_ylim(-per_atom_lim, per_atom_lim)

##############################################################################################
## Plot data
##############################################################################################
# substract line
def magnetic_fit(B, a, b, c):

   return a*B + b*np.tanh(c*B)

for temp in sorted(samples["272"]["data"], key=lambda x: int(x)):

   xdata = samples["272"]["data"][temp][0]
   ydata = samples["272"]["data"][temp][1]

   p0 = (0, 0.1, 1)
   popt, pcov = curve_fit(magnetic_fit, xdata, ydata, p0=p0)

   ysub = ydata - popt[0]*xdata

   ax_272.scatter(xdata, ysub, s=10, marker='s', lw=2, label=f'$T={temp}$ K')# ec='k', fc='k') 
   ax_272.plot(xdata, ysub, ls=':', c='k', lw=1)

for temp in sorted(samples["365"]["data"], key=lambda x: int(x)):

   if int(temp) == 30 or int(temp) == 100:
      continue

   xdata = samples["365"]["data"][temp][0]
   ydata = samples["365"]["data"][temp][1]

   p0 = (0, 1, 1)
   popt, pcov = curve_fit(magnetic_fit, xdata, ydata, p0=p0)

   ysub = ydata - popt[0]*xdata

   ax_365.scatter(xdata, ysub, s=10, marker='s', lw=2, label=f'$T={temp}$ K')# ec='k', fc='k') 
   ax_365.plot(xdata, ysub, ls=':', c='k', lw=1)

for temp in sorted(samples["367"]["data"], key=lambda x: int(x)):

   if int(temp) == 30:
      continue

   xdata = samples["367"]["data"][temp][0]
   ydata = samples["367"]["data"][temp][2]

   p0 = (0, 1, 1)
   popt, pcov = curve_fit(magnetic_fit, xdata, ydata, p0=p0)

   ysub = ydata - popt[0]*xdata

   ax_367.scatter(xdata, ysub, s=10, marker='s', lw=2, label=f'$T={temp}$ K')# ec='k', fc='k') 
   ax_367.plot(xdata, ysub, ls=':', c='k', lw=1)

ax_272.legend(loc='lower right', fontsize=15)
ax_365.legend(loc='lower right', fontsize=15)
ax_367.legend(loc='lower right', fontsize=15)

fig.savefig('Fe_magnetism.png')
fig.savefig('Fe_magnetism.pdf')
plt.show()
