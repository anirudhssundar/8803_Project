import utils as ut
import poke_defs as poke

import numpy as np
import itertools
import RL_defs as rl
import copy
from tqdm import tqdm
import time
import sys, os


def get_state(pokemon1, pokemon2):
    state = (pokemon1.HP, pokemon2.HP, pokemon1.atk_stage - pokemon2.def_stage)
    return state


def reward(next_state):
    if next_state[1] == 0: # Check if pokemon 2 has 0 HP
        return 10
    elif next_state[0] == 0: # Check if pokemon 1 has 0 HP
        return -10
    else:
        return -1


def Q_learning_base(moves, alpha, gamma):

    move1 = moves[0]
    move2 = moves[1]
    move3 = moves[2]
    move4 = moves[3]
    HPs = np.arange(22)
    attack_def_diff = np.arange(-6,7)

    states = list(itertools.product(HPs, HPs, attack_def_diff))
    state_key_dict = dict(zip(states, np.arange(len(states))))


    key_state_dict = dict()
    for k,v in state_key_dict.items():
        key_state_dict[v] = k

    state_value_dict = dict(zip(states, np.zeros(len(states))))

    actions = np.array([0,1])
    state_action_pairs = list(itertools.product(states, actions))

    Q_dict = dict(zip(state_action_pairs, np.zeros(len(state_action_pairs))))

    state_visit_count = dict(zip(states, np.zeros(len(states))))

    # init_state = (20,20,0)

    action = move1

    # alpha = 0.25
    # gamma = 0.95

    eps = 1e-4
    iter_diff = eps + 3

    start_time = time.time()
    while iter_diff>eps:
        Q_init = copy.deepcopy(Q_dict)
        Q_init_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_init))

        with ut.HiddenPrints():
            pokemon1 = poke.Squirtle()
            pokemon2 = poke.Bulbasaur()
            while((pokemon2.HP>0) and (pokemon1.HP>0)):

                state = rl.get_state(pokemon1, pokemon2)
                action = np.random.choice([0,1]) # Choose actions randomly
                if action==0:
                    move = move1
                else:
                    move = move2

                print(f"Squirtle used {move.name}")

                poke.turn(pokemon1, pokemon2, move, move1)

                new_state = rl.get_state(pokemon1, pokemon2)
                reward = rl.reward(new_state)

                Q_max = max([Q_dict[(t[0],t[1])] for t in list(Q_dict.keys()) if t[0]==new_state])

                # Q learning update
                Q_dict[(state,action)] = Q_dict[(state,action)] + \
                            alpha*(reward + gamma*(Q_max) - Q_dict[(state,action)])
        Q_iter_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_dict))

        iter_diff = abs(Q_init_norm - Q_iter_norm)
        iter_time = time.time()
        if (iter_time - start_time)//60 > 5:
            print("TIMEOUT")
            break
    # return Q_dict, (iter_time - start_time)
    return iter_time - start_time


def Q_learning_attack_always(moves, alpha, gamma):

    """
    Opponent always attacks
    """

    move1 = moves[0]
    move2 = moves[1]
    move3 = moves[2]
    move4 = moves[3]
    HPs = np.arange(21)
    attack_def_diff = np.arange(-6,7)

    states = list(itertools.product(HPs, HPs, attack_def_diff))
    state_key_dict = dict(zip(states, np.arange(len(states))))


    key_state_dict = dict()
    for k,v in state_key_dict.items():
        key_state_dict[v] = k

    state_value_dict = dict(zip(states, np.zeros(len(states))))

    actions = np.array([0,1])
    state_action_pairs = list(itertools.product(states, actions))

    Q_dict = dict(zip(state_action_pairs, np.zeros(len(state_action_pairs))))

    state_visit_count = dict(zip(states, np.zeros(len(states))))

    init_state = (20,20,0)

    action = move1

    # alpha = 0.25
    # gamma = 0.95

    eps = 1e-4
    iter_diff = eps + 3

    start_time = time.time()
    while iter_diff>eps:
        Q_init = copy.deepcopy(Q_dict)
        Q_init_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_init))

        with ut.HiddenPrints():
            pokemon1 = poke.Squirtle()
            pokemon2 = poke.Charmander()
            while((pokemon2.HP>0) and (pokemon1.HP>0)):

                state = rl.get_state(pokemon1, pokemon2)
                action = np.random.choice([0,1]) # Choose actions randomly (epsilon greedy with eps = 0.5)
                if action==0:
                    move = move1
                else:
                    move = move2

                print(f"Squirtle used {move.name}")

                poke.turn(pokemon1, pokemon2, move, move1)

                new_state = rl.get_state(pokemon1, pokemon2)
                reward = rl.reward(new_state)

                Q_max = max([Q_dict[(t[0],t[1])] for t in list(Q_dict.keys()) if t[0]==new_state])

                # Q learning update
                Q_dict[(state,action)] = Q_dict[(state,action)] + \
                            alpha*(reward + gamma*(Q_max) - Q_dict[(state,action)])
        Q_iter_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_dict))

        iter_diff = abs(Q_init_norm - Q_iter_norm)
        iter_time = time.time()
        if (iter_time - start_time)//60 > 10:
            print("TIMEOUT")
            break
    return Q_dict, (iter_time - start_time)


