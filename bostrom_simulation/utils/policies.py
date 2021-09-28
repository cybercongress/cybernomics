import math


def p_boot_inflation_rate_change(params, substep, state_history, previous_state):
    boot_supply = previous_state['boot_liquid_supply'] + previous_state['boot_frozen_supply'] + previous_state['boot_bonded_supply']
    boot_bonded_share_current = previous_state['boot_bonded_supply'] / boot_supply
    boot_inflation_rate_change = (1 - (boot_bonded_share_current/params['boot_bonded_share_target'])) * params['boot_inflation_rate_change_annual']
    boot_inflation_rate_change = boot_inflation_rate_change / params['timesteps_per_year']
    return {'boot_inflation_rate_change': boot_inflation_rate_change}


def p_timestep_provision_boot(params, substep, state_history, previous_state):
    timestep_provision_boot = (previous_state['boot_supply'] * previous_state['boot_inflation_rate']) / params['timesteps_per_year']
    return {'timestep_provision_boot': math.floor(timestep_provision_boot)}


def p_boot_bonded_supply(params, substep, state_history, previous_state):
    delta_boot_bonded_supply = previous_state['boot_liquid_supply'] * (1 - params['liquid_boot_supply_share']) * 0.005
    return {'delta_boot_bonded_supply': math.floor(delta_boot_bonded_supply)}


def p_boot_claimed_supply(params, substep, state_history, previous_state):
    if previous_state['timestep'] < params['days_for_gift_activation']:
        delta_boot_claimed_supply = params['claimed_at_activation_share'] * params['boot_gift_amount_init'] / params['days_for_gift_activation']
    elif previous_state['timestep'] >= params['days_for_gift_activation']:
        delta_boot_claimed_supply = (1 - params['claimed_at_activation_share']) * params['boot_gift_amount_init'] / params['days_for_gift_full_claim']
    if previous_state['timestep'] > params['days_for_gift_full_claim'] + params['days_for_gift_activation']:
        delta_boot_claimed_supply = 0
    return {'delta_boot_claimed_supply': delta_boot_claimed_supply}


def p_boot_frozen_supply(params, substep, state_history, previous_state):
    if previous_state['timestep'] < params['days_for_gift_activation']:
        delta_boot_frozen_supply = 0
    else:
        delta_boot_frozen_supply = previous_state['boot_to_distribution_supply'] * 0.1
    return {'delta_boot_frozen_supply': -delta_boot_frozen_supply}


def p_agents_count(params, substep, state_history, previous_state):
    delta_agents_count = 18 * previous_state['timestep'] + 100
    return {'delta_agents_count': delta_agents_count}


def p_capitalization_per_agent(params, substep, state_history, previous_state):
    delta_capitalization_per_agent = params['start_capitalization_per_agent'] * math.pow(params['agents_count_at_activation'], 0.7) * math.pow(previous_state['agents_count'], -0.7)
    return {'delta_capitalization_per_agent': delta_capitalization_per_agent}


def p_cyberlinks_per_day(params, substep, state_history, previous_state):
    cyberlinks_per_day = params['cyberlinks_transactions_coeff'] * 9 * math.pow(previous_state['agents_count'], -0.3) * previous_state['agents_count'] + params['extra_links'] + params['guaranted_links']
    return {'cyberlinks_per_day': cyberlinks_per_day}


def p_ampere_minted_amount(params, substep, state_history, previous_state):
    if previous_state['timestep'] % 90 == 0:
        minted_ampere_amount = math.floor((0.5 * previous_state['boot_bonded_supply'] / params['ampere_base_investmint_amount']) * \
                                    (90 / params['ampere_base_investmint_period']) * previous_state['ampere_mint_rate'])
    else:
        minted_ampere_amount = 0
    return {'ampere_minted_amount': math.floor(minted_ampere_amount)}


def p_volt_minted_amount(params, substep, state_history, previous_state):
    if previous_state['timestep'] % 90 == 0:
        minted_volt_amount = math.floor((0.5 * previous_state['boot_bonded_supply'] / params['volt_base_investmint_amount']) * \
                                    (90/params['volt_base_investmint_period']) * previous_state['volt_mint_rate'])
    else:
        minted_volt_amount = 0
    return {'volt_minted_amount': math.floor(minted_volt_amount)}
