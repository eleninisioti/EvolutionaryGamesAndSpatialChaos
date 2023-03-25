#!/bin/bash

for benefit in 1.5 2.2
do
 for day_duration in 1 2 3 
 do 
    for night_duration in 2 4 6 8
    do 
    	python simulate.py --project "dynamic/parametric_frequency/b_${benefit}_day_${day_duration}_night_${night_duration}" --grid_length 20 --init_coop 0.9 --rounds 100 --cost 0 --radius 1 --eval_movement --nagents 400 --trials 1 --prob_move 0.25 --benefit $benefit --day_duration $day_duration --night_duration $night_duration
    done
 done
done

