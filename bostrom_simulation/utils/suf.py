import math


def s_boot_inflation_rate(params, substep, state_history, previous_state, policy_input):
    boot_inflation_rate = previous_state['boot_inflation_rate'] + policy_input['delta_boot_inflation_rate']
    if boot_inflation_rate > params['boot_inflation_max']:
        boot_inflation_rate = params['boot_inflation_max']
    elif boot_inflation_rate < params['boot_inflation_min']:
        boot_inflation_rate = params['boot_inflation_min']
    return 'boot_inflation_rate', boot_inflation_rate


def s_frozen_boot(params, substep, state_history, previous_state, policy_input):
    frozen_boot = previous_state['frozen_boot'] + policy_input['delta_frozen_boot']
    if frozen_boot < 0:
        frozen_boot= 0
    return 'frozen_boot', frozen_boot


def s_vested_boot(params, substep, state_history, previous_state, policy_input):
    vested_boot = previous_state['vested_boot'] + policy_input['delta_vested_boot'] - policy_input['delta_unvested_boot']
    if vested_boot < 0:
        vested_boot = 0
    return 'vested_boot', vested_boot


def s_liquid_boot(params, substep, state_history, previous_state, policy_input):
    liquid_boot = previous_state['liquid_boot'] - policy_input['delta_frozen_boot'] - policy_input['delta_vested_boot'] + \
                  policy_input['timestep_provision'] + policy_input['delta_unvested_boot']
    return 'liquid_boot', liquid_boot


def s_amper(params, substep, state_history, previous_state, policy_input):
    amper = previous_state['amper'] + policy_input['delta_amper']
    return 'amper', amper


def s_volt(params, substep, state_history, previous_state, policy_input):
    volt = previous_state['volt'] + policy_input['delta_volt']
    return 'volt', volt


def s_mint_rate_amper(params, substep, state_history, previous_state, policy_input):
    mint_rate_amper = params['mint_rate_amper_init'] / math.pow(2, (previous_state['timestep'] + 1) / params['base_halving_period_amper'])
    if mint_rate_amper < 1:
        mint_rate_amper = 1
    return 'mint_rate_amper', mint_rate_amper


def s_mint_rate_volt(params, substep, state_history, previous_state, policy_input):
    mint_rate_volt = params['mint_rate_volt_init'] / math.pow(2, (previous_state['timestep'] + 1) / params['base_halving_period_volt'])
    if mint_rate_volt < 1:
        mint_rate_volt = 1
    return 'mint_rate_volt', mint_rate_volt


def s_cyberlinks(params, substep, state_history, previous_state, policy_input):
    cyberlinks = previous_state['cyberlinks'] + policy_input['delta_cyberlinks']
    return 'cyberlinks', cyberlinks


def s_investmint_max_period(params, substep, state_history, previous_state, policy_input):
    investmint_max_period = params['investmint_max_period_init'] * math.pow(2, (previous_state['timestep'] + 1) / params['timesteps_per_year'])
    return 'investmint_max_period', investmint_max_period


def s_agents_count(params, substep, state_history, previous_state, policy_input):
    agents_count = previous_state['agents_count'] + policy_input['delta_agents_count']
    return 'agents_count', agents_count


def s_capitalization_per_agent(params, substep, state_history, previous_state, policy_input):
    capitalization_per_agent = previous_state['capitalization_per_agent'] + policy_input['delta_capitalization_per_agent']
    return 'capitalization_per_agent', capitalization_per_agent