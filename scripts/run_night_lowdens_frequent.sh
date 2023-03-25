#!/bin/bash

for benefit in 1.4 1.6 1.8
do
 for day_duration in 1 2 3
 do 
    for night_duration in 1 4 6
    do 
    	python simulate.py --project "dynamic/low_density/night_parametric_frequent/b_${benefit}_day_${day_duration}_night_${night_duration}" --grid_length 20 --init_coop 0.8 --rounds 400 --cost 0 --radius 1 --eval_movement --nagents 96 --trials 1 --prob_move 0.8 --benefit $benefit --day_duration $day_duration --night_duration $night_duration
    done
 done
done

