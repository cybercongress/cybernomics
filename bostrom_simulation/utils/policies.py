import math


def p_boot_inflation(params, substep, state_history, previous_state):
    boot_supply = previous_state['liquid_boot_amount'] + previous_state['frozen_boot_amount'] + previous_state['bonded_boot_amount']
    boot_bonded_share = previous_state['bonded_boot_amount']/boot_supply
    delta_boot_inflation = (1 - (boot_bonded_share/params['boot_bonded_share_target'])) * params['boot_inflation_rate_change_annual']
    delta_boot_inflation = delta_boot_inflation / params['timesteps_per_year']
    return {'delta_boot_inflation': delta_boot_inflation}


def p_timestep_provision(params, substep, state_history, previous_state):
    timestep_provision = (previous_state['boot_supply'] * previous_state['boot_inflation']) / params['timesteps_per_year']
    return {'timestep_provision': math.floor(timestep_provision)}


def p_bonded_boot_amount(params, substep, state_history, previous_state):
    delta_bonded_boot_amount = previous_state['liquid_boot_amount'] * params['boot_bonding_share'] * (1 - params['liquid_boot_supply_share'])
    return {'delta_bonded_boot_amount': math.floor(delta_bonded_boot_amount)}


def p_unbonded_boot_amount(params, substep, state_history, previous_state):
    delta_unbonded_boot_amount = previous_state['bonded_boot_amount'] * (1 - params['boot_bonding_share']) * params['liquid_boot_supply_share']
    return {'delta_unbonded_boot_amount': delta_unbonded_boot_amount}


def p_claimed_boot_amount(params, substep, state_history, previous_state):
    if previous_state['timestep'] < params['days_for_gift_activation']:
        delta_claimed_boot_amount = params['claimed_at_activation_share'] * params['boot_gift_amount_init'] / params['days_for_gift_activation']
    elif previous_state['timestep'] >= params['days_for_gift_activation']:
        delta_claimed_boot_amount = (1 - params['claimed_at_activation_share']) * params['boot_gift_amount_init'] / params['days_for_gift_full_claim']
    if previous_state['timestep'] > params['days_for_gift_full_claim'] + params['days_for_gift_activation']:
        delta_claimed_boot_amount = 0
    return {'delta_claimed_boot_amount': delta_claimed_boot_amount}


def p_frozen_boot_amount(params, substep, state_history, previous_state):
    if previous_state['timestep'] < params['days_for_gift_activation']:
        delta_frozen_boot_amount = 0
    else:
        delta_frozen_boot_amount = previous_state['to_distribution_boot_amount'] * 0.1
    return {'delta_frozen_boot_amount': -delta_frozen_boot_amount}


def p_agents_count(params, substep, state_history, previous_state):
    delta_agents_count = 18 * previous_state['timestep'] + 100
    return {'delta_agents_count': delta_agents_count}


def p_capitalization_per_agent(params, substep, state_history, previous_state):
    delta_capitalization_per_agent = params['start_capitalization_per_agent'] * math.pow(params['agents_count_at_activation'], 0.7) * math.pow(previous_state['agents_count'], -0.7)
    return {'delta_capitalization_per_agent': delta_capitalization_per_agent}


def p_cyberlinks(params, substep, state_history, previous_state):
    delta_cyberlinks = 27 * math.pow(previous_state['agents_count'], -0.3) * previous_state['agents_count'] + params['extra_links'] + params['guaranted_links']
    return {'delta_cyberlinks': delta_cyberlinks}


def p_minted_amper_amount(params, substep, state_history, previous_state):
    delta_bonded_boot_amount = previous_state['liquid_boot_amount'] * params['boot_bonding_share']
    delta_minted_amper_amount = math.floor((0.5 * delta_bonded_boot_amount / params['base_investmint_amount_amper']) * \
                                           (previous_state['investmint_max_period']/params['base_investmint_period_amper']) * previous_state['mint_rate_amper'])
    return {'delta_minted_amper_amount': math.floor(delta_minted_amper_amount)}


def p_minted_volt_amount(params, substep, state_history, previous_state):
    delta_bonded_boot_amount = previous_state['liquid_boot_amount'] * params['boot_bonding_share']
    delta_minted_volt_amount = math.floor((0.5 * delta_bonded_boot_amount / params['base_investmint_amount_volt']) * \
                                          (previous_state['investmint_max_period']/params['base_investmint_period_volt']) * previous_state['mint_rate_volt'])
    return {'delta_minted_volt_amount': math.floor(delta_minted_volt_amount)}
