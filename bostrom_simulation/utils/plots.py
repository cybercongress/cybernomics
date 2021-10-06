# import plotly.express as px
# import seaborn as sns
# import pandas as pd
import matplotlib.pyplot as plt

path = './images/'


def boot_supply_plot(df, title='boot supply and inflation rate', figsize=(16, 9)):
    columns = ['boot_liquid_supply', 'boot_frozen_supply', 'boot_bonded_supply']
    ax1 = df.plot.area(y=columns, linewidth=0, colormap="winter", xticks=range(0, 3650, 365), grid=True,
                            title=title, figsize=figsize)
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df.plot.line(ax=ax2, y='boot_inflation_rate', figsize=figsize, xticks=range(0, 3650, 365), grid=True)
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def hydrogen_supply_plot(df, title='hydrogen supply', figsize=(16, 9)):
    df.plot(y='hydrogen_supply', figsize=figsize, xticks=range(0, 3650, 365), grid=True, title=title)
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def agents_count_plot(df, title='agents count', figsize=(16, 9)):
    df.plot(y='agents_count', figsize=figsize, xticks=range(0, 3650, 365), grid=True, title=title)
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def capitalization_plot(df, title='cap in eth and cap per agent', figsize=(16, 9)):
    ax1 = df.plot(y='capitalization_per_agent', figsize=figsize, xticks=range(0, 3650, 365), grid=True, title=title,
                  logy=True, style={'capitalization_per_agent': 'r'})
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df.plot.line(ax=ax2, y='capitalization_in_eth', figsize=figsize, xticks=range(0, 3650, 365), grid=True, )
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def gboot_price_plot(df, title='gboot price and validators revenue', figsize=(16, 9)):
    df.plot(y=['gboot_price', 'validator_revenue_gboot'], figsize=figsize, xticks=range(0, 3650, 365), grid=True,
                 title=title)
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def cyberlinks_per_day_plot(df, title='cyberlinks per day', figsize=(16, 9)):
    df.plot(y=['cyberlinks_per_day', 'volt_supply', 'volt_liquid_supply'], figsize=figsize,
                 xticks=range(0, 3650, 365), grid=True, title=title)
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def volt_and_ampere_supply_plot(df, title='volt and ampere supply', figsize=(16, 9)):
    columns = ['volt_supply', 'ampere_supply']
    df.plot.area(y=columns, linewidth=0, colormap="winter", xticks=range(0, 3650, 365), grid=True, figsize=figsize, title=title)
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def cyberlinks_count_plot(df, title='cyberlinks count and ampere supply', figsize=(16, 9)):
    ax1 = df.plot.line(x='timestep', y='cyberlinks_count', grid=True, xticks=range(0, 3650, 365), figsize=figsize, title=title)
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df.plot.line(ax=ax2, y=['ampere_supply', 'ampere_liquid_supply'], figsize=figsize, xticks=range(0, 3650, 365),
                      grid=True)
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def mint_rate_plot(df, title='ampere and volt mint rate investmint max', figsize=(16, 9)):
    ax1 = df.plot(y=['ampere_mint_rate', 'volt_mint_rate'], figsize=figsize, xticks=range(0, 3650, 365), grid=True, title=title)
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df.plot.line(ax=ax2, y='investmint_max_period', figsize=figsize, xticks=range(0, 3650, 365),
                      style={'investmint_max_period': 'r'}, grid=True)
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def gpu_memory_usage_plot(df, title='gpu memory usage', figsize=(16, 9)):
    ax1 = df.plot(y=['ampere_supply', 'cyberlinks_count'], figsize=figsize, xticks=range(0, 3650, 365), grid=True, title=title)
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df.plot.line(ax=ax2, y='gpu_memory_usage', figsize=figsize, xticks=range(0, 3650, 365),
                      style={'gpu_memory_usage': 'r'}, grid=True)
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()