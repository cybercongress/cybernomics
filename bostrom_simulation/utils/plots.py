import plotly.express as px
import seaborn as sns


def df_preparator(df):
    # df = df.drop(df[df['timestep']%10 != 0].index)
    return df


year = dict(
        tick0 = 0,
        dtick = 365
    )


def linear_plot(df, _y, render='sns'):
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