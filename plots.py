import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import const as cn
import datetime

def line_chart(df, settings):
    title = settings['title'] if 'title' in settings else ''
    if 'x_dt' not in settings: settings['x_dt'] = 'Q'
    if 'y_dt' not in settings: settings['y_dt'] = 'Q'
    chart = alt.Chart(df).mark_line(width = 2, clip=True).encode(
            x= alt.X(f"{settings['x']}:{settings['x_dt']}", scale=alt.Scale(domain=settings['x_domain'])),
            y= alt.Y(f"{settings['y']}:{settings['y_dt']}", scale=alt.Scale(domain=settings['y_domain'])),
            tooltip=settings['tooltip']    
        )
    if 'regression' in settings:
        line = chart.transform_regression(settings['x'], settings['y']).mark_line()
        plot = (chart + line).properties(width=settings['width'], height=settings['height'], title = title)
    else:
        plot = chart.properties(width=settings['width'], height=settings['height'], title = title)
    st.altair_chart(plot)

def scatter_plot(df, settings):
    title = settings['title'] if 'title' in settings else ''
    chart = alt.Chart(df).mark_circle(size=60).encode(
        x= alt.X(settings['x'], scale=alt.Scale(domain=settings['domain'])),
        y= alt.Y(settings['y'], scale=alt.Scale(domain=settings['domain'])),
        tooltip=settings['tooltip'],
        color=alt.Color(settings['color'], sort="descending", scale=alt.Scale(scheme='redblue'))
    ).interactive()
    plot = chart.properties(width=settings['width'], height=settings['height'], title = title)
    st.altair_chart(plot)


def wl_time_series_chart(df, settings):
    #line = alt.Chart(df_line).mark_line(color= 'red').encode(
    #    x= 'x',
    #    y= 'y'
    #    )


    chart = alt.Chart(df).mark_line().encode(
        x = alt.X(f"{settings['x']}:T", scale=alt.Scale(domain=settings['x_domain']), title=settings['x_title']),
        y = alt.Y(f"{settings['y']}:Q", scale=alt.Scale(domain=settings['y_domain']), title=settings['y_title']),
        tooltip = settings['tooltip']
    ).interactive()
    plot = chart.properties(width=settings['width'], height=settings['height'], title=settings['title'])
    st.altair_chart(plot)

def time_series_bar(df, settings):
    chart = alt.Chart(df).mark_bar(size=settings['size'], clip=True).encode(
        x = alt.X(f"{settings['x']}:T", title=settings['x_title'], scale=alt.Scale(domain=settings['x_domain'])),
        y = alt.Y(f"{settings['y']}:Q", title=settings['y_title']),
        tooltip=settings['tooltip']
    )
    plot = chart.properties(width=settings['width'], height=settings['height'], title = settings['title'])
    st.altair_chart(plot)


def time_series_line(df, settings):
    if 'x_domain' in settings:
        xax = alt.X(f"{settings['x']}:T", title=settings['x_title'], scale=alt.Scale(domain=settings['x_domain']))
    else:
        xax = alt.X(f"{settings['x']}:T", title=settings['x_title'])
    
    if settings['y_domain'][0] != settings['y_domain'][1]:
        yax = alt.Y(f"{settings['y']}:Q", title=settings['y_title'], scale=alt.Scale(domain=settings['y_domain']))
    else:  
        yax = alt.Y(f"{settings['y']}:Q", title=settings['y_title'])

    if 'color' in settings:
        chart = alt.Chart(df).mark_line(clip=True).encode(
            x = xax,
            y = yax,
            color = f"{settings['color']}:N",
            tooltip=settings['tooltip']
        )
    else:
        chart = alt.Chart(df).mark_line(clip=True).encode(
            x = xax,
            y = yax,
            tooltip=settings['tooltip']
        )

    if 'h_line' in settings:
        chart += alt.Chart(df).mark_line(clip=True, color='red').encode(
        x = xax,
        y = settings['h_line'],
        tooltip = settings['h_line'])
    
    if 'symbol_size' in settings:
        if not('symbol_opacity' in settings):
            settings['symbol_opacity'] = 0.6
        if 'color' in settings:
            chart += alt.Chart(df).mark_circle(size=settings['symbol_size'], clip=True, opacity=settings['symbol_opacity']).encode(
                x = xax,
                y = yax,
                color = f"{settings['color']}:N",
                tooltip = settings['tooltip']
            )
        else:
            chart += alt.Chart(df).mark_circle(size=settings['symbol_size'], opacity=settings['symbol_opacity']).encode(
                x = xax,
                y = yax,
                tooltip = settings['tooltip']
            )
    plot = chart.properties(width=settings['width'], height=settings['height'], title=settings['title'])
    st.altair_chart(plot)

