import sys
sys.path.insert(0, "../source")
from visualize import plot_bifurcation
import numpy as np
import pickle5 as pickle
import matplotlib.pyplot as plt

# ---- set up -----
top_dir = "dynamic/low_density/"
project_dirs = ["bifurc_pm0_onlyday" ]
labels = ["night", "day", "static"]
for idx, project in enumerate(project_dirs):
    benefit_values = np.linspace(1, 2.5, 10)

    data_file = "../projects/" + top_dir + "/" + project + "/log.pickle"
    data = pickle.load(open(data_file,"rb"))
    fixed_points = data["fixed_points"]
    plot_bifurcation(project, benefit_values, fixed_points, label=labels[idx])

plt.savefig("../projects/"  + top_dir + "/" + project + "/plots/bifurcation.png")
plt.clf()



