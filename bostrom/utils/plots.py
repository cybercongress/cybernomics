import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FuncFormatter
from matplotlib import axes

IMAGES_PATH = './images/'
FIGSIZE = (16, 5)
XTICKS = range(0, 4015, 365)
XLIM = (0, 3650)
XLABEL = 'timestep (days)'


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
                replace('Cpu', 'CPU'). \
                replace('Gb', 'GB'). \
                replace('Of ', 'of '). \
                replace('For ', 'for '). \
                replace('In ', 'in '). \
                replace('To ', 'to '). \
                replace('Second', 'second'). \
                replace('Per ', 'per ')


def prepare_df(df: pd.DataFrame, a_v_ratio: float = 0.5, growth_rate_period: int = 1) -> pd.DataFrame:

    df['boot_liquid_supply'] = df['boot_liquid_supply'] / 1e12
    df['boot_frozen_supply'] = df['boot_frozen_supply'] / 1e12
    df['boot_bonded_supply'] = df['boot_bonded_supply'] / 1e12
    df['hydrogen_supply'] = df['hydrogen_supply'] / 1e12
    df['hydrogen_liquid_supply'] = df['hydrogen_liquid_supply'] / 1e12
    df['ampere_supply'] = df['ampere_supply'] / 1e6
    df['ampere_minted_amount'] = df['ampere_minted_amount'] / 1e6
    df['volt_supply'] = df['volt_supply'] / 1e6
    df['volt_minted_amount'] = df['volt_minted_amount'] / 1e6
    df['cyberlinks_per_day'] = df['cyberlinks_per_day'] / 1e6
    df['cyberlinks_count'] = df['cyberlinks_count'] / 1e9
    df['agents_count'] = df['agents_count'] / 1e6
    df['gpu_memory_usage'] = df['gpu_memory_usage'] / 1e9

    df['agents_daily_growth_rate'] = df['agents_count'].pct_change(periods=growth_rate_period)
    df['cyberlink_daily_growth_rate'] = df['cyberlinks_count'].pct_change(periods=growth_rate_period)

    df['transactions_per_second'] = df['cyberlinks_per_day'] / 24 / 3_600 * 1e6
    df['hydrogen_investminted_for_ampere'] = (df['hydrogen_supply'] - df['hydrogen_liquid_supply']) * a_v_ratio
    df['hydrogen_investminted_for_volt'] = (df['hydrogen_supply'] - df['hydrogen_liquid_supply']) * (1 - a_v_ratio)
    df['validator_revenue,_eth'] = df['validator_revenue_gboot'] * df['gboot_price']

    rename_columns_dict = {item: rename_column(item) for item in df.columns
                           if item not in ('simulation', 'subset', 'run', 'substep', 'timestep')}
    df.rename(columns=rename_columns_dict)
    return df.rename(columns=rename_columns_dict)


def get_colors(df: pd.DataFrame, sns_style: str = 'dark'):
    columns = [column for column in df.columns.sort_values()
               if column not in ('simulation', 'subset', 'run', 'substep', 'timestep')]
    colors = list(sns.color_palette(palette=sns_style, n_colors=len(columns)).as_hex())
    return {column: color for column, color in zip(columns, colors)}


def set_axis(ax: axes, ylabel: str, ylogscale: bool, ymin: float, ymax:float, ymax_value: float,
             ypercent: bool, legend_loc: str) -> axes:
    ax.spines['top'].set_visible(False)
    ax.set(ylabel=ylabel)
    ax.set_ylim(top=ymax)
    legend = ax.legend(loc=legend_loc)
    legend.get_frame().set_facecolor('#FFFFFF')
    legend.get_frame().set_alpha(0.6)
    if not ylogscale:
        ax.set_ylim(bottom=ymin, top=ymax)
        ax.yaxis.set_major_locator(plt.MaxNLocator(6))
        if ymax_value > 1000:
            ax.get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
        if ypercent:
            ticks_loc = ax.get_yticks()
            ax.yaxis.set_major_locator(FixedLocator(ticks_loc))
            ax.set_yticklabels(['{:,.0%}'.format(x) for x in ticks_loc])
    return ax


