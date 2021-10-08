import pandas as pd
import matplotlib.pyplot as plt

IMAGES_PATH = './images/'
FIGSIZE = (16, 7)
XTICKS = range(0, 4015, 365)
XLABEL = "timestep(days)"


def boot_supply_plot(df: pd.DataFrame, title: str = 'BOOT Supply and Inflation Rate', figsize: tuple = FIGSIZE):
    columns = ['boot_liquid_supply', 'boot_frozen_supply', 'boot_bonded_supply']
    ax1 = df.plot.area(y=columns, linewidth=0, colormap="winter", xticks=XTICKS, grid=True, figsize=figsize)
    ax1.set(xlabel=XLABEL, ylabel="BOOT")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    ax2.set(ylabel="rate")
    df.plot.line(ax=ax2, y='boot_inflation_rate', figsize=figsize, xticks=XTICKS, grid=True)
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def hydrogen_supply_plot(df: pd.DataFrame, title: str = 'HYDROGEN Supply', figsize: tuple = FIGSIZE):
    ax = df.plot.line(y='hydrogen_supply', figsize=figsize, xticks=XTICKS, grid=True)
    ax.set(xlabel=XLABEL, ylabel="HYDROGEN")
    ax.set_title(title, size=16, fontweight="bold")
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def agents_count_plot(df: pd.DataFrame, title: str = 'Agents Count', figsize: tuple = FIGSIZE):
    ax = df.plot.line(y='agents_count', figsize=figsize, xticks=XTICKS, grid=True)
    ax.set(xlabel=XLABEL, ylabel="Agents Count")
    ax.set_title(title, size=16, fontweight="bold")
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def capitalization_plot(df: pd.DataFrame, title: str = 'BOOT Capitalization and BOOT Capitalization per Agent, ETH',
                        figsize: tuple = FIGSIZE):
    ax1 = df.plot(y='capitalization_per_agent', figsize=figsize, xticks=XTICKS, grid=True, 
                  style={'capitalization_per_agent': 'r'}, logy=True)
    ax1.set(xlabel=XLABEL, ylabel="BOOT Capitalization per Agent, ETH")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    ax2.set(ylabel="BOOT Capitalization, ETH")
    df.plot.line(ax=ax2, y='capitalization_in_eth', figsize=figsize, xticks=XTICKS, grid=True)
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def gboot_price_plot(df: pd.DataFrame, title: str = 'GBOOT Price and Validators Revenue', figsize: tuple = FIGSIZE):
    ax1 = df.plot(y='gboot_price', figsize=figsize, xticks=XTICKS, grid=True, style={'gboot_price': 'r'})
    ax1.set(xlabel=XLABEL, ylabel="GBOOT Price, ETH")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    ax2.set(ylabel="Validators Revenue, GBOOT")
    df.plot.line(ax=ax2, y='validator_revenue_gboot', figsize=figsize, xticks=XTICKS, grid=True, )
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def cyberlinks_per_day_plot(df: pd.DataFrame, title: str = 'cyberLinks per day', figsize: tuple = FIGSIZE):
    ax1 = df.plot(y=['cyberlinks_per_day', 'volt_supply', 'volt_liquid_supply'], figsize=figsize, xticks=XTICKS,
                  style={'cyberlinks_per_day': 'r'}, grid=True)
    ax1.set(xlabel=XLABEL, ylabel="cyberLinks per day | VOLT")
    ax1.set_title(title, size=16, fontweight="bold")
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def cyberlinks_count_plot(df: pd.DataFrame, title: str = 'cyberLinks Count', figsize: tuple = FIGSIZE):
    ax1 = df.plot(y=['cyberlinks_count'], figsize=figsize, xticks=XTICKS, grid=True)
    ax1.set_title(title, size=16, fontweight="bold")
    ax1.set(xlabel=XLABEL, ylabel="cyberLinks Count")
    ax1.set_title(title, size=16, fontweight="bold")
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def volt_and_ampere_supply_plot(df: pd.DataFrame, title: str = 'AMPERE and VOLT Supply', figsize: tuple = FIGSIZE):
    columns = ['volt_supply', 'ampere_supply']
    ax1 = df.plot.area(y=columns, linewidth=0, colormap="winter", xticks=XTICKS, grid=True, figsize=figsize)
    ax1.set(xlabel=XLABEL, ylabel="AMPERE | VOLT")
    ax1.set_title(title, size=16, fontweight="bold")
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def mint_rate_plot(df: pd.DataFrame, title: str = 'AMPERE and VOLT Mint Rate Investmint Max', figsize: tuple = FIGSIZE):
    ax1 = df.plot(y=['ampere_mint_rate', 'volt_mint_rate'], figsize=figsize, xticks=XTICKS, grid=True)
    ax1.set(xlabel=XLABEL, ylabel="Share")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.set(ylabel="Days")
    ax2.spines['right'].set_position(('axes', 1.0))
    df.plot.line(ax=ax2, y='investmint_max_period', figsize=figsize, xticks=XTICKS,
                 style={'investmint_max_period': 'r'}, grid=True)
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def minted_volt_ampere_plot(df: pd.DataFrame, title: str = 'AMPERE and VOLT Minted Amount', 
                            figsize: tuple = FIGSIZE):
    columns = ['volt_minted_amount', 'ampere_minted_amount']
    ax1 = df.plot.line(x='timestep', y=columns, xticks=XTICKS, grid=True, figsize=figsize)
    ax1.set(xlabel=XLABEL, ylabel="AMPERE | VOLT")
    ax1.set_title(title, size=16, fontweight="bold")
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()


def gpu_memory_usage_plot(df: pd.DataFrame, title: str = 'GPU Memory Usage', figsize: tuple = FIGSIZE):
    ax1 = df.plot(y=['cyberlinks_count'], figsize=figsize, xticks=XTICKS, grid=True, logy=True)
    ax1.set(xlabel=XLABEL, ylabel="cyberLinks Count")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    ax2.set(ylabel="GPU Memory Usage, Bytes")
    df.plot.line(ax=ax2, y='gpu_memory_usage', figsize=figsize, xticks=XTICKS,
                 style={'gpu_memory_usage': 'r'}, grid=True)
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.savefig(IMAGES_PATH + title.replace(' ', '_').lower() + '.png')
    plt.show()
