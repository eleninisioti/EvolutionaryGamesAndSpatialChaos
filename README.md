# Evolutionary games and spatial chaos

This is an implementation of the paper [Evolutionary games and spatial chaos](https://www.nature.com/articles/359826a0)

## How to use

You can look into file ``environment.yml`` for package dependencies that you can automatically
install using:

``conda env create -f environment.yml``

You can run a simulation when you are under folder ``source`` by calling file ``simulate.py`` and providing the appropriate flags. 

For example

``python simulate.py --project test --grid_length 50 --init_coop 0.8 --rounds 1000``

will run a simulation with a grid-world of size 50x50 for 1000 rounds starting with 80% of the population being a cooperator. 
Images, videos and data files will be saved under a newly created directory ``projects/test``.

To get the fractal patterns that the Spatial Prisoner's Dilemma produces when its dynamics are chaotic you can run:

``python simulate.py --project chaos_test --benefit 1.9 --grid_length 50 --init_coop 0.99 --inter_per_round 1 --rounds 100``


![Any text here](visuals/chaos.gif)


Reducing the grid size will drastically reduce computation time.



