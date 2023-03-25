import argparse
from tournament import *
import os
from visualize import plot_grid, plot_bifurcation, plot_mixed, plot_coop_evol
import pickle
colors = {0: "blue", 1: "red",2: "green", 3: "yellow"  }
# 0: C->C, 1: D->D, 2: D -> C, 4: C-> D
import yaml
def main(args):

  # initialize project's subdirs

  if not os.path.exists("../projects/" + args.project + "/plots/grids"):
    os.makedirs("../projects/" + args.project + "/plots/grids")

  for trial in range(args.trials):
    if not os.path.exists("../projects/" + args.project + "/plots/trial_" + str(trial)):
      os.makedirs("../projects/" + args.project + "/plots/trial_" + str(trial))

  log_perf = {"coop_perc": [] }

  if args.bifurcation:
    benefit_values = np.linspace(1, 2.5, 10)
    fixed_points = [[] for _ in range(len(benefit_values))]

    for trial in range(args.trials):
      #fixed_points.append([])
      log_perf["coop_perc"].append([])

      for b_idx, benefit in enumerate(benefit_values):

        args.benefit = benefit
        tournament = Tournament(args)
        for round in range(args.rounds):
          log_round = tournament.play_round()
          if not os.path.exists("../projects/" + args.project + "/b_" + str(benefit) + "/trial_"+ str(trial) +  "/plots/grids"):
            os.makedirs("../projects/" + args.project + "/b_" + str(benefit) + "/trial_"+ str(trial) + "/plots/grids")
          plot_grid(strat_transitions=log_round["strat_transitions"],
                    round=round, project=args.project + "/b_" + str(benefit) + "/trial_"+ str(trial) )

          # consider that the last 10 rounds have converged
          # gather performance metrics

          pop_log = tournament.pop_log()
          if round  == (args.rounds-1):
            fixed_points[b_idx].append(pop_log["coop_perc"])

          log_perf["coop_perc"][trial].append(pop_log["coop_perc"])
      #plot_coop_evol(args.project, log_perf["coop_perc"][trial], trial, night=args.night_duration, trial=trial)


    log_perf["fixed_points"] = fixed_points
    plot_bifurcation(args.project, benefit_values, fixed_points)


  elif args.eval_movement:
    if args.move_parametric:
      p_movement_values = np.linspace(0, 1, 5)
    else:
      p_movement_values = [args.prob_move]
    print(p_movement_values)
    uniform_metric = []
    for p_idx, p in enumerate(p_movement_values):
      log_perf["coop_perc"].append([])
      args.prob_move = p
      if not os.path.exists("../projects/" + args.project + "/prob_move_" + str(p) + "/plots/grids"):
        os.makedirs("../projects/" + args.project + "/prob_move_" + str(p) + "/plots/grids")
      tournament = Tournament(args)
      logs = []
      for round in range(args.rounds):
        print("round is ", round)
        log_round = tournament.play_round()
        plot_grid(strat_transitions=log_round["strat_transitions"], round=round, project=args.project+ "/prob_move_" + str(p))
        logs.append(log_round)
        # gather performance metrics
        pop_log = tournament.pop_log()
        log_perf["coop_perc"][p_idx].append(pop_log["coop_perc"])

      pop_log = tournament.pop_log()
      uniform_metric.append(pop_log["uniform_day"])
      #print(uniform_metric)
    plot_coop_evol(project=args.project  + "/prob_move_" + str(p), parameter_values=p_movement_values,
                   parameter_label="$p_m$", coop_perc=log_perf["coop_perc"],
                   trial=0, night=args.night_duration)

    log_perf["uniform_metric"] = uniform_metric
    plot_mixed(project=args.project, prob_move=p_movement_values, metric=uniform_metric)

  else:
    if not os.path.exists("../projects/" + args.project + "/plots/grids"):
      os.makedirs("../projects/" + args.project + "/plots/grids")
    tournament = Tournament(args)
    logs = []
    for round in range(args.rounds):
      log_round = tournament.play_round()
      plot_grid(strat_transitions=log_round["strat_transitions"], round=round, project=args.project)
      logs.append(log_round)
      pop_log = tournament.pop_log()
      log_perf["coop_perc"].append(pop_log["coop_perc"])

  # ----- final saving for project ------
  with open("../projects/" + args.project + '/config.yml', 'w') as outfile:
    yaml.dump(args, outfile)
  with open('../projects/' + args.project + '/log.pickle', 'wb') as pfile:
    pickle.dump(log_perf, pfile, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()


  parser.add_argument('--project',
                      help='Name of current project',
                      type=str,
                      default="temp")

  parser.add_argument('--order',
                      help='Choose between CDO (combat-diffusion-offspring) and COD (combat-offspring-diffusion).',
                      type=str,
                      default="COD")

  parser.add_argument('--game',
                      help='Name of game. Choose between PD and Snow',
                      type=str,
                      default="PD")

  parser.add_argument('--grid_length',
                      help='Length of grid in tiles ',
                      type=int,
                      default=20)

  parser.add_argument('--radius',
                      help='Neighborhood radius ',
                      type=int,
                      default=20)


  parser.add_argument('--cost',
                      help='Cost of cooperation.',
                      type=float,
                      default=1)

  parser.add_argument('--benefit',
                      help='Benefit of cooperation.',
                      type=float,
                      default=10)



  parser.add_argument('--inter_per_round',
                      help='Interactions per round.',
                      type=int,
                      default=8)

  parser.add_argument('--init_coop',
                      help='Initial percentage of cooperators.',
                      type=float,
                      default=0.1)

  parser.add_argument('--prob_move',
                      help='Probability of moving during the day time.',
                      type=float,
                      default=0.1)

  parser.add_argument('--rounds',
                      help='Number of evolutionary rounds.',
                      type=int,
                      default=10)

  parser.add_argument('--trials',
                      help='Number of independent trials.',
                      type=int,
                      default=10)

  parser.add_argument('--day_duration',
                      help='Number of trials a day consists of',
                      type=int,
                      default=5)

  parser.add_argument('--night_duration',
                      help='Number of trials a night consists of',
                      type=int,
                      default=5)

  parser.add_argument('--nagents',
                      help='Number of agents',
                      type=int,
                      default=10)

  parser.add_argument('--well_mixed',
                      help='Number of evolutionary rounds.',
                      default=False,
                      action="store_true")

  parser.add_argument('--bifurcation',
                      help='Whether a bifurcation plot will be made.',
                      default=False,
                      action="store_true")

  parser.add_argument('--eval_movement',
                      help='Evaluate movement during daytime.',
                      default=False,
                      action="store_true")

  parser.add_argument('--move_parametric',
                      help='Evaluate different values of movement.',
                      default=False,
                      action="store_true")

  args = parser.parse_args()
  main(args)
