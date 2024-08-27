import os
import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import savgol_filter

from SdH_func import (
   epsilon,
   moving_average,
   remove_bg,
   symmetrize,
   find_extr
)

samples = {
   # "272": {
   #    'color': 'black',
   #    'label': r"Bi$_2$Se$_3$",
   #    'data': {},
   #    "b_ind": 2,
   #    "x_ind": 1,
   #    "osc_shift": 5e-6,
   #    'min_field': 10,
   #    'max_field': 15.6,
   #    'window_length': 200,
   #    'polyorder': 2,
   #    'deriv': 1,
   #    'n_extr': 10,
   #    'mins': {},
   #    'min_amps': {},
   #    'maxs': {},
   #    'max_amps': {},
   #    'expected_mins': [0.0647, 0.0701, 0.0753, 0.0806, 0.0859],
   #    'expected_maxs': [0.0675, 0.0729, 0.0782, 0.0835, 0.0889],
   #    'n0': 12,
   #    'osc_ind': [0],
   #    'fit_params': {}
   # },
   # "363": {
   #    'color': 'black',
   #    'label': r"(FeSe)$_{0.005}$+Bi$_2$Se$_3$",
   #    'data': {},
   #    "b_ind": 0,
   #    "x_ind": 3,
   #    "osc_shifts": [0, 3e-4, 4e-4, 5e-4],
   #    'min_field': 7,
   #    'max_field': 15.6,
   #    'window_length': 100,
   #    'polyorder': 1,
   #    'deriv': 1,
   #    'n_extr': 10,
   #    'mins': {},
   #    'min_amps': {},
   #    'maxs': {},
   #    'max_amps': {},
   #    'expected_mins': [0.0708 + i * (0.0803 - 0.0708) for i in range(6)],
   #    'expected_maxs': [0.0652 + i * (0.0750 - 0.0652) for i in range(6)],
   #    'n0': 9.4,
   #    'osc_ind': [0],
   #    'fit_params': {}
   # },   
   # "363": {
   #    'color': 'black',
   #    'label': r"(FeSe)$_{0.005}$+Bi$_2$Se$_3$",
   #    'data': {},
   #    "b_ind": 4,
   #    "x_ind": 3,
   #    "osc_shift": 1e-4,
   #    'min_field': 7,
   #    'max_field': 15.6,
   #    'window_length': 150,
   #    'polyorder': 1,
   #    'deriv': 1,
   #    'n_extr': 10,
   #    'mins': {},
   #    'min_amps': {},
   #    'maxs': {},
   #    'max_amps': {},
   #    'expected_mins': [0.0673, 0.0745, 0.0818, 0.0898, 0.0965, 0.1024, 0.1101, 0.1167, 0.1244, 0.1321],
   #    'expected_maxs': [0.0654, 0.0705, 0.0783, 0.0860, 0.0933, 0.0996, 0.1059, 0.1134, 0.1207, 0.1288],
   #    'n0': 9.4,
   #    'osc_ind': [2],
   #    'fit_params': {}
   # },
   "367": {
      'color': 'black',
      'label': r"(FeSe)$_{0.1}$+Bi$_2$Se$_3$",
      'data': {},
      "b_ind": 0,
      "x_ind": 1,
      "osc_shifts": [4e-3, 6e-3, 0, 2e-3],
      'min_field': 7,
      'max_field': 15.6,
      'window_length': 50,
      'polyorder': 1,
      'deriv': 1,
      'n_extr': 10,
      'mins': {},
      'min_amps': {},
      'maxs': {},
      'max_amps': {},
      'expected_mins': [0.06523 + i*(0.06902-0.06523) for i in range(20)],
      'expected_maxs': [0.06717 + i*(0.07095-0.06717) for i in range(20)],
      'n0': 17,
      'osc_ind': [0],
      'fit_params': {}
   },
}

#########################################################################################
### Load data
#########################################################################################
for num in samples.keys():

   data_dir = f"RB_curves\\{num}"
   hline_added = False

   for ind, fname in enumerate(os.listdir(data_dir)):
      temp = fname.removesuffix('.dat').removeprefix("T=")

      # Extract raw data, interpolate and symmetrize
      raw_data = np.loadtxt(f"{data_dir}\\{fname}", delimiter='\t').transpose()
      b_ind = samples[num]["b_ind"]
      x_ind = samples[num]["x_ind"]
      grid, sym = symmetrize(raw_data[b_ind], epsilon(raw_data[b_ind], raw_data[x_ind]))

      # Apply Savitzky-Golay filter
      window_length = samples[num]['window_length']
      polyorder = samples[num]['polyorder']
      deriv = samples[num]['deriv']
      sym_filt = savgol_filter(sym, window_length, polyorder, deriv)

      # Trim data
      max_field = samples[num]['max_field']
      min_field = samples[num]['min_field']
      grid, sym_filt = grid[grid<max_field], sym_filt[grid<max_field]
      grid, sym_filt = grid[grid>min_field], sym_filt[grid>min_field]

      # Load data to dict
      samples[num]['data'][temp] = np.array([grid, sym_filt])

      expected_mins = samples[num]['expected_mins']
      expected_maxs = samples[num]['expected_maxs']
      mins, min_amps = find_extr(1/grid, sym_filt, expected_mins)
      maxs, max_amps = find_extr(1/grid, sym_filt, expected_maxs)

      samples[num]['mins'][temp] = mins
      samples[num]['maxs'][temp] = maxs
      samples[num]['min_amps'][temp] = min_amps
      samples[num]['max_amps'][temp] = max_amps

      # plt.plot(grid, sym_filt, label=f"T={temp} K")
      # plt.scatter(mins, min_amps, c='k')
      # plt.scatter(maxs, max_amps, c='k')

      # if not hline_added:
      #    for x in mins:
      #       plt.axvline(x=x, ls='--', c='b')
      #    for x in maxs:
      #       plt.axvline(x=x, ls='--', c='r')
      # hline_added = True

# plt.legend(loc='best')
# plt.tight_layout()
# plt.show()