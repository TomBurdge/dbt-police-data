import json
import time

import polars as pl
import requests


def get_available_data(available_data: str):
    """
    The function `get_available_data` retrieves available data for
    stop-and-searches from a given URL and returns a set of force names
    and corresponding URLs.

    :param available_data: The `available_data` parameter is a string that
    represents the URL from which the available data can be retrieved
    :type available_data: str
    :return: a set of tuples, where each tuple contains a force name and a
    corresponding URL.
    """
    r = requests.get(available_data)
    searches = json.loads(r.content)

    url_tuples = set()
    base_url = "https://data.police.uk/api/stops-no-location?"
    for dict in searches:
        forces = dict.get("stop-and-search")
        date = dict.get("date")
        for force in forces:
            url = base_url + f"force={force}&date={date}"
            url_tuples.add((force, date, url))
    return url_tuples


def get_stop_search_data(url_tuples: str):
    """
    The function `get_stop_search_data` retrieves data from multiple URLs,
    processes the content, and returns a DataFrame containing the results.

    :param url_pairs: The `url_pairs` parameter is a list of tuples.
    Each tuple contains two elements: the first element is the force name,
    and the second element is the URL to fetch the data from. The function
    iterates over each URL in the `url_pairs` list, makes a GET request to the
    :type url_pairs: str
    :return: a DataFrame object.
    """
    df = None
    df_schema = [
        ("age_range", pl.Utf8),
        ("outcome", pl.Utf8),
        ("involved_person", pl.Boolean),
        ("self_defined_ethnicity", pl.Utf8),
        ("gender", pl.Utf8),
        ("legislation", pl.Utf8),
        ("outcome_linked_to_object_of_search", pl.Boolean),
        ("datetime", pl.Utf8),
        ("removal_of_more_than_outer_clothing", pl.Boolean),
        (
            "outcome_object",
            pl.Struct([pl.Field("id", pl.Utf8), pl.Field("name", pl.Utf8)]),
        ),
        ("location", pl.Utf8),
        ("operation", pl.Boolean),
        ("officer_defined_ethnicity", pl.Utf8),
        ("type", pl.Utf8),
        ("operation_name", pl.Utf8),
        ("object_of_search", pl.Utf8),
    ]
    for i, url_tuple in enumerate(url_tuples):
        force = url_tuple[0].replace("-", " ")
        date = url_tuple[1]
        url = url_tuple[2]
        print(i, "/", len(url_tuples), "Police URLs processed.")
        r = requests.get(url)
        content = json.loads(r.content)
        try:
            if content:
                result = (
                    pl.DataFrame(content, schema=df_schema)
                    .unnest("outcome_object")
                    .with_columns(pl.lit(force).alias("force"))
                    # .with_columns(
                    #     pl.col("datetime")
                    #     # .str.rstrip("+00:00")
                    #     .str.strptime(
                    #         pl.Datetime,
                    #         "%Y-%m-%dT%H:%M:%S%z",
                    #     )
                    # )
                    .with_columns(
                        pl.lit(date)
                        .alias("month")
                        .str.strptime(
                            pl.Datetime,
                            "%Y-%m",
                        )
                    )
                )
                if df is None:
                    df = result

                else:
                    df = df.vstack(result)

                # see api call limits:
                # https://data.police.uk/docs/api-call-limits/
                time.sleep(0.01)
        except Exception as e:
            print("An Error occured while calling the API : ", e)
            exit()
    return df


def model(dbt, session):
    """
    The `model` function retrieves stop search data from the police API using
    available data from the provided URL.

    :param dbt: The "dbt" parameter is likely referring to a database
    connection or a database object that is used to interact with a database.
    It is standard for a python model in dbt and unused here.
    :param session: The "session" parameter is typically used to establish a
    connection or session with a database.
    It is standard for a python model in dbt and unused here.
    :return: a DataFrame object named "df".
    """
    url = "https://data.police.uk/api/crimes-street-dates"
    force_url_pairs = get_available_data(url)

    df = get_stop_search_data(force_url_pairs).with_columns(pl.col("force"))

    return df


if __name__ == "__main__":
    model("hello", "world")
