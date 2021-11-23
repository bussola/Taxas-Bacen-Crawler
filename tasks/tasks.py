from crawler.series_list import get_series


def task_scrap_series():
    series_list = ["1", "11", "21", "433"]

    for serie in series_list:
        get_series(serie)
