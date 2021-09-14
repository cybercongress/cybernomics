import math


def p_boot_inflation_rate(params, substep, state_history, previous_state):
    boot_supply = previous_state['liquid_boot'] + previous_state['frozen_boot'] + previous_state['vested_boot']
    vested_ratio = previous_state['vested_boot']/boot_supply
    delta_boot_inflation_rate = (1 - (vested_ratio/params['boot_bonded_share_target'])) * params['inflation_rate_change_annual']
    delta_boot_inflation_rate = delta_boot_inflation_rate / params['timesteps_per_year']
    return {'delta_boot_inflation_rate': delta_boot_inflation_rate}


def p_timestep_provision(params, substep, state_history, previous_state):
    boot_supply = previous_state['liquid_boot'] + previous_state['frozen_boot'] + previous_state['vested_boot']
    vested_ratio = previous_state['vested_boot']/boot_supply
    delta_boot_inflation_rate = (1 - (vested_ratio/params['boot_bonded_share_target'])) * params['inflation_rate_change_annual']
    delta_boot_inflation_rate = delta_boot_inflation_rate / params['timesteps_per_year']
    boot_inflation_rate = previous_state['boot_inflation_rate'] + delta_boot_inflation_rate
    if boot_inflation_rate > params['boot_inflation_max']:
        boot_inflation_rate = params['boot_inflation_max']
    elif boot_inflation_rate < params['boot_inflation_min']:
        boot_inflation_rate = params['boot_inflation_min']
    timestep_provision = (boot_supply * boot_inflation_rate) / params['timesteps_per_year']
    return {'timestep_provision': math.floor(timestep_provision)}


def p_frozen_boot(params, substep, state_history, previous_state):
    delta_frozen_boot = 45404590000000 * math.exp(-0.0648637 * (previous_state['timestep'] + 1))
    if previous_state['frozen_boot'] <= 0:
        delta_frozen_boot = 0
    return {'delta_frozen_boot': -delta_frozen_boot}


def p_vested_boot(params, substep, state_history, previous_state):
    delta_vested_boot = previous_state['liquid_boot']/((params['timesteps_per_year']/12) * params['vesting_speed'])
    return {'delta_vested_boot': math.floor(delta_vested_boot)}


def p_unvested_boot(params, substep, state_history, previous_state):
    if previous_state['timestep'] <= params['base_investmint_preiod_volt']:
        delta_unvested_boot = 0
    else:
        delta_unvested_boot = previous_state['liquid_boot']/((params['timesteps_per_year']/12) * params['unvesting_speed'])
    return {'delta_unvested_boot': math.floor(delta_unvested_boot)}


def p_cyberlinks(params, substep, state_history, previous_state):
    cyberlinks = 6.3 / previous_state['agents_count'] + params['extra_links'] + params['guaranted_links']
    return {'delta_cyberlinks': cyberlinks}


def p_amper(params, substep, state_history, previous_state):
    delta_vested_boot = previous_state['liquid_boot']/((params['timesteps_per_year']/12) * params['vesting_speed'])
    delta_amper = math.floor((delta_vested_boot / params['base_investmint_amount_amper']) * (previous_state['investmint_max_period']/params['base_investmint_preiod_amper']) * (previous_state['mint_rate_amper'] / 100))
    return {'delta_amper': math.floor(delta_amper)}


def p_volt(params, substep, state_history, previous_state):
    delta_vested_boot = previous_state['liquid_boot']/((params['timesteps_per_year']/12) * params['vesting_speed'])
    delta_volt = math.floor((delta_vested_boot / params['base_investmint_amount_volt']) * (previous_state['investmint_max_period']/params['base_investmint_preiod_volt']) * (previous_state['mint_rate_volt'] / 100))
    return {'delta_volt': math.floor(delta_volt)}


def p_agents_count(params, substep, state_history, previous_state):
    timestep = ((previous_state['timestep'] + 1) // params['timesteps_per_year']) * 365
    d_agents_count = 18 * timestep + 100
    return {'delta_agents_count': d_agents_count}


def p_capitalization_per_agent(params, substep, state_history, previous_state):
    delta_capitalization_per_agent = - (params['start_capitalization_per_agent'] * math.pow(params['agents_count_at_activation'], 0.7)) / \
                                     math.pow(previous_state['agents_count'], 1.7)
    return {'delta_capitalization_per_agent': delta_capitalization_per_agent}