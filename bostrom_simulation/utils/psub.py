from utils.policies import *
from utils.suf import *

partial_state_update_blocks = [
    {
        'policies': {
            'delta_boot_inflation_rate': p_boot_inflation_rate,
            'timestep_provision': p_timestep_provision,
            'delta_frozen_boot': p_frozen_boot,
            'delta_vested_boot': p_vested_boot,
            'delta_unvested_boot': p_unvested_boot,
            'delta_cyberlinks': p_cyberlinks,
            'delta_amper': p_amper,
            'delta_volt': p_volt,
            'delta_agents_count': p_agents_count,
            'delta_capitalization_per_agent': p_capitalization_per_agent
        },
        'variables': {
            'boot_inflation_rate': s_boot_inflation_rate,
            'frozen_boot': s_frozen_boot,
            'vested_boot': s_vested_boot,
            'liquid_boot': s_liquid_boot,
            'amper': s_amper,
            'volt': s_volt,
            'mint_rate_amper': s_mint_rate_amper,
            'mint_rate_volt': s_mint_rate_volt,
            'cyberlinks': s_cyberlinks,
            'investmint_max_period': s_investmint_max_period,
            'agents_count': s_agents_count,
            'capitalization_per_agent': s_capitalization_per_agent
        }
    }
]