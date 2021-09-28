from utils.policies import *
from utils.state_update_functions import *

partial_state_update_blocks = [
    {
        'policies': {
            'delta_boot_inflation': p_boot_inflation,
            'timestep_provision': p_timestep_provision,
            'delta_frozen_boot_amount': p_frozen_boot_amount,
            'delta_bonded_boot_amount': p_bonded_boot_amount,
            'delta_unbonded_boot_amount': p_unbonded_boot_amount,
            'delta_claimed_boot_amount': p_claimed_boot_amount,
            'delta_agents_count': p_agents_count,
            'delta_capitalization_per_agent': p_capitalization_per_agent,
            'delta_cyberlinks': p_cyberlinks,
            'delta_minted_amper_amount': p_minted_amper_amount,
            'delta_minted_volt_amount': p_minted_volt_amount
        },
        'variables': {
            'boot_supply': s_boot_supply,
            'timestep_provision': s_timestep_provision,
            'claimed_boot_amount': s_claimed_boot_amount,
            'boot_inflation': s_boot_inflation,
            'frozen_boot_amount': s_frozen_boot_amount,
            'bonded_boot_amount': s_bonded_boot_amount,
            'liquid_boot_amount': s_liquid_boot_amount,
            'to_distribution_boot_amount': s_to_distribution_boot_amount,
            'agents_count': s_agents_count,
            'capitalization_per_agent': s_capitalization_per_agent,
            'capitalization': s_capitalization,
            'gboot_price': s_gboot_price,
            'validator_revenue': s_validator_revenue,
            'cyberlinks': s_cyberlinks,
            'delta_cyberlinks': s_delta_cyberlinks,
            'minted_amper_amount': s_minted_amper_amount,
            'minted_volt_amount': s_minted_volt_amount,
            'mint_rate_volt': s_mint_rate_volt,
            'mint_rate_amper': s_mint_rate_amper,
            'investmint_max_period': s_investmint_max_period,
            'gpu_memory_usage': s_gpu_memory_usage,
            'amper_volt_ratio': s_amper_volt_ratio
        }
    }
]