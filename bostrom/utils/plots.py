import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter

IMAGES_PATH = './images/'
FIGSIZE = (16, 5)
XTICKS = range(0, 4015, 365)
XLIM = (0, 3650)
XLABEL = 'timestep(days)'


def rename_column(column: str) -> str:
    return column. \
                replace('cyberlinks_per_day', 'cyberlinks_demand'). \
                replace('_', ' ').title(). \
                replace('Cyberlink', 'cyberLink'). \
                replace('Count', 'Amount'). \
                replace('Agent', 'Neuron'). \
                replace('Gboot', 'GBOOT'). \
                replace('Boot', 'BOOT'). \
                replace('Hydrogen', 'H'). \
                replace('Ampere', 'A'). \
                replace('Volt', 'V'). \
                replace('Eth', 'ETH'). \
                replace('Gpu', 'GPU'). \
                replace('Gb', 'GB'). \
                replace('Of ', 'of '). \
                replace('In ', 'in '). \
                replace('To ', 'to '). \
                replace('Per ', 'per ')


def prepare_df(df: pd.DataFrame) -> pd.DataFrame:

    df['boot_liquid_supply'] = df['boot_liquid_supply'] / 1e12
    df['boot_frozen_supply'] = df['boot_frozen_supply'] / 1e12
    df['boot_bonded_supply'] = df['boot_bonded_supply'] / 1e12
    df['hydrogen_supply'] = df['hydrogen_supply'] / 1e12
    df['ampere_supply'] = df['ampere_supply'] / 1e6
    df['ampere_minted_amount'] = df['ampere_minted_amount'] / 1e6
    df['volt_supply'] = df['volt_supply'] / 1e6
    df['volt_minted_amount'] = df['volt_minted_amount'] / 1e6
    df['cyberlinks_per_day'] = df['cyberlinks_per_day'] / 1e6
    df['cyberlinks_count'] = df['cyberlinks_count'] / 1e9
    df['agents_count'] = df['agents_count'] / 1e6
    df['gpu_memory_usage'] = df['gpu_memory_usage'] / 1e9

    growth_rate_period = 1
    df['agents_count_growth_rate'] = df['agents_count'].pct_change(periods=growth_rate_period)
    df['cyberlink_count_growth_rate'] = df['cyberlinks_count'].pct_change(periods=growth_rate_period)

    rename_columns_dict = {item: rename_column(item) for item in df.columns
                           if item not in ('simulation', 'subset', 'run', 'substep', 'timestep')}
    df.rename(columns=rename_columns_dict)
    return df.rename(columns=rename_columns_dict)


def plot(df: pd.DataFrame, title: str,
         columns_1: list,
         ylabel_1: str, ylabel_2: str = '',
         ypercent_1: bool = False, ypercent_2: bool = False,
         ylogscale_1: bool = False, ylogscale_2: bool = False,
         columns_2=None,
         type_1: str = 'area',
         ymin_1: float = 0, ymin_2: float = 0,
         figsize: tuple = FIGSIZE):
    columns_1 = list(map(rename_column, columns_1))
    plt.rcParams["figure.figsize"] = figsize
    plt.rcParams["figure.facecolor"] = '#FFFFFF'
    plt.rcParams["legend.facecolor"] = '#FFFFFF'
    plt.rcParams["legend.edgecolor"] = '#FFFFFF'
    if type_1 == 'area':
        ax1 = df.plot.area(y=columns_1, linewidth=0, colormap='winter', xticks=XTICKS, grid=True)
    else:
        ax1 = df.plot(y=columns_1, xticks=XTICKS, grid=True, style={columns_1[0]: 'r'}, logy=ylogscale_1)
    ax1.set(xlabel=XLABEL, ylabel=ylabel_1)
    ax1.set_title(title, size=16, fontweight='bold')
    ax1.spines['top'].set_visible(False)
    legend_1 = ax1.legend(loc='upper left')
    legend_1.get_frame().set_facecolor('#FFFFFF')
    if not ylogscale_1:
        ax1.set_ylim(bottom=ymin_1)
        ax1.yaxis.set_major_locator(plt.MaxNLocator(6))
        if df[columns_1].max().max() > 1000:
            ax1.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
        if ypercent_1:
            ticks_loc = ax1.get_yticks()
            ax1.yaxis.set_major_locator(FixedLocator(ticks_loc))
            ax1.set_yticklabels(['{:,.0%}'.format(x) for x in ticks_loc])
    if ylabel_2:
        columns_2 = list(map(rename_column, columns_2))
        ax2 = ax1.twinx()
        ax2.spines['right'].set_position(('axes', 1.0))
        ax2.set(ylabel=ylabel_2)
        df.plot.line(ax=ax2, y=columns_2, xticks=XTICKS, grid=True, logy=ylogscale_2)
        ax2.spines['top'].set_visible(False)
        ax2.grid(None)
        ax2.legend(loc='upper right')
        if not ylogscale_2:
            ax2.set_ylim(bottom=ymin_2)
            ax2.yaxis.set_major_locator(plt.MaxNLocator(6))
            if df[columns_2].max().max() > 1000:
                ax2.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
            if ypercent_2:
                ticks_loc = ax2.get_yticks()
                ax2.yaxis.set_major_locator(FixedLocator(ticks_loc))
                ax2.set_yticklabels(['{:,.1%}'.format(x) for x in ticks_loc])
    else:
        ax1.spines['right'].set_visible(False)
    plt.xlim(XLIM)
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').replace(',', '_').lower() + '.png')
    plt.show()