def plot(df: pd.DataFrame, title: str,
         columns_1: list,
         ylabel_1: str, ylabel_2: str = '',
         ypercent_1: bool = False, ypercent_2: bool = False,
         ylogscale_1: bool = False, ylogscale_2: bool = False,
         columns_2=None,
         type_1: str = 'area',
         ymin_1: float = 0, ymin_2: float = 0,
         ymax_1=None, ymax_2=None,
         figsize: tuple = FIGSIZE):
    columns_1 = list(map(rename_column, columns_1))
    color_style = get_colors(df)
    plt.rcParams["figure.figsize"] = figsize
    plt.rcParams["figure.facecolor"] = '#FFFFFF'
    plt.rcParams["legend.facecolor"] = '#FFFFFF'
    plt.rcParams["legend.edgecolor"] = '#FFFFFF'
    if type_1 == 'area':
        ax1 = df.plot.area(y=columns_1, xticks=XTICKS, grid=True, style=color_style, linewidth=0,  alpha=0.7)
    else:
        ax1 = df.plot.line(y=columns_1, xticks=XTICKS, grid=True, style=color_style, logy=ylogscale_1)
    ax1.set(xlabel=XLABEL)
    ax1.set_title(title, size=16, fontweight='bold')
    ax1 = set_axis(ax=ax1, ylabel=ylabel_1, ylogscale=ylogscale_1, ymin=ymin_1, ymax=ymax_1,
                   ymax_value=df[columns_1].max().max(), ypercent=ypercent_1, legend_loc='upper left')
    if ylabel_2:
        columns_2 = list(map(rename_column, columns_2))
        ax2 = ax1.twinx()
        df.plot.line(ax=ax2, y=columns_2, xticks=XTICKS, grid=True, style=color_style, logy=ylogscale_2)
        ax2.spines['right'].set_position(('axes', 1.0))
        ax2.grid(None)
        ax2 = set_axis(ax=ax2, ylabel=ylabel_2, ylogscale=ylogscale_2, ymin=ymin_2, ymax=ymax_2,
                       ymax_value=df[columns_2].max().max(), ypercent=ypercent_2, legend_loc='upper right')
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
         columns_1=['hydrogen_liquid_supply', 'hydrogen_investminted_for_ampere', 'hydrogen_investminted_for_volt'],
         ylabel_1='H Supply, trillions',
         figsize=figsize)


def agents_count_plot(df: pd.DataFrame, title: str = 'Neurons Forecast', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['agents_count'],
         columns_2=['agents_daily_growth_rate'],
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
         ylabel_1='BOOT Capitalization per Neuron, ETH',
         ylabel_2='BOOT Capitalization, ETH',
         ylogscale_1=True,
         type_1='line',
         figsize=figsize)


def gboot_price_plot(df: pd.DataFrame, title: str = 'Validators Revenue', figsize: tuple = FIGSIZE):
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
         columns_2=['cyberlink_daily_growth_rate'],
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


def ampere_mint_rate_plot(df: pd.DataFrame, title: str = 'A Halving Cycles', figsize: tuple = FIGSIZE):
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


def volt_mint_rate_plot(df: pd.DataFrame, title: str = 'V Halving Cycles', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['volt_mint_rate'],
         columns_2=['investmint_max_period'],
         ylabel_1='V Mint Rate',
         ylabel_2='Investmint Maximum Period, days',
         ypercent_1=True,
         type_1='line',
         figsize=figsize)


def tps_plot(df: pd.DataFrame, title: str = 'Transactions per second', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['Transactions per second'],
         ylabel_1='Transactions per second',
         figsize=figsize)


def gpu_memory_usage_plot(df: pd.DataFrame, title: str = 'Memory and Time Usage', figsize: tuple = FIGSIZE):
    plot(df=df,
         title=title,
         columns_1=['gpu_memory_usage', 'cpu_memory_usage'],
         columns_2=['gpu_time_usage', 'cpu_time_usage'],
         ylabel_1='Memory Usage, GB',
         ylabel_2='Time Usage, seconds',
         ylogscale_1=True,
         ylogscale_2=True,
         ymax_2=1.5 * df[[rename_column('gpu_time_usage'), rename_column('cpu_time_usage')]].max().max(),
         type_1='line',
         figsize=figsize)