def time_series_chart(df, settings):
    #line = alt.Chart(df_line).mark_line(color= 'red').encode(
    #    x= 'x',
    #    y= 'y'
    #    )
    title = settings['title'] if 'title' in settings else ''
    if 'x_title' not in settings:
        settings['x_title'] = ''
    plot = alt.Chart(df).mark_line(point=alt.OverlayMarkDef(color='blue')).encode(
        x= alt.X(f"{settings['x']}:T", title=settings['x_title']),#, scale=alt.Scale(domain=settings['x_domain']), ),
        y= alt.Y(f"{settings['y']}:Q", scale=alt.Scale(domain=settings['y_domain']), title=settings['y_title']),
        tooltip=settings['tooltip']
    )
    if 'show_regression' in settings:
        if settings['show_regression']:
            line = plot.transform_regression(settings['x'], settings['y']).mark_line(color='orange')
            plot += line
    if 'show_average' in settings:
        if settings['show_average']:
            avg = df[settings['y']].mean()
            df_avg = pd.DataFrame({'x':[df[settings['x']].min(), df[settings['x']].max()], 'y':[avg, avg]})
            line = alt.Chart(df_avg).mark_line(color= 'red').encode(
                x= 'x',
                y= 'y',
            )
            plot += line
    plot = plot.properties(width=settings['width'], height=settings['height'], title = title)
    st.altair_chart(plot)


def heatmap(df, settings):
    title = settings['title'] if 'title' in settings else ''
    plot = alt.Chart(df).mark_rect().encode(
        x=alt.X(settings['x'],
            sort=list(cn.MONTHS_REV_DICT.keys())),
        y=alt.Y(settings['y'],
            sort=alt.EncodingSortField(field = 'jahr', order='descending'),
        ),
        color=settings['color'],
        tooltip=settings['tooltip']
    ).properties(width=settings['width'], title = title)
    st.altair_chart(plot)


def bar_chart(df:pd.DataFrame, settings:dict):
    if 'title' not in settings:
        settings['title'] = ''
    # if 'tooltip' not in settings:
    settings['tooltip'] = [settings['x'], settings['y']]
    bar_width = settings['width'] / len(df) * .75
    plot = alt.Chart(df).mark_bar(size=bar_width).encode(
        x=f"{settings['x']}:N",
        y=settings['y'],
        tooltip=settings['tooltip'] 
    )
    if 'h_line' in settings:
        plot += alt.Chart(df).mark_line(color='red').encode(
            x=f"{settings['x']}:N",
            y = settings['h_line'],
        )

    plot = plot.properties(title = settings['title'],width=settings['width'], height=settings['height'])

    return st.altair_chart(plot)

def histogram(df:pd.DataFrame, settings:dict):
    def get_x_domain():
        x_domain = [df[settings['x']].min(), df[settings['x']].max()]
        if 'show_current_month' in settings:
            if x_domain[0] > settings['show_current_month']:
                x_domain[0] = settings['show_current_month']
            if x_domain[1] < settings['show_current_month']:
                x_domain[1] = settings['show_current_month']
        if x_domain[1] % 2 != 0:
            x_domain[1] += 1
        return x_domain
        
    bins=20
    x_domain = get_x_domain()
    if 'title' not in settings:
        settings['title'] = ''
    plot = alt.Chart(df).mark_bar().encode(
        x=alt.X(settings['x'], 
                bin=alt.BinParams(maxbins=bins),
                scale = alt.Scale(domain=x_domain),
                title = settings['x_title']
        ),
        y = alt.Y('count()', title = settings['y_title']),
        tooltip=[settings['x'], 'count()'],
    )

    if 'show_current_month' in settings:
        df_line = pd.DataFrame( {'x':[settings['show_current_month']], 'y':[0]} )
        current_month_dot = alt.Chart(df_line).mark_circle(size = 100, color='red').encode(
            x = alt.X('x:Q',
                    scale=alt.Scale(domain=x_domain)),
            y = alt.Y('y:Q'),
        )
    

    if 'show_current_month' in settings:
        plot += current_month_dot
    plot = plot.properties(title = settings['title'], width=settings['width'], height=settings['height'])
    return st.altair_chart(plot)