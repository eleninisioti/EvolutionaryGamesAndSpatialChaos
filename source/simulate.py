import argparse
from tournament import *
import os
from visualize import plot_grid, plot_bifurcation
import pickle
import imageio
import yaml
from os import walk

colors = {0: "blue", 1: "red", 2: "green", 3: "yellow"}
# 0: C->C, 1: D->D, 2: D -> C, 3: C-> D


def main(args):
    # initialize project's subdirs
    if not os.path.exists("../projects/" + args.project + "/plots/grids"):
        os.makedirs("../projects/" + args.project + "/plots/grids")



    log_perf = {"coop_perc": []}


    if not os.path.exists("../projects/" + args.project + "/plots/grids"):
        os.makedirs("../projects/" + args.project + "/plots/grids")
    tournament = Tournament(args)
    logs = []
    for round in range(args.rounds):
        if round%10 ==0:
            print("Round ", str(round))
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

    # make gif from plots
    filenames = next(walk("../projects/" + args.project + "/plots/grids"), (None, None, []))[2]  # [] if no file
    filenames.sort()
    with imageio.get_writer("../projects/" + args.project + '/movie.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread("../projects/" + args.project + "/plots/grids/" + filename)
            writer.append_data(image)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--project',
                        help='Name of current project',
                        type=str,
                        default="temp")

    parser.add_argument('--game',
                        help='Name of game. Choose between PD and Snow',
                        type=str,
                        default="PD")

    parser.add_argument('--grid_length',
                        help='Length of grid in tiles ',
                        type=int,
                        default=50)

    parser.add_argument('--radius',
                        help='Neighborhood radius ',
                        type=int,
                        default=1)

    parser.add_argument('--benefit',
                        help='Benefit of cooperation.',
                        type=float,
                        default=1.9)

    parser.add_argument('--inter_per_round',
                        help='Interactions per round.',
                        type=int,
                        default=1)

    parser.add_argument('--init_coop',
                        help='Initial percentage of cooperators.',
                        type=float,
                        default=0.999)

    parser.add_argument('--rounds',
                        help='Number of evolutionary rounds.',
                        type=int,
                        default=1000)



    parser.add_argument('--well_mixed',
                        help='Number of evolutionary rounds.',
                        default=False,
                        action="store_true")


    args = parser.parse_args()
    main(args)
