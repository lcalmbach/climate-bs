def show_spiral_old(self):
    """
    Show temperature spiral using code from https://www.dataquest.io/blog/climate-temperature-spirals-python/

    Args:
        df (_type_): _description_
    """
    #
    def plot_rings(min, rings):
        full_circle_thetas = np.linspace(0, 2 * np.pi, 1000)
        blue_line_one_radii = [rings[0]] * 1000
        red_line_one_radii = [rings[1]] * 1000
        red_line_two_radii = [rings[2]] * 1000
        ax1.plot(full_circle_thetas, blue_line_one_radii, c="blue")
        ax1.plot(full_circle_thetas, red_line_one_radii, c="orange")
        ax1.plot(full_circle_thetas, red_line_two_radii, c="red")

        buffer = 0.02
        ax1.text(
            np.pi / 2,
            rings[0] + buffer,
            f"{rings[0]-min} °C",
            color="blue",
            ha="center",
            fontdict={"fontsize": 20},
        )
        ax1.text(
            np.pi / 2,
            rings[1] + buffer,
            f"{rings[1]-min} °C",
            color="orange",
            ha="center",
            fontdict={"fontsize": 20},
        )
        ax1.text(
            np.pi / 2,
            rings[2] + buffer,
            f"{rings[2]-min} °C",
            color="red",
            ha="center",
            fontdict={"fontsize": 20},
        )

    def get_data(datasource_id: int):
        if datasource_id == 1:
            df = pd.read_csv(
                HADCRUT_FILE, delim_whitespace=True, usecols=[0, 1], header=None
            )
            df["year"] = df.iloc[:, 0].apply(lambda x: x.split("/")[0]).astype(int)
            df["month"] = df.iloc[:, 0].apply(lambda x: x.split("/")[1]).astype(int)
            min_year = df["year"].min()
            df = df.rename(columns={1: "value"})
            df = df.iloc[:, 1:]
            df = df.set_index(["year", "month"])
            df -= df.loc[min_year:1900].mean()
            df = df.reset_index()
        else:
            df = self.data[["Year", "Month", "Temperature_diff"]]
            df.columns = ["year", "month", "value"]
            # remove current year
            df = df.reset_index()
        df = df[df["year"] < datetime.now().year]
        return df

    def plot_year():
        ax1.text(0, 0, str(year - 1), color="#000100", size=30, ha="center")
        ax1.text(0, 0, str(year), color=clr, size=30, ha="center")

    plot_placeholder = st.empty()
    option_datasources = ["Station Basel/Binningen", "Globale Temperatur"]
    datasource = st.sidebar.selectbox("Datenquelle", options=option_datasources)
    datasource_id = option_datasources.index(datasource)
    temperature_df = get_data(datasource_id)
    fig = plt.figure(figsize=(14, 14))
    ax1 = plt.subplot(111, projection="polar")

    ax1.axes.get_yaxis().set_ticklabels([])
    ax1.axes.get_xaxis().set_ticklabels([])
    fig.set_facecolor("#323331")
    years = temperature_df["year"].unique()

    theta = np.linspace(0, 2 * np.pi, 12)
    min_year = temperature_df["year"].min()
    max_year = temperature_df["year"].max()
    ax1.grid(False)
    ax1.set_title(
        SPIRAL[datasource_id]["title"].format(min_year, max_year),
        color="white",
        fontdict={"fontsize": 20},
    )
    min = np.abs(np.floor(temperature_df["value"].min()))
    max = min + np.ceil(temperature_df["value"].max()) + 0.5
    ax1.set_ylim(0, max)
    ax1.set_facecolor("#000100")
    animate_plot = st.sidebar.checkbox("Animation")

    plot_rings(min, SPIRAL[datasource_id]["rings"])
    for index, year in enumerate(years):
        r = temperature_df[temperature_df["year"] == year]["value"] + min
        clr = plt.cm.viridis(index * 2)
        plot_year()
        ax1.plot(theta, r, c=clr)
        if (animate_plot) & (year % 10 == 0):
            plot_placeholder.pyplot(fig)

    plot_year()
    plot_rings(min, SPIRAL[datasource_id]["rings"])
    plot_placeholder.pyplot(fig)
    st.markdown(
        f"""Datenquelle: {SPIRAL[datasource_id]['datasource']}, 
        Code angepasst von: [Generating Climate Temperature Spirals in Python](https://www.dataquest.io/blog/climate-temperature-spirals-python/)"""
    )
    st.markdown(f"""Die Normperiode entspricht dem Mittel der Jahre {min_year}-1900""")
