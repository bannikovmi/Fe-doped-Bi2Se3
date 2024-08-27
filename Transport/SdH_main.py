import math, os, sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from scipy.optimize import curve_fit

# local imports
from SdH_samples import samples
from SdH_func import (
   hbar,
   k_B,
   m_0,
   q,
   epsilon,
   moving_average,
   remove_bg,
   symmetrize,
   LC_amp,
   LC_func,
   R_T,
   R_D,
)
from SdH_plots import SdH_figure
# rc('text', usetex=True)
# rc('text.latex',preamble=r'\usepackage[utf8]{inputenc}')
# rc('text.latex',preamble=r'\usepackage[russian]{babel}')
#########################################################################################
### Figures setup
#########################################################################################


for num in samples.keys():

   fig, ax = SdH_figure()
   ax_osc, ax_ext, ax_temp, ax_dng = ax

   fig.suptitle('Sample# ' + num + ' ' + samples[num]['label'], fontsize=20)

   ####################################################################################
   ### Oscillations
   ####################################################################################

   ax_osc.annotate('(a)', xy=(0.01, 0.95), xycoords='axes fraction', fontsize=20)

   x_min = 1/16.5
   x_max = 1/(samples[num]['min_field']-0.2)
   ax_osc.set_xlim(x_min, x_max)

   for ind, temp in enumerate(samples[num]['data'].keys()):

      # if float(temp)!=3:
      #    continue

      field = samples[num]['data'][temp][0]
      volts = samples[num]['data'][temp][1]

      shift = samples[num]["osc_shifts"][ind]

      color = cm.winter(float(temp)/30.0)
      ax_osc.plot(1/field, volts+shift, label=r'$T={temp}$K', color=color, lw=2)
      ax_osc.annotate(f'{temp}K', xy=(1/samples[num]['min_field']+1e-3, shift), fontsize=15)

      mins = samples[num]['mins'][temp]
      maxs = samples[num]['maxs'][temp]
      min_amps = samples[num]['min_amps'][temp]
      max_amps = samples[num]['max_amps'][temp]

      # ax_osc.scatter(mins, min_amps+shift, c='k')
      # ax_osc.scatter(maxs, max_amps+shift, c='r')

      # pvis = (1.5e-1, 2.7, 190, 590, samples[num]['m_c'])
      # popt = LC_fit(field, volts, T=3, p0=pvis)
      # print(popt)
      # ax_osc.plot(1/field, LC_func(field, 3, *popt)+shift, color=color, lw=1.5, ls='--')
      # ax_osc.plot(1/field, LC_func(field, float(temp), *pvis)+shift, color='k')

   ####################################################################################
   ### Extremums
   ####################################################################################
   y_min = 1/(samples[num]['max_field']+0.4)
   y_max = 1/(samples[num]['min_field']-0.4)

   ax_ext.annotate('(b)', xy=(0.05, 0.85), xycoords='axes fraction', fontsize=20)

   # ax_ext.set_ylim(y_min, y_max)
   for temp in samples[num]['mins'].keys():

      if float(temp) != 3:
         continue

      mins = samples[num]['mins'][temp]
      nu = np.array(range(len(mins)))

      a, b = np.polyfit(nu, mins, 1)
      
      n0 = samples[num]['n0']
      color = cm.winter(float(temp)/30.0)
      ax_ext.scatter(nu+n0, mins, color=color)
      ax_ext.axline((0, 0), slope=a, color=color, ls='--')

      ax_ext.set_xlim(n0-1, n0+len(mins)+1)
      ax_ext.set_ylim(0.85*min(mins), 1.15*max(mins))

      q = 1.6e-19
      hbar = 1.054e-34
      degeneracy = 2

      n_SdH = 2*np.pi*degeneracy*q/(hbar)/a
      print(f"{num}: n_SdH = {n_SdH:.3e}")
      samples[num]['n_SdH'] = n_SdH

   ####################################################################################
   ### Temperature dependencies
   ####################################################################################
   x_min = 0
   x_max = 35

   ax_temp.set_xlim(x_min, x_max)

   ax_temp.annotate('(c)', xy=(0.9, 0.85), xycoords='axes fraction', fontsize=20)

   temps_count = len(samples[num]['mins'].keys())
   temps = np.empty(temps_count)

   mins = np.empty(shape=(temps_count, len(samples[num]['osc_ind'])))
   maxs = np.empty(shape=(temps_count, len(samples[num]['osc_ind'])))
   min_amps = np.empty(shape=(temps_count, len(samples[num]['osc_ind'])))
   max_amps = np.empty(shape=(temps_count, len(samples[num]['osc_ind'])))
   
   for i, temp in enumerate(samples[num]['mins'].keys()):

      temps[i]=float(temp)
      
      for j, ind in enumerate(samples[num]['osc_ind']):
         
         mins[i, j] = samples[num]['mins'][temp][ind]
         maxs[i, j] = samples[num]['maxs'][temp][ind]
         min_amps[i, j] = samples[num]['min_amps'][temp][ind]
         max_amps[i, j] = samples[num]['max_amps'][temp][ind]

   t_sort = np.argsort(temps)
   ax_temp.set_xlim(0, max(temps)*1.15)

   for j, ind in enumerate(samples[num]['osc_ind']):
      
      amps = max_amps[t_sort, j]

      def fit_func(T, a, b):
         # here b = 2 pi^2 k_B m_c / hbar q B
         return a*T/np.sinh(b*T)

      ax_temp.scatter(temps[t_sort], amps, color=cm.hot(j/len(samples[num]['osc_ind'])))
      popt, pcov = curve_fit(fit_func, temps[t_sort], amps, p0=(1e-3, 1))

      B = 1 / mins[0, j]

      samples[num]['fit_params']['amp'] = popt[0]/popt[1]
      m_c = abs(popt[1]*hbar*q*B/(np.pi**2 * k_B))
      samples[num]['fit_params']['m_c'] = m_c

      print(f"{num}: m_c = {m_c:.3e} = {(m_c/9.1e-31):.2f} m_0")
      t_grid = np.linspace(0, max(temps)*1.2, 100)
      opt_grid = fit_func(t_grid, *popt)
      
      ax_temp.plot(t_grid, opt_grid)

   ####################################################################################
   ### Dingle plots
   ####################################################################################
   x_min = 1/16.5
   x_max = 1/(samples[num]['min_field']-0.4)

   ax_dng.annotate('(d)', xy=(0.9, 0.85), xycoords='axes fraction', fontsize=20)

   ax_dng.set_xlim(x_min, x_max)

   for temp in samples[num]['maxs'].keys():

      if float(temp) > 5:
         continue

      maxs = samples[num]['maxs'][temp]
      max_amps = abs(samples[num]['max_amps'][temp])

      color = cm.winter(float(temp)/30.0)
      B = 1/maxs
      T = float(temp)
      amp = samples[num]['fit_params']['amp']
      m_c = samples[num]['fit_params']['m_c']
   
      ax_dng.scatter(maxs, np.log(max_amps/R_T(B, T, amp, m_c)), color=color)
      a, b = np.polyfit(maxs, np.log(max_amps/R_T(B, T, amp, m_c)), deg=1)
      ylim = ax_dng.get_ylim()
      ax_dng.axline((0, b), slope=a, color='black', ls='--')
      ax_dng.set_ylim(ylim)

      # b = -k_B T_D/hbar omega_C
      T_D = abs(a*q*hbar/(m_c*k_B))
      tau_q = hbar/(2*np.pi*k_B*T_D)
      mu_SdH = q*tau_q/m_c
      print(f"{num}: tau_q = {tau_q:.3e} [s], mu_SdH = {1e4*mu_SdH:.1f} [cm^2/V*s]")
      samples[num]['fit_params']['T_D'] = T_D
      samples[num]['fit_params']['tau_q'] = tau_q
      samples[num]['fit_params']['mu_q'] = 1e4*q*tau_q/m_c

plt.savefig("SdH_figure.png")
plt.show()