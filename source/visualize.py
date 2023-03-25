import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import seaborn as sns

colors = {0: np.array([0, 0, 255]), 1: np.array([255, 0, 0]), 2: np.array([0, 255, 0]), 3:
  np.array([255, 255, 0]), 4: np.array([128,128,128])  }
# 0: C->C, 1: D->D, 2: D -> C, 3: C-> D, 4: empty

def plot_coop(project, hor_axis_values, hor_axis_label, coop_perc):
  for label, values in coop_perc.items():
    inds = np.ndarray.tolist(np.array(hor_axis_values).argsort())
    values = np.ndarray.tolist(np.array(values)[inds])
    hor_axis_values.sort()
    plt.plot(hor_axis_values, values, label=label)
  plt.title("Evolution of cooperation")
  plt.xlabel(hor_axis_label)
  plt.ylabel("Fixed point, $C^*$")
  plt.legend()
  plt.savefig("../projects/" + project + "/plots/coop_" + hor_axis_label + ".png")
  plt.clf()

def plot_coop_evol(project, parameter_values, parameter_label, coop_perc, trial, night=False):
  """ Plots the evolution of the percentage of cooperation with the rounds of a single trial.
  """
  for p_idx, move_prob in enumerate(parameter_values):

    plt.plot(list(range(len(coop_perc[p_idx]))), coop_perc[p_idx],
             label=parameter_label + str(move_prob) + "," + str(night))
  plt.title("Evolution of cooperation")
  plt.xlabel("Round, $r$")
  plt.ylabel("Percentage of cooperators, $p_C$")
  plt.legend()

  plt.savefig("../projects/" + project + "/plots/evol_coop.png")
  plt.clf()

def plot_mixed(project, prob_move, metric):
  plt.plot(prob_move, metric)
  plt.title("Well-mxed population?")
  plt.xlabel("$p_m$")
  plt.ylabel("$D$")
  plt.savefig("../projects/" + project + "/plots/movement_day.png")
  plt.clf()

def plot_grid(strat_transitions, round, project):
  data_3d = np.ndarray(shape=(strat_transitions.shape[0],
                              strat_transitions.shape[1], 3), dtype=int)
  for i in range(0, strat_transitions.shape[0]):
    for j in range(0,strat_transitions.shape[1]):
      #print(strat_transitions[i][j])
      data_3d[i][j] = colors[strat_transitions[i][j].T]
  img = plt.imshow(data_3d,
                   origin="lower")
  plt.title("Round " + str(round))
  plt.xlabel("$x$")
  plt.ylabel("$y$")
  plt.savefig("../projects/" + project + "/plots/grids/round_" + str(round) + ".png")
  plt.clf()

def plot_bifurcation(project, benefit_values, fixed_points, label):
  print("plot bifurc")
  for idx, b in enumerate(benefit_values):
    points = fixed_points[idx]
    print(b, points)
    plt.plot([ b for _ in range(len(points))], points, 'o', color="black")

  plt.title("Bifurcation")
  plt.xlabel("$b$")
  plt.ylabel("$x^*$")
  #plt.legend()


def plot_coop_heatmap(project, benefit_values, day_night_ratios, fixed_points):
  """ Plots the fixed points for different values of benefit and day/night ratio.
  """

  plt.figure()
  ax = sns.heatmap(fixed_points.T, xticklabels=benefit_values, yticklabels=day_night_ratios)
  xlabels = ['{:3.1f}'.format(x) for x in benefit_values]
  ylabels = ['{:3.1f}'.format(y) for y in day_night_ratios]
  ax.set_xticks(ax.get_xticks())
  ax.set_xticklabels(xlabels)
  ax.set_yticks(ax.get_yticks())
  ax.set_yticklabels(ylabels)
  plt.title("Fixed points heatmap")
  plt.xlabel("$b$")
  plt.ylabel("$T_d/T_n$")
  plt.savefig("../projects/" + project + "/plots/heatmap.png")
  plt.clf()


