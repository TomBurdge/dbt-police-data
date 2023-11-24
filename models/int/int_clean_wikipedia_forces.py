from polars import Float32, col, when


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
    df = dbt.ref("stg_wikipedia__forces").pl()
    df = df.with_columns(
        col("Force").str.replace(
            r"(?i)Constabulary| Police|Police Service of |Police | Service|,", ""
        ),
        col("Number of police officers")
        .str.replace(r"\[[^\]]*\]", "")
        .str.replace(",", "")
        .cast(Float32),
        col("Budget (millions)")
        .str.lstrip("£")
        .str.replace(r"\[[^\]]*\]", "")
        .str.replace(",", "")
        .cast(Float32),
        col("Area size (km2)")
        .str.lstrip("£")
        .str.replace(r"\[[^\]]*\]", "")
        .str.replace(r"(?i)-|—", ""),
    )
    df = df.with_columns(
        [
            when(col("Area size (km2)").str.lengths() == 0)
            .then(None)
            .otherwise(col("Area size (km2)"))
            .cast(Float32)
            .keep_name()
        ]
    )

    return df
