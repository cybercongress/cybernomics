import math


def s_boot_supply(params, substep, state_history, previous_state, policy_input):
    boot_supply = previous_state['boot_supply'] + policy_input['timestep_provision']
    return 'boot_supply', boot_supply


def s_timestep_provision(params, substep, state_history, previous_state, policy_input):
    return 'timestep_provision', policy_input['timestep_provision']


def s_boot_inflation(params, substep, state_history, previous_state, policy_input):
    boot_inflation = previous_state['boot_inflation'] + policy_input['delta_boot_inflation']
    if boot_inflation > params['boot_inflation_max']:
        boot_inflation = params['boot_inflation_max']
    elif boot_inflation < params['boot_inflation_min']:
        boot_inflation = params['boot_inflation_min']
    return 'boot_inflation', boot_inflation


def s_bonded_boot_amount(params, substep, state_history, previous_state, policy_input):
    bonded_boot_amount = previous_state['bonded_boot_amount'] + policy_input['delta_bonded_boot_amount'] - \
                         policy_input['delta_unbonded_boot_amount']
    return 'bonded_boot_amount', bonded_boot_amount


def s_claimed_boot_amount(params, substep, state_history, previous_state, policy_input):
    claimed_boot_amount = previous_state['claimed_boot_amount'] + policy_input['delta_claimed_boot_amount']
    if claimed_boot_amount > params['boot_gift_amount_init']:
        claimed_boot_amount = params['boot_gift_amount_init']
    return 'claimed_boot_amount', claimed_boot_amount


def s_frozen_boot_amount(params, substep, state_history, previous_state, policy_input):
    frozen_boot_amount = previous_state['frozen_boot_amount'] + policy_input['delta_frozen_boot_amount']
    if frozen_boot_amount < 0:
        frozen_boot_amount = 0
    return 'frozen_boot_amount', frozen_boot_amount


def s_liquid_boot_amount(params, substep, state_history, previous_state, policy_input):
    liquid_boot_amount = previous_state['liquid_boot_amount'] - policy_input['delta_frozen_boot_amount'] - policy_input['delta_bonded_boot_amount'] + \
                  policy_input['timestep_provision'] + policy_input['delta_unbonded_boot_amount']
    return 'liquid_boot_amount', liquid_boot_amount


def s_to_distribution_boot_amount(params, substep, state_history, previous_state, policy_input):
    to_distribution_boot_amount = previous_state['to_distribution_boot_amount'] + policy_input['delta_claimed_boot_amount'] + \
                                  policy_input['delta_frozen_boot_amount']
    if to_distribution_boot_amount < 0:
        to_distribution_boot_amount = 0
    if to_distribution_boot_amount > params['boot_gift_amount_init']:
        to_distribution_boot_amount = params['boot_gift_amount_init']
    return 'to_distribution_boot_amount', to_distribution_boot_amount


def s_agents_count(params, substep, state_history, previous_state, policy_input):
    agents_count = previous_state['agents_count'] + policy_input['delta_agents_count']
    return 'agents_count', agents_count


def s_capitalization_per_agent(params, substep, state_history, previous_state, policy_input):
    capitalization_per_agent = params['start_capitalization_per_agent'] * math.pow(params['agents_count_at_activation'],0.7) * math.pow(previous_state['agents_count'], -0.7)
    return 'capitalization_per_agent', capitalization_per_agent


def s_capitalization(params, substep, state_history, previous_state, policy_input):
    return 'capitalization', previous_state['capitalization_per_agent'] * previous_state['agents_count']


def s_gboot_price(params, substep, state_history, previous_state, policy_input):
    return 'gboot_price', (previous_state['capitalization'] / previous_state['boot_supply']) * 1_000_000_000


def s_validator_revenue(params, substep, state_history, previous_state, policy_input):
    validator_revenue = ((previous_state['timestep_provision']) / 1_000_000_000 * params['validator_commission'] * previous_state['gboot_price']) / params['max_validator_count']
    return 'validator_revenue', validator_revenue


def s_cyberlinks(params, substep, state_history, previous_state, policy_input):
    cyberlinks = previous_state['cyberlinks'] + policy_input['delta_cyberlinks']
    return 'cyberlinks', cyberlinks


def s_mint_rate_amper(params, substep, state_history, previous_state, policy_input):
    mint_rate_amper = params['mint_rate_amper_init'] / math.pow(2, (math.floor(previous_state['timestep'] / params['base_halving_period_amper'])))
    if mint_rate_amper < 0.01:
        mint_rate_amper = 0.01
    return 'mint_rate_amper', mint_rate_amper


def s_mint_rate_volt(params, substep, state_history, previous_state, policy_input):
    mint_rate_volt = params['mint_rate_volt_init'] / math.pow(2, (math.floor(previous_state['timestep'] / params['base_halving_period_volt'])))
    if mint_rate_volt < 0.01:
        mint_rate_volt = 0.01
    return 'mint_rate_volt', mint_rate_volt


def s_investmint_max_period(params, substep, state_history, previous_state, policy_input):
    investmint_max_period = params['horizont_initial_period'] * math.pow(2, math.ceil((math.log2(math.ceil((previous_state['timestep'] + 1) / params['horizont_initial_period'])))))
    return 'investmint_max_period', investmint_max_period

def s_minted_amper_amount(params, substep, state_history, previous_state, policy_input):
    minted_amper_amount = previous_state['minted_amper_amount'] + policy_input['delta_minted_amper_amount']
    return 'minted_amper_amount', minted_amper_amount


def s_minted_volt_amount(params, substep, state_history, previous_state, policy_input):
    minted_volt_amount = previous_state['minted_volt_amount'] + policy_input['delta_minted_volt_amount']
    return 'minted_volt_amount', minted_volt_amount


def s_gpu_memory_usage(params, substep, state_history, previous_state, policy_input):
    if previous_state['minted_volt_amount'] == 0:
        return 'gpu_memory_usage', 0
    gpu_memory_usage = 40 * previous_state['cyberlinks'] + 40 * previous_state['minted_amper_amount']
    return 'gpu_memory_usage', gpu_memory_usage


def s_amper_volt_ratio(params, substep, state_history, previous_state, policy_input):
    if previous_state['minted_volt_amount'] == 0:
        return 'amper_volt_ratio', 0
    return 'amper_volt_ratio', previous_state['minted_amper_amount'] / previous_state['minted_volt_amount']