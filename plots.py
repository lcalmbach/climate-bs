import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import const as cn


def line_chart(df, settings):
    title = settings["title"] if "title" in settings else ""
    if "x_dt" not in settings:
        settings["x_dt"] = "Q"
    if "y_dt" not in settings:
        settings["y_dt"] = "Q"
    chart = (
        alt.Chart(df)
        .mark_line(width=2, clip=True, opacity=0.5)
        .encode(
            x=alt.X(
                f"{settings['x']}:{settings['x_dt']}",
                scale=alt.Scale(domain=settings["x_domain"]),
            ),
            y=alt.Y(
                f"{settings['y']}:{settings['y_dt']}",
                scale=alt.Scale(domain=settings["y_domain"]),
            ),
            tooltip=settings["tooltip"],
            color=alt.Color(
                settings["color"], scale=alt.Scale(scheme="redblue", reverse=True)
            ),
        )
    )
    if "regression" in settings:
        line = chart.transform_regression(settings["x"], settings["y"]).mark_line()
        plot = (chart + line).properties(
            width=settings["width"], height=settings["height"], title=title
        )
    else:
        plot = chart.properties(
            width=settings["width"], height=settings["height"], title=title
        )
    st.altair_chart(plot)


def scatter_plot(df, settings):
    title = settings["title"] if "title" in settings else ""
    chart = (
        alt.Chart(df)
        .mark_circle(
            size=60,
        )
        .encode(
            x=alt.X(settings["x"], scale=alt.Scale(domain=settings["domain"])),
            y=alt.Y(settings["y"], scale=alt.Scale(domain=settings["domain"])),
            tooltip=settings["tooltip"],
            color=alt.Color(
                settings["color"], sort="ascending", scale=alt.Scale(scheme="bluered")
            ),
        )
        .interactive()
    )
    plot = chart.properties(
        width=settings["width"], height=settings["height"], title=title
    )
    st.altair_chart(plot)


def time_series_bar(df, settings):
    chart = (
        alt.Chart(df)
        .mark_bar(size=settings["size"], clip=True)
        .encode(
            x=alt.X(
                f"{settings['x']}:T",
                title=settings["x_title"],
                scale=alt.Scale(domain=settings["x_domain"]),
            ),
            y=alt.Y(f"{settings['y']}:Q", title=settings["y_title"]),
            tooltip=settings["tooltip"],
        )
    )
    plot = chart.properties(
        width=settings["width"], height=settings["height"], title=settings["title"]
    )
    st.altair_chart(plot)


def time_series_line(df, settings):
    if "x_domain" in settings:
        xax = alt.X(
            f"{settings['x']}:T",
            title=settings["x_title"],
            scale=alt.Scale(domain=settings["x_domain"]),
        )
    else:
        xax = alt.X(f"{settings['x']}:T", title=settings["x_title"])

    if settings["y_domain"][0] != settings["y_domain"][1]:
        yax = alt.Y(
            f"{settings['y']}:Q",
            title=settings["y_title"],
            scale=alt.Scale(domain=settings["y_domain"]),
        )
    else:
        yax = alt.Y(f"{settings['y']}:Q", title=settings["y_title"])

    if "color" in settings:
        chart = (
            alt.Chart(df)
            .mark_line(clip=True)
            .encode(
                x=xax,
                y=yax,
                color=f"{settings['color']}:N",
                tooltip=settings["tooltip"],
            )
        )
    else:
        chart = (
            alt.Chart(df)
            .mark_line(clip=True)
            .encode(x=xax, y=yax, tooltip=settings["tooltip"])
        )

    if "h_line" in settings:
        chart += (
            alt.Chart(df)
            .mark_line(clip=True, color="red")
            .encode(x=xax, y=settings["h_line"], tooltip=settings["h_line"])
        )

    if "symbol_size" in settings:
        if not ("symbol_opacity" in settings):
            settings["symbol_opacity"] = 0.6
        if "color" in settings:
            chart += (
                alt.Chart(df)
                .mark_circle(
                    size=settings["symbol_size"],
                    clip=True,
                    opacity=settings["symbol_opacity"],
                )
                .encode(
                    x=xax,
                    y=yax,
                    color=f"{settings['color']}:N",
                    tooltip=settings["tooltip"],
                )
            )
        else:
            chart += (
                alt.Chart(df)
                .mark_circle(
                    size=settings["symbol_size"], opacity=settings["symbol_opacity"]
                )
                .encode(x=xax, y=yax, tooltip=settings["tooltip"])
            )
    plot = chart.properties(
        width=settings["width"], height=settings["height"], title=settings["title"]
    )
    st.altair_chart(plot)


