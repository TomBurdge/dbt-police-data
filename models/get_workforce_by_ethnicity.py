import polars as pl


def model(dbt, session):
    """
    The function retrieves data on the ethnicity of police officers from a
    specific URL and returns it as a pandas DataFrame.

    :param dbt: The "dbt" parameter is likely referring to a database
    connection or a database object that is used to interact with a database.
    It is standard for a python model in dbt and unused here.
    :param session: The "session" parameter is typically used to establish a
    connection or session with a database.
    It is standard for a python model in dbt and unused here.
    :return: a DataFrame object named "df".
    """
    url = "https://www.ethnicity-facts-figures.service.gov.uk\
/workforce-and-business/workforce-diversity/police-workforce\
/latest/downloads/by-ethnicity-police-officers.csv"
    return pl.read_csv(url)
