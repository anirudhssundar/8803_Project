import numpy as np
import functools
import os,sys

def damage(pokemon1, pokemon2, move):

    if move.isdmg:
    # If the move is a damage-dealing move:
        is_miss = np.random.randint(0,100)
        is_crit = np.random.randint(0,100)
        if is_miss > move.acc:
            print(f"{pokemon1.name}'s {move.name} missed!'")
            return 0.0

    # NOT CONSIDERING CRITS FOR KICKS
        elif is_crit < 16:
            print("It's a critical hit!")
            Level = 5 # Attacker's level
            AttackStat = max(pokemon1.max_atk,
                            pokemon1.atk * get_stat_multiplier(pokemon1.atk_stage)) # Reduction in attack not considered in crits!
            DefenseStat = min(pokemon2.defs* get_stat_multiplier(pokemon2.def_stage),
                                pokemon2.max_def)# Defender's defense
            AttackPower = move.base_dmg # Move's base damage

            STAB = 1 # STAB (not being considered)
            Resistance = 1 # Effectiveness (not being considered)

            RandomNumber = np.random.randint(85, 101) # Damage modifier


            dmg = 2*((((2*Level/5 + 2) *AttackStat * AttackPower / DefenseStat) / 50) + 2) * STAB * Resistance * RandomNumber / 100

            dmg_round = np.floor(dmg)
            return dmg_round
        else:
            Level = 5 # Attacker's level
            AttackStat = pokemon1.atk * get_stat_multiplier(pokemon1.atk_stage) # Attacker's  attack stat
            DefenseStat = pokemon2.defs * get_stat_multiplier(pokemon2.def_stage) # Defender's defense
            AttackPower = move.base_dmg # Move's base damage

            STAB = 1 # STAB (not being considered)
            Resistance = 1 # Effectiveness (not being considered)

            RandomNumber = np.random.randint(85, 101) # Damage modifier


            dmg = ((((2*Level/5 + 2) *AttackStat * AttackPower / DefenseStat) / 50) + 2) * STAB * Resistance * RandomNumber / 100

            dmg_round = np.floor(dmg)
            # dmg = ((((((((2*A/5+2)*B*C)/D)/50)+2)*X)*Y/10)*Z)/255
            return dmg_round

    # The move reduces stats
    else:
        if move.stat_red == 0: # Reduce attack
            if pokemon2.atk_stage == -6:
                print(f"{pokemon2.name}'s attack can't go any lower")
            else:
                pokemon2.atk_stage = pokemon2.atk_stage -1

        elif move.stat_red == 1: # Reduce defense
            if pokemon2.def_stage == -6:
                print(f"{pokemon2.name}'s defense can't go any lower")
            else:
                pokemon2.def_stage = pokemon2.def_stage -1


def summary(pokemon):
    print(f"HP: {pokemon.HP}")
    print(f"Attack Stage: {pokemon.atk_stage}")
    print(f"Defense Stage: {pokemon.def_stage}")


def dict_values_to_numpy(dictionary):
    """
    Convert the values in a dictionary into a numpy array
    """
    return np.array(list(dictionary.values()))



@functools.lru_cache(maxsize=256)
def get_stat_multiplier(stage):
    stat_mult_dict = {
      -6: 2/8,
      -5: 2/7,
      -4: 2/6,
      -3: 2/5,
      -2: 2/4,
      -1: 2/3,
      0: 2/2,
      1: 3/2,
      2: 4/2,
      3: 5/2,
      4: 6/2,
      5: 7/2,
      6: 8/2
    }

    return stat_mult_dict[stage]

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def avg_convergence_time():
    times = []
    for file in os.listdir('logs/'):
        with open(f'logs/{file}', 'rb') as f:
            data = pickle.load(f)
        if len(times) == 0:
            times = np.array([i[1] for i in data])
        else:
            times += np.array([i[1] for i in data])
        del data
    print(np.argmin(times), min(times)/len(os.listdir('logs/')))
    return times