def Q_learning_base_Char(moves, alpha, gamma):
    """
    Learn the optimal policy for Charmander
    """
    move1 = moves[0]
    move2 = moves[1]
    move3 = moves[2]
    move4 = moves[3]
    HPs = np.arange(21)
    attack_def_diff = np.arange(-6,7)

    states = list(itertools.product(HPs, HPs, attack_def_diff))
    state_key_dict = dict(zip(states, np.arange(len(states))))


    key_state_dict = dict()
    for k,v in state_key_dict.items():
        key_state_dict[v] = k

    state_value_dict = dict(zip(states, np.zeros(len(states))))

    actions = np.array([0,1])
    state_action_pairs = list(itertools.product(states, actions))

    Q_dict = dict(zip(state_action_pairs, np.zeros(len(state_action_pairs))))

    state_visit_count = dict(zip(states, np.zeros(len(states))))

    init_state = (20,20,0)

    action = move1

    # alpha = 0.25
    # gamma = 0.95

    eps = 1e-4
    iter_diff = eps + 3

    start_time = time.time()
    while iter_diff>eps:
        Q_init = copy.deepcopy(Q_dict)
        Q_init_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_init))

        with ut.HiddenPrints():
            pokemon1 = poke.Charmander()
            pokemon2 = poke.Squirtle()
            while((pokemon2.HP>0) and (pokemon1.HP>0)):

                state = rl.get_state(pokemon1, pokemon2)
                action = np.random.choice([0,1]) # Choose actions randomly (epsilon greedy with eps = 0.5)
                if action==0:
                    move = move1
                else:
                    move = move3

                print(f"{pokemon1.name} used {move.name}")

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
        if (iter_time - start_time)//60 > 10:
            print("TIMEOUT")
            break
    return Q_dict, (iter_time - start_time)


def Q_learning_attack_always_Char(moves, alpha, gamma):
    """
    Learn the optimal policy for Charmander
    """
    move1 = moves[0]
    move2 = moves[1]
    move3 = moves[2]
    move4 = moves[3]
    HPs = np.arange(21)
    attack_def_diff = np.arange(-6,7)

    states = list(itertools.product(HPs, HPs, attack_def_diff))
    state_key_dict = dict(zip(states, np.arange(len(states))))


    key_state_dict = dict()
    for k,v in state_key_dict.items():
        key_state_dict[v] = k

    state_value_dict = dict(zip(states, np.zeros(len(states))))

    actions = np.array([0,1])
    state_action_pairs = list(itertools.product(states, actions))

    Q_dict = dict(zip(state_action_pairs, np.zeros(len(state_action_pairs))))

    state_visit_count = dict(zip(states, np.zeros(len(states))))

    init_state = (20,20,0)

    action = move1

    # alpha = 0.25
    # gamma = 0.95

    eps = 1e-4
    iter_diff = eps + 3

    start_time = time.time()
    while iter_diff>eps:
        Q_init = copy.deepcopy(Q_dict)
        Q_init_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_init))

        with ut.HiddenPrints():
            pokemon1 = poke.Charmander()
            pokemon2 = poke.Squirtle()
            while((pokemon2.HP>0) and (pokemon1.HP>0)):

                state = rl.get_state(pokemon1, pokemon2)
                action = np.random.choice([0,1]) # Choose actions randomly (epsilon greedy with eps = 0.5)
                if action==0:
                    move = move1
                else:
                    move = move3

                print(f"{pokemon1.name} used {move.name}")

                poke.turn(pokemon1, pokemon2, move, move1)

                new_state = rl.get_state(pokemon1, pokemon2)
                reward = rl.reward(new_state)

                Q_max = max([Q_dict[(t[0],t[1])] for t in list(Q_dict.keys()) if t[0]==new_state])

                # Q learning update
                Q_dict[(state,action)] = Q_dict[(state,action)] + \
                            alpha*(reward + gamma*(Q_max) - Q_dict[(state,action)])
        Q_iter_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_dict))

        iter_diff = abs(Q_init_norm - Q_iter_norm)
        iter_time = time.time()
        if (iter_time - start_time)//60 > 10:
            print("TIMEOUT")
            break
    return Q_dict, (iter_time - start_time)


def Q_learning_parallel(params):

    moves = params[0]
    alpha = params[1][0]
    gamma = params[1][1]

    move1 = moves[0]
    move2 = moves[1]
    move3 = moves[2]
    move4 = moves[3]
    HPs = np.arange(22)
    attack_def_diff = np.arange(-6,7)

    states = list(itertools.product(HPs, HPs, attack_def_diff))
    state_key_dict = dict(zip(states, np.arange(len(states))))


    key_state_dict = dict()
    for k,v in state_key_dict.items():
        key_state_dict[v] = k

    state_value_dict = dict(zip(states, np.zeros(len(states))))

    actions = np.array([0,1])
    state_action_pairs = list(itertools.product(states, actions))

    Q_dict = dict(zip(state_action_pairs, np.zeros(len(state_action_pairs))))

    state_visit_count = dict(zip(states, np.zeros(len(states))))

    # init_state = (20,20,0)

    action = move1

    # alpha = 0.25
    # gamma = 0.95

    eps = 1e-3
    iter_diff = eps + 3

    start_time = time.time()
    while iter_diff>eps:
        Q_init = copy.deepcopy(Q_dict)
        Q_init_norm = np.linalg.norm(ut.dict_values_to_numpy(Q_init))

        with ut.HiddenPrints():
            pokemon1 = poke.Squirtle()
            pokemon2 = poke.Charmander()
            while((pokemon2.HP>0) and (pokemon1.HP>0)):

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
        if (iter_time - start_time)//60 > 10:
            print("TIMEOUT")
            break
    # return Q_dict, (iter_time - start_time)
    return iter_time - start_time
