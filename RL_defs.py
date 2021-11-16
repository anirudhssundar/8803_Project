def get_state(pokemon1, pokemon2):
    state = (pokemon2.HP, pokemon1.atk_stage - pokemon2.def_stage)
    return state


def reward(next_state):
    if next_state[0] == 0: # Check if pokemon has 0 HP
        return 10
    else:
        return -1
