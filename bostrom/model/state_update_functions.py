import math
import pandas as pd


def s_boot_supply(params, substep, state_history, previous_state, policy_input):
    boot_supply = previous_state['boot_supply'] + policy_input['timestep_provision_boot']
    return 'boot_supply', boot_supply


def s_timestep_provision_boot(params, substep, state_history, previous_state, policy_input):
    return 'timestep_provision_boot', policy_input['timestep_provision_boot']


def s_boot_inflation_rate(params, substep, state_history, previous_state, policy_input):
    boot_inflation_rate = previous_state['boot_inflation_rate'] + policy_input['boot_inflation_rate_change']
    if boot_inflation_rate > params['boot_inflation_rate_max']:
        boot_inflation_rate = params['boot_inflation_rate_max']
    elif boot_inflation_rate < params['boot_inflation_rate_min']:
        boot_inflation_rate = params['boot_inflation_rate_min']
    return 'boot_inflation_rate', boot_inflation_rate


def s_boot_bonded_supply(params, substep, state_history, previous_state, policy_input):
    boot_bonded_supply = previous_state['boot_bonded_supply'] + policy_input['boot_bonded_supply_delta']
    return 'boot_bonded_supply', boot_bonded_supply


def s_hydrogen_supply(params, substep, state_history, previous_state, policy_input):
    hydrogen_supply = previous_state['hydrogen_supply'] + policy_input['hydrogen_supply_delta']
    return 'hydrogen_supply', hydrogen_supply


def s_hydrogen_liquid_supply(params, substep, state_history, previous_state, policy_input):
    hydrogen_liquid_supply = previous_state['hydrogen_liquid_supply'] + policy_input['hydrogen_liquid_supply_delta']
    return 'hydrogen_liquid_supply', hydrogen_liquid_supply


def s_boot_claimed_supply(params, substep, state_history, previous_state, policy_input):
    boot_claimed_supply = previous_state['boot_claimed_supply'] + policy_input['boot_claimed_supply_delta']
    if boot_claimed_supply > params['boot_gift_amount_init']:
        boot_claimed_supply = params['boot_gift_amount_init']
    return 'boot_claimed_supply', boot_claimed_supply


def s_boot_frozen_supply(params, substep, state_history, previous_state, policy_input):
    boot_frozen_supply = previous_state['boot_frozen_supply'] + policy_input['boot_frozen_supply_delta']
    if boot_frozen_supply < 0:
        boot_frozen_supply = 0
    return 'boot_frozen_supply', boot_frozen_supply


def s_boot_liquid_supply(params, substep, state_history, previous_state, policy_input):
    boot_liquid_supply = previous_state['boot_liquid_supply'] - policy_input['boot_frozen_supply_delta'] - \
                         policy_input['boot_bonded_supply_delta'] + policy_input['timestep_provision_boot']
    return 'boot_liquid_supply', boot_liquid_supply


def s_boot_to_distribution_supply(params, substep, state_history, previous_state, policy_input):
    boot_to_distribution_supply = \
        previous_state['boot_to_distribution_supply'] + policy_input['boot_claimed_supply_delta'] + \
        policy_input['boot_frozen_supply_delta']
    if boot_to_distribution_supply < 0:
        boot_to_distribution_supply = 0
    if boot_to_distribution_supply > params['boot_gift_amount_init']:
        boot_to_distribution_supply = params['boot_gift_amount_init']
    return 'boot_to_distribution_supply', boot_to_distribution_supply


def s_agents_count(params, substep, state_history, previous_state, policy_input):
    agents_count = previous_state['agents_count'] + policy_input['agents_count_delta']
    return 'agents_count', agents_count


def s_capitalization_per_agent(params, substep, state_history, previous_state, policy_input):
    capitalization_per_agent = \
        previous_state['capitalization_per_agent'] + policy_input['capitalization_per_agent_delta']
    return 'capitalization_per_agent', capitalization_per_agent


def s_capitalization_in_eth(params, substep, state_history, previous_state, policy_input):
    return 'capitalization_in_eth', previous_state['capitalization_per_agent'] * previous_state['agents_count']


