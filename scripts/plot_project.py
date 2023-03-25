import sys
sys.path.insert(0, "../source")
from visualize import plot_coop_heatmap, plot_coop
import numpy as np
import pickle5 as pickle

# ---- set up -----
top_dir = "dynamic/low_density/night_parametric"
b_values = [1.4, 1.6, 1.8, 2.0]
day_values = [10, 20, 30, 40, 50]
night_values = [10, 20, 30, 40, 50]



fixed_points = np.zeros((len(b_values), 19))
for idx1, b in enumerate(b_values):
  day_night_ratios = []
  idx2 = 0
  for d in day_values:
    for n in night_values:
      if d/n not in day_night_ratios:
        day_night_ratios.append(d / n)
        idx2 += 1
        data_file = "../projects/" + top_dir + "/b_" + str(b) + "_day_" + str(d) + "_night_" + str(n) + "/log.pickle"
        data = pickle.load(open(data_file,"rb"))
        fixed_points[idx1, idx2-1] = data["coop_perc"][0][-1]
        print(d/n, b, data["coop_perc"][0][-1])


fixed_points = np.sort(fixed_points, axis=-1)
day_night_ratios.sort(reverse=True)
plot_coop_heatmap(project=top_dir, benefit_values=b_values,
                  day_night_ratios=day_night_ratios, fixed_points=fixed_points)

# top_dir = "dynamic/parametric_frequency"
# b_values = [1.0, 1.2, 1.5, 1.7, 2.0, 2.2]
# day_values = [2, 3]
# night_values = [2, 4, 6, 8]
# fixed_points = {}
# for idx1, b in enumerate(b_values):
#   frequencies = []
#   fixed_points[b]= []
#   idx2 = 0
#   for d in day_values:
#     for n in night_values:
#       freq = 1/(d+n)
#       if freq not in frequencies:
#         frequencies.append(freq)
#         idx2 += 1
#         data_file = "../projects/" + top_dir + "/b_" + str(b) + "_day_" + str(d) + "_night_" + str(n) + "/log.pickle"
#         data = pickle.load(open(data_file,"rb"))
#         fixed_points[b].append( data["coop_perc"][0][-1])
#
# plot_coop(project=top_dir, hor_axis_values=frequencies, hor_axis_label="f", coop_perc=fixed_points)