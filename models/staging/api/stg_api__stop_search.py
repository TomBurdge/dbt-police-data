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

    url_pairs = set()
    for dict in searches:
        forces = dict.get("stop-and-search")
        for force in forces:
            url = f"https://data.police.uk/api/stops-no-location?force={force}"
            url_pairs.add((force, url))
    return url_pairs


def get_stop_search_data(url_pairs: str):
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
    for i, url_pair in enumerate(url_pairs):
        force = url_pair[0].replace("-", " ")
        url = url_pair[1]
        print(i, "/", len(url_pairs), "Police URLs processed.")
        r = requests.get(url)
        content = json.loads(r.content)
        if content:
            result = (
                pl.DataFrame(content, schema=df_schema)
                .unnest("outcome_object")
                .with_columns(pl.lit(force).alias("force"))
                .with_columns(
                    pl.col("datetime").str.strptime(
                        pl.Datetime,
                        "%Y-%m-%dT%H:%M:%S%z",
                    )
                )
            )
            if df is None:
                df = result

            else:
                try:
                    df = df.vstack(result)
                except Exception as e:
                    print("An Error occured while calling the API : ", e)
                    print(df.schema)
                    exit()

            # see api call limits: https://data.police.uk/docs/api-call-limits/
            time.sleep(0.01)
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