def s_gboot_price(params, substep, state_history, previous_state, policy_input):
    return 'gboot_price', (previous_state['capitalization_in_eth'] / previous_state['boot_supply']) * 1_000_000_000


def s_validator_revenue_gboot(params, substep, state_history, previous_state, policy_input):
    validator_revenue_gboot = previous_state['timestep_provision_boot'] / 1_000_000_000 * \
                              params['validator_commission'] / params['max_validator_count']
    return 'validator_revenue_gboot', validator_revenue_gboot


def s_cyberlinks_count(params, substep, state_history, previous_state, policy_input):
    cyberlinks_count = previous_state['cyberlinks_count'] + policy_input['cyberlinks_per_day']
    return 'cyberlinks_count', cyberlinks_count


def s_cyberlinks_per_day(params, substep, state_history, previous_state, policy_input):
    cyberlinks_per_day = policy_input['cyberlinks_per_day']
    return 'cyberlinks_per_day', cyberlinks_per_day


def s_ampere_mint_rate(params, substep, state_history, previous_state, policy_input):
    ampere_mint_rate = 1 / math.pow(2, (math.floor(previous_state['timestep'] /
                                                   params['ampere_base_halving_period'])))
    if ampere_mint_rate < params['ampere_mint_rate_min']:
        ampere_mint_rate = params['ampere_mint_rate_min']
    return 'ampere_mint_rate', ampere_mint_rate


def s_volt_mint_rate(params, substep, state_history, previous_state, policy_input):
    volt_mint_rate = 1 / math.pow(2, (math.floor(previous_state['timestep'] /
                                                 params['volt_base_halving_period'])))
    if volt_mint_rate < params['volt_mint_rate_min']:
        volt_mint_rate = params['volt_mint_rate_min']
    return 'volt_mint_rate', volt_mint_rate


def s_investmint_max_period(params, substep, state_history, previous_state, policy_input):
    investmint_max_period = params['investmint_max_period_init'] * math.ceil((previous_state['timestep'] + 1) /
                                                                             params['horizon_period_init'])
    return 'investmint_max_period', investmint_max_period


def s_ampere_supply(params, substep, state_history, previous_state, policy_input):
    ampere_supply = previous_state['ampere_supply'] + policy_input['ampere_minted_amount']
    return 'ampere_supply', ampere_supply


def s_volt_supply(params, substep, state_history, previous_state, policy_input):
    volt_supply = previous_state['volt_supply'] + policy_input['volt_minted_amount']
    return 'volt_supply', volt_supply


def s_gpu_memory_usage(params, substep, state_history, previous_state, policy_input):
    particles = previous_state['cyberlinks_count'] * params['particle_per_cyberlink']
    if previous_state['volt_supply'] == 0:
        return 'gpu_memory_usage', 0
    gpu_memory_usage = 40 * previous_state['cyberlinks_count'] + 40 * particles
    return 'gpu_memory_usage', gpu_memory_usage


def s_cpu_memory_usage(params, substep, state_history, previous_state, policy_input):
    cpu_memory_usage = 1.2 * (10 ** 3) * previous_state['cyberlinks_count']
    return 'cpu_memory_usage', cpu_memory_usage


def s_cpu_time_usage(params, substep, state_history, previous_state, policy_input):
    cpu_time_usage = 8.7 * (10 ** (-7)) * previous_state['cyberlinks_count']
    return 'cpu_time_usage', cpu_time_usage


def s_gpu_time_usage(params, substep, state_history, previous_state, policy_input):
    gpu_time_usage = 6.2 * (10 ** (-9)) * previous_state['cyberlinks_count']
    return 'gpu_time_usage', gpu_time_usage


def s_volt_minted_amount(params, substep, state_history, previous_state, policy_input):
    return 'volt_minted_amount', policy_input['volt_minted_amount']


def s_ampere_minted_amount(params, substep, state_history, previous_state, policy_input):
    return 'ampere_minted_amount', policy_input['ampere_minted_amount']
