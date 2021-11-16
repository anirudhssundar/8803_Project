import utils as ut
import poke_defs as poke

import numpy as np
import itertools
import RL_defs as rl
import copy
from tqdm import tqdm
import time

pokemon1 = poke.Squirtle()
pokemon2 = poke.Charmander()

import sys, os

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


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

poke.turn(pokemon1, pokemon2, move1, move4)
ut.summary(pokemon1)
ut.summary(pokemon2)


# RL stuff
HPs = np.arange(21)
attack_def_diff = np.arange(-6,7)

states = list(itertools.product(HPs, attack_def_diff))
state_key_dict = dict(zip(states, np.arange(len(states))))


key_state_dict = dict()
for k,v in state_key_dict.items():
    key_state_dict[v] = k

state_value_dict = dict(zip(states, np.zeros(len(states))))

actions = np.array([0,1])
state_action_paris = list(itertools.product(states, actions))

Q_dict = dict(zip(state_action_paris, np.zeros(len(state_action_paris))))

state_visit_count = dict(zip(states, np.zeros(len(states))))

init_state = (20,0)

action = move1

alpha = 0.5
gamma = 0.95

eps = 1e-4
iter_diff = eps + 3

start_time = time.time()
while iter_diff>eps:
    Q_init = copy.deepcopy(Q_dict)
    Q_init_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_init))

    with HiddenPrints():
        pokemon1 = poke.Squirtle()
        pokemon2 = poke.Charmander()
        while(pokemon2.HP>0):

            state = rl.get_state(pokemon1, pokemon2)
            action = np.random.choice([0,1]) # Choose actions randomly (epsilon greedy with eps = 0.5)
            if action==0:
                move = move1
            else:
                move = move2

            print(f"Squirtle used {move.name}")

            poke.turn(pokemon1, pokemon2, move, move4)

            new_state = rl.get_state(pokemon1, pokemon2)
            reward = rl.reward(new_state)

            Q_max = max([Q_dict[(t[0],t[1])] for t in list(Q_dict.keys()) if t[0]==new_state])

            # Q learning update
            Q_dict[(state,action)] = Q_dict[(state,action)] + \
                        alpha*(reward + gamma*(Q_max) - Q_dict[(state,action)])
    Q_iter_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_dict))

    iter_diff = abs(Q_init_norm - Q_iter_norm)
    iter_time = time.time()
    if (iter_time - start_time)//60 > 2:
        break


# Simulate a game
pokemon1 = poke.Squirtle()
pokemon2 = poke.Charmander()

init_state = (20,0)
state = init_state
moves = []
while (pokemon2.HP>0):
    value_action_0 = Q_dict[(state, 0)]
    value_action_1 = Q_dict[(state, 1)]

    if value_action_0 > value_action_1:
        move = move1
    else:
        move = move2
    poke.turn(pokemon1, pokemon2, move, move4)
    moves.append(move.name)
    state = rl.get_state(pokemon1, pokemon2)
