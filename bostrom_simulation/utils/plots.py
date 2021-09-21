import plotly.express as px
import seaborn as sns


def df_preparator(df):
    # df = df.drop(df[df['timestep']%10 != 0].index)
    return df


year = dict(
        tick0 = 0,
        dtick = 365
    )


def linear_plot(df, _y, render='sns', figsize: tuple=(11.7, 8.27)):
    if render == 'px':
        fig = px.line(
            df,
            x="timestep",
            y=_y,
            facet_col='simulation',
            template='seaborn'
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20), xaxis=year)
        fig.show()
    elif render == 'sns':
        sns.set(rc={'figure.figsize': (11.7, 8.27)})
        sns.lineplot(data=df, x='timestep', y=_y)


def scatter_plot(df, _y, render='sns'):
    if render == 'px':
        fig = px.scatter(
            df,
            x="timestep",
            y=_y,
            opacity=0.01,
            trendline="lowess",
            trendline_color_override="red",
            facet_col='simulation',
            labels={'color': _y}
        )
        fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), xaxis=year)
        fig.show()
    elif render == 'sns':
        sns.lmplot('timestep', _y, data=df, fit_reg=True)


def plot_line_2_diff_y(df, value_1, value_2, figsize: tuple = (16,9), value_1_log=False, value_2_log=False):
    value_1_df = df[[value_1]]
    value_2_df = df[[value_2]]
    ax1 = value_1_df.plot.line(figsize=figsize, logy=value_1_log, xticks=range(0, 3650, 365), grid=True)
    ax2 = ax1.twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    value_2_df.plot.line(ax=ax2, figsize=(16, 9), xticks=range(0, 3650, 365), style={value_2: 'r'}, logy=value_2_log, grid=True)


def plot_line_2_same_y(df, values:list, figsize: tuple = (16,9), value_1_log=False, value_2_log=False):
    df.plot(y=values, figsize=(16, 9), xticks=range(0, 3650, 365), grid=True)