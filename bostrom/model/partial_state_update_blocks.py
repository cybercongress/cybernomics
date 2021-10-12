from model.policies import p_boot_inflation_rate_change, p_timestep_provision_boot, p_boot_frozen_supply, \
    p_boot_bonded_supply, p_boot_claimed_supply, p_agents_count, p_capitalization_per_agent, p_cyberlinks_per_day, \
    p_ampere_minted_amount, p_volt_minted_amount, p_volt_released, p_ampere_released
from model.state_update_functions import s_boot_supply, s_timestep_provision_boot, s_boot_claimed_supply, \
    s_boot_inflation_rate, s_boot_frozen_supply, s_boot_bonded_supply, s_boot_liquid_supply, \
    s_boot_to_distribution_supply, s_hydrogen_supply, s_agents_count, s_capitalization_per_agent, \
    s_capitalization_in_eth, s_gboot_price, s_validator_revenue_gboot, s_cyberlinks_count, s_cyberlinks_per_day, \
    s_ampere_supply, s_volt_supply, s_volt_mint_rate, s_ampere_mint_rate, s_investmint_max_period, s_gpu_memory_usage, \
    s_ampere_volt_ratio, s_volt_liquid_supply, s_ampere_liquid_supply, s_volt_minted_amount, s_ampere_minted_amount

partial_state_update_blocks = [
    {
        'policies': {
            'boot_inflation_rate_change': p_boot_inflation_rate_change,
            'timestep_provision_boot': p_timestep_provision_boot,
            'boot_frozen_supply_delta': p_boot_frozen_supply,
            'boot_bonded_supply_delta': p_boot_bonded_supply,
            'boot_claimed_supply_delta': p_boot_claimed_supply,
            'agents_count_delta': p_agents_count,
            'capitalization_per_agent_delta': p_capitalization_per_agent,
            'cyberlinks_per_day': p_cyberlinks_per_day,
            'ampere_minted_amount': p_ampere_minted_amount,
            'volt_minted_amount': p_volt_minted_amount,
            'volt_released': p_volt_released,
            'ampere_released': p_ampere_released
        },
        'variables': {
            'boot_supply': s_boot_supply,
            'timestep_provision_boot': s_timestep_provision_boot,
            'boot_claimed_supply': s_boot_claimed_supply,
            'boot_inflation_rate': s_boot_inflation_rate,
            'boot_frozen_supply': s_boot_frozen_supply,
            'boot_bonded_supply': s_boot_bonded_supply,
            'boot_liquid_supply': s_boot_liquid_supply,
            'boot_to_distribution_supply': s_boot_to_distribution_supply,
            'hydrogen_supply': s_hydrogen_supply,
            'agents_count': s_agents_count,
            'capitalization_per_agent': s_capitalization_per_agent,
            'capitalization_in_eth': s_capitalization_in_eth,
            'gboot_price': s_gboot_price,
            'validator_revenue_gboot': s_validator_revenue_gboot,
            'cyberlinks_count': s_cyberlinks_count,
            'cyberlinks_per_day': s_cyberlinks_per_day,
            'ampere_supply': s_ampere_supply,
            'volt_supply': s_volt_supply,
            'volt_mint_rate': s_volt_mint_rate,
            'ampere_mint_rate': s_ampere_mint_rate,
            'investmint_max_period': s_investmint_max_period,
            'gpu_memory_usage': s_gpu_memory_usage,
            'ampere_volt_ratio': s_ampere_volt_ratio,
            'volt_liquid_supply': s_volt_liquid_supply,
            'ampere_liquid_supply': s_ampere_liquid_supply,
            'volt_minted_amount': s_volt_minted_amount,
            'ampere_minted_amount': s_ampere_minted_amount
        }
    }
]