def time_series_chart(df, settings):
    # line = alt.Chart(df_line).mark_line(color= 'red').encode(
    #    x= 'x',
    #    y= 'y'
    #    )
    title = settings["title"] if "title" in settings else ""
    if "x_title" not in settings:
        settings["x_title"] = ""
    if "symbol_size" not in settings:
        settings["symbol_size"] = 0
    if "rolling_avg_window" not in settings:
        settings["rolling_avg_window"] = 0
    plot = (
        alt.Chart(df)
        .mark_line(point=alt.OverlayMarkDef(color="blue", size=settings["symbol_size"]))
        .encode(
            x=alt.X(
                f"{settings['x']}:T", title=settings["x_title"]
            ),  # , scale=alt.Scale(domain=settings['x_domain']), ),
            y=alt.Y(
                f"{settings['y']}:Q",
                scale=alt.Scale(domain=settings["y_domain"]),
                title=settings["y_title"],
            ),
            tooltip=settings["tooltip"],
        )
    )
    if "show_regression" in settings:
        if settings["show_regression"]:
            line = plot.transform_regression(settings["x"], settings["y"]).mark_line(
                color="orange"
            )
            plot += line
    if "show_average" in settings:
        if settings["show_average"]:
            avg = df[settings["y"]].mean()
            df_avg = pd.DataFrame(
                {
                    "x": [df[settings["x"]].min(), df[settings["x"]].max()],
                    "y": [avg, avg],
                }
            )
            line = (
                alt.Chart(df_avg)
                .mark_line(color="red")
                .encode(
                    x="x",
                    y="y",
                )
            )
            plot += line
    if settings["rolling_avg_window"] > 0:
        df["ma"] = (
            df[settings["y"]].rolling(window=settings["rolling_avg_window"]).mean()
        )
        # Create the chart
        line = (
            alt.Chart(df)
            .mark_line(color="green")
            .encode(x=f"{settings['x']}:T", y=f"ma:Q", strokeWidth=alt.value(3))
        )
        plot += line

    plot = plot.properties(
        width=settings["width"], height=settings["height"], title=title
    )
    st.altair_chart(plot)


def heatmap(df, settings):
    title = settings["title"] if "title" in settings else ""
    if not "show_numbers" in settings:
        settings["show_numbers"] = True
    if not "color_scheme" in settings:
        settings["color_scheme"] = "viridis"

    plot = (
        alt.Chart(df)
        .mark_rect()
        .encode(
            x=alt.X(settings["x"], sort=list(cn.MONTHS_REV_DICT.keys())),
            y=alt.Y(
                settings["y"],
                sort=alt.EncodingSortField(field="jahr", order="descending"),
            ),
            color=alt.Color(
                f"{settings['color']}:Q",
                scale=alt.Scale(range=["lightblue", "darkred"]),
            ),
            tooltip=settings["tooltip"],
        )
    )

    if settings["show_numbers"]:
        plot += plot.mark_text().encode(
            text=settings["color"], color=alt.value("black")
        )

    plot = plot.properties(width=settings["width"], title=title)
    st.altair_chart(plot)


