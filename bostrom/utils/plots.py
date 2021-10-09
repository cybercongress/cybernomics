import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

IMAGES_PATH = './images/'
FIGSIZE = (16, 7)
XTICKS = range(0, 4015, 365)
XLIM = (0, 3650)
XLABEL = 'timestep(days)'


def rename_column(column: str) -> str:
    return column.\
                replace('_', ' ').title(). \
                replace('Gboot', 'GBOOT'). \
                replace('Boot', 'BOOT'). \
                replace('Hydrogen', 'HYDROGEN'). \
                replace('Ampere', 'AMPERE'). \
                replace('Volt', 'VOLT'). \
                replace('Eth', 'ETH'). \
                replace('Gpu', 'GPU'). \
                replace('Gb', 'GB'). \
                replace('In ', 'in '). \
                replace('To ', 'to '). \
                replace('Per ', 'per ')


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_columns_dict = {item: rename_column(item) for item in df.columns
                           if item not in ('simulation', 'subset', 'run', 'substep', 'timestep')}
    df.rename(columns=rename_columns_dict)
    return df.rename(columns=rename_columns_dict)


def plot(df: pd.DataFrame, title: str,
         columns_1: list,
         ylabel_1: str, ylabel_2: str = '',
         ypercent_1: bool = False, ypercent_2: bool = False,
         columns_2=None,
         type_1: str = 'area',
         ymin_1: float = 0, ymin_2: float = 0,
         figsize: tuple = FIGSIZE):
    columns_1 = list(map(rename_column, columns_1))
    if type_1 == 'area':
        ax1 = df.plot.area(y=columns_1, linewidth=0, colormap='winter', xticks=XTICKS, grid=True, figsize=figsize)
    else:
        ax1 = df.plot(y=columns_1, figsize=figsize, xticks=XTICKS, grid=True, style={columns_1[0]: 'r'})
    ax1.set(xlabel=XLABEL, ylabel=ylabel_1)
    ax1.set_ylim(bottom=ymin_1)
    ax1.set_title(title, size=16, fontweight='bold')
    ax1.spines['top'].set_visible(False)
    ax1.legend(loc='upper left')
    ax1.yaxis.set_major_locator(plt.MaxNLocator(6))
    if ypercent_1:
        ticks_loc = ax1.get_yticks()
        ax1.yaxis.set_major_locator(FixedLocator(ticks_loc))
        ax1.set_yticklabels(['{:,.0%}'.format(x) for x in ticks_loc])
    if ylabel_2:
        columns_2 = list(map(rename_column, columns_2))
        ax2 = ax1.twinx()
        ax2.spines['right'].set_position(('axes', 1.0))
        ax2.set(ylabel=ylabel_2)
        df.plot.line(ax=ax2, y=columns_2, figsize=figsize, xticks=XTICKS, grid=True)
        ax2.set_ylim(bottom=ymin_2)
        ax2.spines['top'].set_visible(False)
        ax2.grid(None)
        ax2.legend(loc='upper right')
        ax2.yaxis.set_major_locator(plt.MaxNLocator(6))
        if ypercent_2:
            ticks_loc = ax2.get_yticks()
            ax2.yaxis.set_major_locator(FixedLocator(ticks_loc))
            ax2.set_yticklabels(['{:,.1%}'.format(x) for x in ticks_loc])
    else:
        ax1.spines['right'].set_visible(False)
    plt.xlim(XLIM)
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def boot_supply_plot(df: pd.DataFrame, title: str = 'BOOT Supply and Inflation Rate', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['boot_liquid_supply', 'boot_frozen_supply', 'boot_bonded_supply'],
         columns_2=['boot_inflation_rate'],
         ylabel_1='BOOT Supply',
         ylabel_2='BOOT Inflation Rate',
         ypercent_2=True,
         figsize=figsize)


def hydrogen_supply_plot(df: pd.DataFrame, title: str = 'HYDROGEN Supply', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['hydrogen_supply'],
         ylabel_1='HYDROGEN Supply',
         figsize=figsize)


def agents_count_plot(df: pd.DataFrame, title: str = 'Agents Count', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['agents_count'],
         ylabel_1='Agents Count',
         figsize=figsize)


def capitalization_plot(df: pd.DataFrame, title: str = 'BOOT Capitalization and BOOT Capitalization per Agent, ETH',
                        figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['capitalization_per_agent'],
         columns_2=['capitalization_in_eth'],
         ylabel_1='BOOT Capitalization per Agent, ETH',
         ylabel_2='BOOT Capitalization, ETH',
         type_1='line',
         figsize=figsize)


def gboot_price_plot(df: pd.DataFrame, title: str = 'GBOOT Price and Validators Revenue', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['gboot_price'],
         columns_2=['validator_revenue_gboot'],
         ylabel_1='GBOOT Price, ETH',
         ylabel_2='Validators Revenue, GBOOT',
         type_1='line',
         figsize=figsize)


def cyberlinks_per_day_plot(df: pd.DataFrame, title: str = 'cyberLinks per day', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['cyberlinks_per_day', 'volt_supply', 'volt_liquid_supply'],
         ylabel_1='cyberLinks per day | VOLT Supply',
         type_1='line',
         figsize=figsize)


def cyberlinks_count_plot(df: pd.DataFrame, title: str = 'cyberLinks Count', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['cyberlinks_count'],
         ylabel_1='cyberLinks Count',
         figsize=figsize)


def volt_and_ampere_supply_plot(df: pd.DataFrame, title: str = 'AMPERE and VOLT Supply', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['volt_supply', 'ampere_supply'],
         ylabel_1='AMPERE | VOLT',
         figsize=figsize)


def mint_rate_plot(df: pd.DataFrame, title: str = 'Mint Rate and Investmint Maximum Period for AMPERE and VOLT',
                   figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['ampere_mint_rate', 'volt_mint_rate'],
         columns_2=['investmint_max_period'],
         ylabel_1='Mint Rate',
         ylabel_2='Investmint Maximum Period, days',
         ypercent_1=True,
         type_1='line',
         figsize=figsize)


def minted_volt_ampere_plot(df: pd.DataFrame, title: str = 'AMPERE and VOLT Minted Amount',
                            figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['volt_minted_amount', 'ampere_minted_amount'],
         ylabel_1='AMPERE | VOLT',
         type_1='line',
         figsize=figsize)


def gpu_memory_usage_plot(df: pd.DataFrame, title: str = 'GPU Memory Usage', figsize: tuple = FIGSIZE):
    df[rename_column('gpu_memory_usage_gb')] = df[rename_column('gpu_memory_usage')] / 1e9
    plot(df=df,
         title=title,
         columns_1=['cyberlinks_count'],
         columns_2=['gpu_memory_usage_gb'],
         ylabel_1='cyberLinks Count',
         ylabel_2='GPU Memory Usage, GB',
         type_1='line',
         figsize=figsize)
