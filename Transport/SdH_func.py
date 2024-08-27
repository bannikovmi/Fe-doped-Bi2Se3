import numpy as np
from scipy.optimize import curve_fit

# World constants
k_B = 1.38e-23 # Boltzmann constant
q = 1.6e-19 # Electron charge
hbar = 1.054e-34 # Planc'k constant
m_0 = 9.11e-31

#########################################################################################
### Data manipulation
#########################################################################################
def symmetrize(field, volts, sym=True):

   isort = np.argsort(field)

   field_range = max(field) - min(field)
   min_field = min(field) + 1e-3*field_range
   max_field = max(field) - 1e-3*field_range
   max_grid = min(abs(min_field), max_field)

   field_grid = np.linspace(-max_grid, max_grid, 10000)
   volts_int = np.interp(field_grid, field[isort], volts[isort])

   if sym:
      volts_sym = 0.5*(volts_int[:] + volts_int[::-1])
   else:
      volts_sym = 0.5*(volts_int[:] - volts_int[::-1])

   return field_grid[field_grid>0], volts_sym[field_grid>0]

def remove_bg(field, volts, sym=True):
   
   if sym:
      deg=6
   else:
      deg=5
   
   coeff = np.polyfit(field, volts, deg=deg)
   return volts - np.poly1d(coeff)(field)

def moving_average(volts, avg_counter):

   n_left = avg_counter // 2
   n_right = avg_counter - n_left

   ret = [np.mean(volts[max(0, i-n_left):min(i+n_right, len(volts))]) for i in range(len(volts))]

   return np.array(ret)

def epsilon(field, volts):
   
   ind = np.argmin(np.abs(field))
   return volts/volts[ind]-1

def find_extr(inv_field, volts, expected_extrs):

   expected_extrs = np.array(expected_extrs)
   extrs = np.empty(len(expected_extrs))
   extr_amps = np.empty(len(expected_extrs))

   extr_dist = np.mean(expected_extrs[1:]-expected_extrs[:-1])
   # print(extr_dist)

   for i in range(len(expected_extrs)):

      slice_left = expected_extrs[i] - 0.3*extr_dist
      slice_right = expected_extrs[i] + 0.3*extr_dist

      # print(slice_left, slice_right)

      f_slice, v_slice = inv_field, volts
      f_slice, v_slice = f_slice[f_slice>slice_left], v_slice[f_slice>slice_left]
      f_slice, v_slice = f_slice[f_slice<slice_right], v_slice[f_slice<slice_right]

      z = np.polyfit(f_slice, v_slice, 2)
      x0 = -0.5*z[1]/z[0]
      y0 = z[0]*x0**2+z[1]*x0+z[2]

      extrs[i] = x0
      extr_amps[i] = y0

   return extrs, extr_amps

# def find_extr(inv_field, volts, first_extr, second_extr, n_extr):

#    mins = []
#    maxs = []
#    min_amps = []
#    max_amps = []

#    extr_dist = second_extr - first_extr

#    for i in range(0, n_extr):
      
#       slice_left = first_extr + extr_dist*i - 0.3*extr_dist
#       slice_right = first_extr + extr_dist*i + 0.3*extr_dist

#       f_slice, v_slice = inv_field, volts
#       f_slice, v_slice = f_slice[f_slice>slice_left], v_slice[f_slice>slice_left]
#       f_slice, v_slice = f_slice[f_slice<slice_right], v_slice[f_slice<slice_right]

#       z = np.polyfit(f_slice, v_slice, 2)
#       x0 = -0.5*z[1]/z[0]
#       y0 = z[0]*x0**2+z[1]*x0+z[2]
      
#       if min(f_slice) < x0 < max(f_slice): # extr inside slice

#          if z[0] > 0: # min
#             mins.append(x0)
#             min_amps.append(y0)
#          else:
#             maxs.append(x0)
#             max_amps.append(y0)

#    mins, maxs = np.array(mins), np.array(maxs)
#    min_amps, max_amps = np.array(min_amps), np.array(max_amps)

#    return mins[::-1], maxs[::-1], min_amps[::-1], max_amps[::-1]

#########################################################################################
### Lifshitz-Cosevich
#########################################################################################
def R_T(B, T, amp, m_c):

	omega_c = q*B/m_c
	x = 2*np.pi**2*k_B*T/(hbar*omega_c)
	return amp*x/np.sinh(x)

def R_D(B, T_D, m_c):

	omega_c = q*B/m_c
	return np.exp(-k_B*T_D/(hbar*omega_c))

def osc(B, f, ph):

	return np.cos(2*np.pi*f/B + ph)

def LC_amp(B, T, amp, m_c, T_D):

	return R_T(B, T, amp, m_c) * R_D(B, T_D, m_c)

def LC_func(B, T, m_c, T_D, f, ph):

	return LC_amp(B, T, m_c, T_D) * osc(B, f, ph)

#########################################################################################
### Curve fitting
######################################################################################### 

def RT_fit(temps, amps, B, p0=None):

	def fit_func(T, a, m_c):
		return R_T(B, T, a, m_c)

	return curve_fit(fit_func, temps, amps, p0=p0)
