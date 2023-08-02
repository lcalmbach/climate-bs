import locale


def get_max_month_name(df, date_col):
    locale.setlocale(locale.LC_TIME, "de_DE")
    max_date = df[date_col].max()
    return max_date.strftime("%B")