def bar_chart(df: pd.DataFrame, settings: dict):
    if "title" not in settings:
        settings["title"] = ""
    # if 'tooltip' not in settings:
    settings["tooltip"] = [settings["x"], settings["y"]]
    bar_width = settings["width"] / len(df) * 0.75
    plot = (
        alt.Chart(df)
        .mark_bar(size=bar_width)
        .encode(x=f"{settings['x']}:N", y=settings["y"], tooltip=settings["tooltip"])
    )
    if "h_line" in settings:
        plot += (
            alt.Chart(df)
            .mark_line(color="red")
            .encode(
                x=f"{settings['x']}:N",
                y=settings["h_line"],
            )
        )

    plot = plot.properties(
        title=settings["title"], width=settings["width"], height=settings["height"]
    )

    return st.altair_chart(plot)


def histogram(df: pd.DataFrame, settings: dict):
    def get_x_domain():
        x_domain = [df[settings["x"]].min(), df[settings["x"]].max()]
        if "show_current_month" in settings:
            if x_domain[0] > settings["show_current_month"]:
                x_domain[0] = settings["show_current_month"]
            if x_domain[1] < settings["show_current_month"]:
                x_domain[1] = settings["show_current_month"]
        if x_domain[1] % 2 != 0:
            x_domain[1] += 1
        return x_domain

    bins = 20
    x_domain = get_x_domain()
    if "title" not in settings:
        settings["title"] = ""
    plot = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(
                settings["x"],
                bin=alt.BinParams(maxbins=bins),
                scale=alt.Scale(domain=x_domain),
                title=settings["x_title"],
            ),
            y=alt.Y("count()", title=settings["y_title"]),
            tooltip=[settings["x"], "count()"],
        )
    )

    if "show_current_month" in settings:
        df_line = pd.DataFrame({"x": [settings["show_current_month"]], "y": [0]})
        current_month_dot = (
            alt.Chart(df_line)
            .mark_circle(size=100, color="red")
            .encode(
                x=alt.X("x:Q", scale=alt.Scale(domain=x_domain)),
                y=alt.Y("y:Q"),
            )
        )

    if "show_current_month" in settings:
        plot += current_month_dot
    plot = plot.properties(
        title=settings["title"], width=settings["width"], height=settings["height"]
    )
    return st.altair_chart(plot)


def line_chart_3d(df, min, max):
    def value_to_xy(value, month):
        v = value - min
        # st.write(value, min ,v, month)
        origin = (np.abs(min) + max) / 2
        theta_radians = 2 * np.pi / 12 * (month - 1)
        x = origin + v * np.cos(theta_radians)
        y = origin + v * np.sin(theta_radians)
        return x, y

    rad_max: float = np.abs(min) + max + 1
    xl, yl, zl, clr = [], [], [], []
    df["x"] = 0
    df["y"] = 0
    df["z"] = 0

    for index, row in df.iterrows():
        x, y = value_to_xy(row["value"], row["month"])
        z = row["year"] + row["month"] / 12
        df.loc[index, "x"] = x
        df.loc[index, "y"] = y
        df.loc[index, "z"] = z

    df["text"] = (
        df["year"].map(str)
        + "/"
        + df["month"].map(str)
        + ": "
        + df["value"].round(1).map(str)
        + " °C"
    )
    ##color schemas: https://plotly.com/python/colorscales/#colorscales-in-dash
    fig = px.scatter_3d(
        df,
        x="x",
        y="y",
        z="z",
        color="value",
        color_continuous_scale="edge",  # px.colors.sequential.ed
        # this does not work
        hover_data={
            "year": True,
            "month": True,
            "value": ":.1f",
            "x": False,
            "y": False,
            "z": False,
        },
    )
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)
    fig.update_traces(mode="markers+lines")

    fig.update_layout(
        width=800,
        height=700,
        autosize=False,
        scene=dict(
            camera=dict(
                up=dict(x=0, y=0, z=1),
                eye=dict(
                    x=0,
                    y=1.0707,
                    z=1,
                ),
            ),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode="manual",
        ),
    )

    st.plotly_chart(fig, width=1000, height=1000)
