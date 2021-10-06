# import plotly.express as px
# import seaborn as sns
# import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = './images/'
_figsize = (16, 7)
_xticks = range(0, 4015, 365)
_xlabel = "timestep(days)"


def boot_supply_plot(df, title='boot supply and inflation rate', figsize=_figsize):
    columns = ['boot_liquid_supply', 'boot_frozen_supply', 'boot_bonded_supply']
    ax1 = df.plot.area(y=columns, linewidth=0, colormap="winter", xticks=_xticks, grid=True, figsize=figsize)
    ax1.set(xlabel=_xlabel, ylabel="boots")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    ax2.set(ylabel="rate")
    df.plot.line(ax=ax2, y='boot_inflation_rate', figsize=figsize, xticks=_xticks, grid=True)
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def hydrogen_supply_plot(df, title='hydrogen supply', figsize=_figsize):
    ax = df.plot.line(y='hydrogen_supply', figsize=figsize, xticks=_xticks, grid=True)
    ax.set(xlabel=_xlabel, ylabel="hydrogens")
    ax.set_title(title, size=16, fontweight="bold")
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def agents_count_plot(df, title='agents count', figsize=_figsize):
    ax = df.plot.line(y='agents_count', figsize=figsize, xticks=_xticks, grid=True)
    ax.set(xlabel=_xlabel, ylabel="count")
    ax.set_title(title, size=16, fontweight="bold")
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def capitalization_plot(df, title='cap in eth and cap per agent', figsize=_figsize):
    ax1 = df.plot(y='capitalization_per_agent', figsize=figsize, xticks=_xticks, grid=True, style={'capitalization_per_agent': 'r'}, logy=True)
    ax1.set(xlabel=_xlabel, ylabel="eth")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    ax2.set(ylabel="eth")
    df.plot.line(ax=ax2, y='capitalization_in_eth', figsize=figsize, xticks=_xticks, grid=True)
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def gboot_price_plot(df, title='gboot price and validators revenue', figsize=_figsize):
    ax1 = df.plot(y='gboot_price', figsize=figsize, xticks=_xticks, grid=True, style={'gboot_price': 'r'})
    ax1.set(xlabel=_xlabel, ylabel="eth")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    ax2.set(ylabel="gboot")
    df.plot.line(ax=ax2, y='validator_revenue_gboot', figsize=figsize, xticks=_xticks, grid=True, )
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def cyberlinks_per_day_plot(df, title='cyberlinks per day', figsize=_figsize):
    ax1 = df.plot(y=['cyberlinks_per_day', 'volt_supply', 'volt_liquid_supply'], figsize=figsize, xticks=_xticks,
                  style={'cyberlinks_per_day': 'r'}, grid=True)
    ax1.set(xlabel="timestep", ylabel="cyberlinks | volts")
    ax1.set_title(title, size=16, fontweight="bold")
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def cyberlinks_count_plot(df, title='cyberlinks count', figsize=_figsize):
    ax1 = df.plot(y=['cyberlinks_count'], figsize=figsize, xticks=_xticks, grid=True)
    ax1.set_title(title, size=16, fontweight="bold")
    # ax1 = df.plot.line(x='timestep', y='cyberlinks_count', grid=True, xticks=range(0, 3650, 365), figsize=figsize, title=title)
    # ax2 = ax1.twinx()
    # ax2.spines['right'].set_position(('axes', 1.0))
    # df.plot.line(ax=ax2, y=['ampere_supply', 'ampere_liquid_supply'], figsize=figsize, xticks=range(0, 3650, 365),
    #                   grid=True)
    # # plt.legend(bbox_to_anchor=(1.0, 1.0))
    ax1.set_title(title, size=16, fontweight="bold")
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def volt_and_ampere_supply_plot(df, title='volt and ampere supply', figsize=_figsize):
    columns = ['volt_supply', 'ampere_supply']
    ax1 = df.plot.area(y=columns, linewidth=0, colormap="winter", xticks=_xticks, grid=True, figsize=figsize)
    ax1.set(xlabel=_xlabel, ylabel="tokens")
    ax1.set_title(title, size=16, fontweight="bold")
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def mint_rate_plot(df, title='ampere and volt mint rate investmint max', figsize=_figsize):
    ax1 = df.plot(y=['ampere_mint_rate', 'volt_mint_rate'], figsize=figsize, xticks=_xticks, grid=True)
    ax1.set(xlabel=_xlabel, ylabel="share")
    ax1.set_title(title, size=16, fontweight="bold")
    ax2 = ax1.twinx()
    ax2.set(ylabel="days")
    ax2.spines['right'].set_position(('axes', 1.0))
    df.plot.line(ax=ax2, y='investmint_max_period', figsize=figsize, xticks=_xticks,
                      style={'investmint_max_period': 'r'}, grid=True)
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()


def gpu_memory_usage_plot(df, title='gpu memory usage', figsize=_figsize):
    ax1 = df.plot(y=['ampere_supply', 'cyberlinks_count'], figsize=figsize, xticks=_xticks, grid=True, title=title)
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    df.plot.line(ax=ax2, y='gpu_memory_usage', figsize=figsize, xticks=range(0, 3650, 365),
                      style={'gpu_memory_usage': 'r'}, grid=True)
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    plt.savefig(path + title.replace(' ', '_') + '.png')
    plt.show()