def boot_supply_plot(df: pd.DataFrame, title: str = 'BOOT Supply', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['boot_liquid_supply', 'boot_frozen_supply', 'boot_bonded_supply'],
         columns_2=['boot_inflation_rate'],
         ylabel_1='BOOT Supply, trillions',
         ylabel_2='BOOT Inflation Rate',
         ypercent_2=True,
         figsize=figsize)


def hydrogen_supply_plot(df: pd.DataFrame, title: str = 'H Supply', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['hydrogen_supply'],
         ylabel_1='H Supply, trillions',
         figsize=figsize)


def agents_count_plot(df: pd.DataFrame, title: str = 'Neurons Forecast', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['agents_count'],
         columns_2=['agents_count_growth_rate'],
         ylabel_1='Neurons Amount, millions',
         ylabel_2='Neurons Daily Growth Rate',
         ylogscale_2=True,
         figsize=figsize)


def capitalization_plot(df: pd.DataFrame, title: str = 'BOOT Capitalization',
                        figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['capitalization_per_agent'],
         columns_2=['capitalization_in_eth'],
         ylabel_1='BOOT Capitalization per Agent, ETH',
         ylabel_2='BOOT Capitalization, ETH',
         type_1='line',
         figsize=figsize)


def gboot_price_plot(df: pd.DataFrame, title: str = 'Validators Revenue', figsize: tuple = FIGSIZE):
    df[rename_column('validator_revenue,_eth')] = \
        df[rename_column('validator_revenue_gboot')] * df[rename_column('gboot_price')]
    plot(df=df,
         title=title,
         columns_1=['gboot_price'],
         columns_2=['validator_revenue,_eth'],
         ylabel_1='GBOOT Price, ETH',
         ylabel_2='Validators Revenue, ETH',
         type_1='line',
         figsize=figsize)


def cyberlinks_per_day_plot(df: pd.DataFrame, title: str = 'Demand and Supply of cyberLinks', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['cyberlinks_per_day', 'volt_supply'],
         ylabel_1='cyberLinks Demand | VOLT Supply, millions',
         type_1='line',
         figsize=figsize)


def cyberlinks_count_plot(df: pd.DataFrame, title: str = 'cyberLinks Forecast', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['cyberlinks_count'],
         columns_2=['cyberlink_count_growth_rate'],
         ylabel_1='cyberLinks Amount, billions',
         ylabel_2='cyberLinks Daily Growth Rate',
         ylogscale_2=True,
         figsize=figsize)


def ampere_supply_plot(df: pd.DataFrame, title: str = 'A Supply', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['ampere_supply'],
         ylabel_1='A Supply, millions',
         columns_2=['ampere_minted_amount'],
         ylabel_2='Minted A, millions',
         figsize=figsize)


def ampere_mint_rate_plot(df: pd.DataFrame, title: str = 'A Halving Cycles',
                          figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['ampere_mint_rate'],
         columns_2=['investmint_max_period'],
         ylabel_1='A Mint Rate',
         ylabel_2='Investmint Maximum Period, days',
         ypercent_1=True,
         type_1='line',
         figsize=figsize)


def volt_supply_plot(df: pd.DataFrame, title: str = 'V Supply', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['volt_supply'],
         ylabel_1='V Supply, millions',
         columns_2=['volt_minted_amount'],
         ylabel_2='Minted V, millions',
         figsize=figsize)


def volt_mint_rate_plot(df: pd.DataFrame, title: str = 'V Halving Cycles',
                        figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['volt_mint_rate'],
         columns_2=['investmint_max_period'],
         ylabel_1='V Mint Rate',
         ylabel_2='Investmint Maximum Period, days',
         ypercent_1=True,
         type_1='line',
         figsize=figsize)


def gpu_memory_usage_plot(df: pd.DataFrame, title: str = 'GPU Memory Usage', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['gpu_memory_usage'],
         ylabel_1='GPU Memory Usage, GB',
         ylogscale_1=True,
         type_1='line',
         figsize=figsize)
