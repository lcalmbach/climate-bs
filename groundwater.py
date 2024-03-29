import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import os

# local
from const import *
from texts import *
import plots


class Groundwater:
    def __init__(self):
        self.type = type
        self.data = self.get_data()

    def get_data(self):
        def read_data_from_source():
            def extract_lat(x):
                return json.loads(x)[0]

            def extract_long(x):
                return json.loads(x)[1]

            response = requests.get(GROUNDWATER_URL)
            st.write(GROUNDWATER_URL)
            if response.status_code == 200:
                data = response.json()["records"]
                st.write(data)
                df = [
                    {
                        "stationnr": x["record"]["fields"]["stationnr"],
                        "geopoint": x["record"]["fields"]["geo_point_2d"],
                        "stationname": x["record"]["fields"]["stationname"],
                        "month": x["record"]["fields"]["month(timestamp)"],
                        "year": x["record"]["fields"]["year(timestamp)"],
                        "temperature": x["record"]["fields"]["avg_value"],
                    }
                    for x in data
                ]
                df = pd.DataFrame(df)
                df["longitude"] = df["geopoint"].apply(extract_long)
                df["latitude"] = df["geopoint"].apply(extract_lat)
                df[["month", "year"]] = df[["month", "year"]].astype(int)
                df = df.drop(columns=["geopoint"])
                df.to_parquet(GROUNDWATER_FILE, compression="GZIP")
                print(len(df))
                return df

        if os.path.exists(GROUNDWATER_FILE):
            df = pd.read_parquet(GROUNDWATER_FILE)
        else:
            df = read_data_from_source()
        return df

    def show_spiral(self):
        station_options = ["Alle Stationen"] + sorted(
            list(self.data["stationname"].unique())
        )
        sel_station = st.sidebar.selectbox("Station", options=station_options)
        df = self.data
        if station_options.index(sel_station) == 0:
            df = (
                df[["month", "year", "temperature"]]
                .groupby(["month", "year"])
                .agg("mean")
                .reset_index()
            )
        else:
            df = df[df["stationname"] == sel_station]
        min_year, max_year = int(df["year"].min()), int(df["year"].max())
        sel_years = st.sidebar.slider(
            "Jahr", min_value=min_year, max_value=max_year, value=(min_year, max_year)
        )

        if sel_years != [min_year, max_year]:
            df = df[(df["year"] >= sel_years[0]) & (df["year"] <= sel_years[1])]
        df = df[["month", "year", "temperature"]].sort_values(by=["year", "month"])
        df.columns = ["month", "year", "value"]
        min = np.floor(df["value"].min())
        max = min + np.ceil(df["value"].max()) + 0.5

        st.markdown(GW_SPIRAL_LEGEND_PRE)
        plots.line_chart_3d(df, min, max)
        with st.expander("Show Data", expanded=False):
            st.table(df[["year", "month", "value"]])
        st.markdown(GW_SPIRAL_LEGEND_POST)

    def show_menu(self):
        plot_type_options = ["Spirale"]
        sel_plottype = st.sidebar.selectbox("Darstellung", options=plot_type_options)

        if plot_type_options.index(sel_plottype) == 0:
            self.show_spiral()
