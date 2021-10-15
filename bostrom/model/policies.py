import math

volt_hydrogen = {}
ampere_hydrogen = {}


def p_boot_inflation_rate_change(params, substep, state_history, previous_state):
    boot_supply = previous_state['boot_liquid_supply'] + previous_state['boot_frozen_supply'] + \
                  previous_state['boot_bonded_supply']
    boot_bonded_share_current = previous_state['boot_bonded_supply'] / boot_supply
    boot_inflation_rate_change = (1 - (boot_bonded_share_current / params['boot_bonded_share_target'])) * \
                                 params['boot_inflation_rate_change_annual']
    boot_inflation_rate_change = boot_inflation_rate_change / params['timesteps_per_year']
    return {'boot_inflation_rate_change': boot_inflation_rate_change}


def p_timestep_provision_boot(params, substep, state_history, previous_state):
    timestep_provision_boot = \
        (previous_state['boot_supply'] * previous_state['boot_inflation_rate']) / params['timesteps_per_year']
    return {'timestep_provision_boot': math.floor(timestep_provision_boot)}


def p_boot_bonded_supply(params, substep, state_history, previous_state):
    boot_bonded_share = previous_state['boot_bonded_supply'] / previous_state['boot_supply']
    boot_bonded_supply_delta = (params['boot_bonded_share_limit'] - boot_bonded_share) * \
                               previous_state['boot_supply'] * params['bonding_speed_coeff']
    return {'boot_bonded_supply_delta': math.floor(boot_bonded_supply_delta)}


def p_hydrogen_supply(params, substep, state_history, previous_state):
    boot_bonded_share = previous_state['boot_bonded_supply'] / previous_state['boot_supply']
    hydrogen_supply_delta = (params['boot_bonded_share_limit'] - boot_bonded_share) * previous_state[
        'boot_supply'] * params['bonding_speed_coeff']
    return {'hydrogen_supply_delta': math.floor(hydrogen_supply_delta)}


def p_boot_claimed_supply(params, substep, state_history, previous_state):
    if previous_state['timestep'] < params['days_for_gift_activation']:
        boot_claimed_supply_delta = params['claimed_at_activation_share'] * params['boot_gift_amount_init'] / \
                                    params['days_for_gift_activation']
    elif previous_state['timestep'] >= params['days_for_gift_activation']:
        boot_claimed_supply_delta = (1 - params['claimed_at_activation_share']) * params['boot_gift_amount_init'] / \
                                    params['days_for_gift_full_claim']
    if previous_state['timestep'] > params['days_for_gift_full_claim'] + params['days_for_gift_activation']:
        boot_claimed_supply_delta = 0
    return {'boot_claimed_supply_delta': boot_claimed_supply_delta}


def p_boot_frozen_supply(params, substep, state_history, previous_state):
    if previous_state['timestep'] < params['days_for_gift_activation']:
        boot_frozen_supply_delta = 0
    elif previous_state['timestep'] == params['days_for_gift_activation']:
        boot_frozen_supply_delta = previous_state['boot_to_distribution_supply'] * 0.1
    else:
        boot_frozen_supply_delta = previous_state['boot_to_distribution_supply'] * 0.01
    return {'boot_frozen_supply_delta': -boot_frozen_supply_delta}


def p_agents_count(params, substep, state_history, previous_state):
    agents_count_delta = 18 * previous_state['timestep'] + 100
    return {'agents_count_delta': agents_count_delta}


def p_capitalization_per_agent(params, substep, state_history, previous_state):
    agents_count_delta = 18 * previous_state['timestep'] + 100
    capitalization_per_agent_delta = \
        2990 * (- 0.7) * math.pow(previous_state['agents_count'], (-1.7)) * agents_count_delta
    return {'capitalization_per_agent_delta': capitalization_per_agent_delta}


def p_cyberlinks_per_day(params, substep, state_history, previous_state):
    cyberlinks_per_day = \
        params['cyberlinks_transactions_coeff'] * 9 * math.pow(previous_state['agents_count'], -0.3) * \
        previous_state['agents_count'] + params['extra_links'] + params['guaranteed_links']
    return {'cyberlinks_per_day': cyberlinks_per_day}


def p_ampere_minted_amount(params, substep, state_history, previous_state):
    boot_bonded_share = previous_state['boot_bonded_supply'] / previous_state['boot_supply']
    hydrogen_supply_delta = (params['boot_bonded_share_limit'] - boot_bonded_share) * previous_state[
        'boot_supply'] * params['bonding_speed_coeff']
    hydrogen_supply_delta *= (1 - params['hydrogen_liquid_ratio'])
    if previous_state['timestep'] in ampere_hydrogen.keys():
        released_hydrogen = ampere_hydrogen[previous_state['timestep']]
    else:
        released_hydrogen = 0
    hydrogen_for_minting = (params['ampere_volt_ratio'] * hydrogen_supply_delta) + released_hydrogen
    investmint_max_period = math.floor(params['investmint_period_share'] * previous_state['investmint_max_period'])
    ampere_minted_amount = \
        math.floor((hydrogen_for_minting / params['ampere_base_investmint_amount']) *
                   (investmint_max_period / params['ampere_base_investmint_period']) * previous_state[
                       'ampere_mint_rate'])
    ampere_hydrogen[previous_state['timestep'] + investmint_max_period] = hydrogen_for_minting
    return {'ampere_minted_amount': math.floor(ampere_minted_amount)}


def p_volt_minted_amount(params, substep, state_history, previous_state):
    boot_bonded_share = previous_state['boot_bonded_supply'] / previous_state['boot_supply']
    hydrogen_supply_delta = (params['boot_bonded_share_limit'] - boot_bonded_share) * previous_state[
        'boot_supply'] * params['bonding_speed_coeff']
    hydrogen_supply_delta *= (1 - params['hydrogen_liquid_ratio'])
    if previous_state['timestep'] in volt_hydrogen.keys():
        released_hydrogen = volt_hydrogen[previous_state['timestep']]
    else:
        released_hydrogen = 0
    hydrogen_for_minting = ((1 - params['ampere_volt_ratio']) * hydrogen_supply_delta) + released_hydrogen
    investmint_max_period = math.floor(params['investmint_period_share'] * previous_state['investmint_max_period'])
    volt_minted_amount = \
        math.floor((hydrogen_for_minting / params['volt_base_investmint_amount']) * \
                   (investmint_max_period / params['volt_base_investmint_period']) * previous_state['volt_mint_rate'])
    volt_hydrogen[previous_state['timestep'] + investmint_max_period] = hydrogen_for_minting
    return {'volt_minted_amount': math.floor(volt_minted_amount)}


def p_hydrogen_liquid_supply_delta(params, substep, state_history, previous_state):
    boot_bonded_share = previous_state['boot_bonded_supply'] / previous_state['boot_supply']
    boot_bonded_supply_delta = (params['boot_bonded_share_limit'] - boot_bonded_share) * previous_state[
        'boot_supply'] * params['bonding_speed_coeff']
    hydrogen_liquid_supply_delta = params['hydrogen_liquid_ratio'] * boot_bonded_supply_delta
    return {'hydrogen_liquid_supply_delta': math.floor(hydrogen_liquid_supply_delta)}
