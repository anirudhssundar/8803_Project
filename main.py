import utils as ut
import poke_defs as poke

import numpy as np
import itertools
import RL_defs as rl
import copy
from tqdm import tqdm
import time
import pickle
import multiprocessing

# multiprocessing.set_start_method('fork')

pokemon1 = poke.Squirtle()
pokemon2 = poke.Charmander()

import sys, os

# Create various moves for the pokemon
move1 = poke.move(name='tackle',
                isdmg=1,
                base_dmg=50,
                acc=95,
                stat_red=None)

move2 = poke.move(name='tail whip',
                isdmg=0,
                base_dmg=0,
                acc=100,
                stat_red=1)

move3 = poke.move(name='growl',
                isdmg=0,
                base_dmg=0,
                acc=100,
                stat_red=0)

move4 = poke.move(name='snooze',
                isdmg=0,
                base_dmg=0,
                acc=-1,
                stat_red=None)

# poke.turn(pokemon1, pokemon2, move1, move4)
# ut.summary(pokemon1)
# ut.summary(pokemon2)

moves = [move1, move2, move3, move4]
alphas = np.arange(0.1, 0.9, 0.1)
# gammas = np.arange(0.1, 0.9, 0.3)

# hyperparams = list(itertools.product(alphas, gammas))

# paramslist = [[moves, i] for i in hyperparams]

for run in tqdm(range(20)):
    # convergence_times = np.zeros((len(alphas), len(gammas)))
    convergence_times = []
    # with multiprocessing.Pool(32) as pool:
    #     convergence_times = pool.map(rl.Q_learning_parallel, paramslist)

    # for row, alpha in enumerate(alphas):
    #     for col,gamma in enumerate(gammas):
    #        print(row, col)
    #        # Q_dict, convergence_time = rl.Q_learning_base(moves, alpha, gamma)
    #        convergence_time = rl.Q_learning_base(moves, alpha, gamma)
    #        convergence_times[row, col] = convergence_time
    gamma = 0.33
    for row, alpha in enumerate(alphas):
        convergence_time = rl.Q_learning_base(moves, alpha, gamma)
    convergence_times.append(convergence_time)
    with open(f'logs2/convergence_times_{run}.pickle', 'wb') as f:
        pickle.dump(convergence_times, f)

moves = [move1, move2, move3, move4]
alpha=0.25
gamma=0.9

convergence_time = rl.Q_learning_base(moves, alpha, gamma)
print(convergence_time)

# Q_dict, convergence_time = rl.Q_learning_attack_always(moves, alpha, gamma)

# Q_dict, convergence_time = rl.Q_learning_base_Char(moves, alpha=0.25, gamma=0.9)

# Q_dict, convergence_time = rl.Q_learning_attack_always_Char(moves, alpha=0.25, gamma=0.2)
# Simulate a game

"""
results = []
for i in range(100000):
    with ut.HiddenPrints():
        pokemon1 = poke.Squirtle()
        pokemon2 = poke.Charmander()

        init_state = (20,20,0)
        state = init_state
        played_moves = []
        while ((pokemon2.HP>0)and (pokemon1.HP>0)):
            value_action_0 = Q_dict[(state, 0)]
            value_action_1 = Q_dict[(state, 1)]

            if value_action_0 > value_action_1:
                move = move1
            else:
                move = move3
            t = poke.turn(pokemon1, pokemon2, move1, move1)
            # played_moves.append(move.name)
            state = rl.get_state(pokemon1, pokemon2)
        results.append(t)



# Simulate policy based situation
results = []
for i in tqdm(range(10000)):

    with ut.HiddenPrints():
        pokemon1 = poke.Bulbasaur()
        pokemon2 = poke.Squirtle()

        match_turn=1

        init_state = (20,20,0)
        state = init_state
        played_moves = []
        while ((pokemon2.HP>0)and (pokemon1.HP>0)):
            # value_action_0 = Q_dict[(state, 0)]
            # value_action_1 = Q_dict[(state, 1)]

            if match_turn==1:
                move_a = move3
                move_b = move2
            elif match_turn==2:
                move_a = move3
                move_b = move2
            elif match_turn==3:
                move_a= move1
                move_b = move1
            else:
                move_a = move1
                move_b = move1
            match_turn += 1
            t = poke.turn(pokemon1, pokemon2, move_a, move_b)
            # played_moves.append(move.name)
            state = rl.get_state(pokemon1, pokemon2)
        results.append(t)

print(np.mean(results))

pokemon1 = poke.Charmander()
pokemon2 = poke.Squirtle()
damages = []
for i in tqdm(range(100000)):
    with ut.HiddenPrints():
        damage = ut.damage(pokemon1, pokemon2, move1)
        damages.append(damage)


print(np.mean(damages))
"""
