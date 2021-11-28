import utils as ut
import numpy as np


class Squirtle:
    # Stats for a level 5 Squirtle
    name = 'Squritle'
    max_HP = 20
    max_atk = 11
    max_def = 13
    max_spd = 10

    atk = max_atk
    HP = max_HP
    defs = max_def
    spd = max_spd

    # Stat stages, used to calculate reduction in stats
    atk_stage = 0
    def_stage = 0

class Charmander:
    # Stats for a level 5 Charmander
    name = 'Charmander'
    max_HP = 20
    max_atk = 11
    max_def = 10
    max_spd = 13

    atk = max_atk
    HP = max_HP
    defs = max_def
    spd = max_spd

    # Stat stages, used to calculate reduction in stats
    atk_stage = 0
    def_stage = 0

class Bulbasaur:
    # Stats for a level 5 Bulbasaur
    name = 'Bulbasaur'
    max_HP = 21
    max_atk = 11
    max_def = 11
    max_spd = 11

    atk = max_atk
    HP = max_HP
    defs = max_def
    spd = max_spd

    # Stat stages, used to calculate reduction in stats
    atk_stage = 0
    def_stage = 0


class move:

    def __init__(self, name, isdmg, base_dmg, acc, stat_red):
        self.name = name
        self.isdmg = isdmg
        self.base_dmg = base_dmg
        self.acc = acc
        self.stat_red = stat_red # Reduces stats, 0=attack, 1=defense


def turn(pokemon1, pokemon2, pk1_move, pk2_move):
    """
    Simulate one turn of a battle
    Pokemon1: First pokemon
    Pokemon2: Second pokemon
    pk1_move: First pokemon action
    pk2_move: Second pokemon action
    """

    if pokemon1.spd > pokemon2.spd:
        if pk1_move.isdmg:
            dmg = ut.damage(pokemon1, pokemon2, pk1_move)
            pokemon2.HP = pokemon2.HP - dmg
        elif not(pk1_move.isdmg):
            ut.damage(pokemon1, pokemon2, pk1_move)
        if pokemon2.HP <=0:
            pokemon2.HP = 0
            print(f"{pokemon2.name} is unable to battle")
            return 1


        if pk2_move.isdmg:
            dmg = ut.damage(pokemon2, pokemon1, pk2_move)
            pokemon1.HP = pokemon1.HP - dmg
        elif not(pk2_move.isdmg):
            ut.damage(pokemon2, pokemon1, pk2_move)
        if pokemon1.HP <=0:
            pokemon1.HP = 0
            print(f"{pokemon1.name} is unable to battle")
            return 0




    if pokemon2.spd > pokemon1.spd:
        if pk2_move.isdmg:
            dmg = ut.damage(pokemon2, pokemon1, pk2_move)
            pokemon1.HP = pokemon1.HP - dmg
        elif not(pk2_move.isdmg):
            ut.damage(pokemon2, pokemon1, pk2_move)
        if pokemon1.HP <=0:
            pokemon1.HP = 0
            print(f"{pokemon1.name} is unable to battle")
            return 0

        if pk1_move.isdmg:
            dmg = ut.damage(pokemon1, pokemon2, pk1_move)
            pokemon2.HP = pokemon2.HP - dmg
        elif not(pk1_move.isdmg):
            ut.damage(pokemon1, pokemon2, pk1_move)
        if pokemon2.HP <=0:
            pokemon2.HP = 0
            print(f"{pokemon2.name} is unable to battle")
            return 1

    if pokemon1.spd == pokemon2.spd:
        # Speed tie, choose randomly
        cointoss = np.random.choice([0,1])
        if cointoss:
            if pk1_move.isdmg:
                dmg = ut.damage(pokemon1, pokemon2, pk1_move)
                pokemon2.HP = pokemon2.HP - dmg
            elif not(pk1_move.isdmg):
                ut.damage(pokemon1, pokemon2, pk1_move)
            if pokemon2.HP <=0:
                pokemon2.HP = 0
                print(f"{pokemon2.name} is unable to battle")
                return 1


            if pk2_move.isdmg:
                dmg = ut.damage(pokemon2, pokemon1, pk2_move)
                pokemon1.HP = pokemon1.HP - dmg
            elif not(pk2_move.isdmg):
                ut.damage(pokemon2, pokemon1, pk2_move)
            if pokemon1.HP <=0:
                pokemon1.HP = 0
                print(f"{pokemon1.name} is unable to battle")
                return 0
        else:
            if pk2_move.isdmg:
                dmg = ut.damage(pokemon2, pokemon1, pk2_move)
                pokemon1.HP = pokemon1.HP - dmg
            elif not(pk2_move.isdmg):
                ut.damage(pokemon2, pokemon1, pk2_move)
            if pokemon1.HP <=0:
                pokemon1.HP = 0
                print(f"{pokemon1.name} is unable to battle")
                return 0

            if pk1_move.isdmg:
                dmg = ut.damage(pokemon1, pokemon2, pk1_move)
                pokemon2.HP = pokemon2.HP - dmg
            elif not(pk1_move.isdmg):
                ut.damage(pokemon1, pokemon2, pk1_move)
            if pokemon2.HP <=0:
                pokemon2.HP = 0
                print(f"{pokemon2.name} is unable to battle")
                return 1


def sim_game(pokemon1, pokemon2, Q_dict, moves):

    init_state = (20,20,0)
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



"""
class tackle:
    name = 'tackle'
    base_dmg = 40
    acc = 95
"""
