"""Description: Module for data cleaning for Pixel data."""

import polars as pl


def json_to_dataframe(json_path: str) -> pl.DataFrame:
    """
    Purpose:
        Convert path to json file into Polars DataFrame.
    Args:
        json_path: Path to json file.
    Returns:
        json_data: JSON data as a Polars DataFrame.
    """
    return pl.read_json(json_path)


def daily_average_score(data: pl.DataFrame) -> pl.DataFrame:
    """
    Purpose:
        Create an overall score per day based on how many numbers were saved per day.
    Args:
        data: Dataset to work on.
    Returns:
        data: Dataset with new daily score.
    """
    data = data.with_columns(
        average_score=pl.col("scores").list.sum() / pl.col("scores").list.len(),
    )

    return data


def clean_date(data: pl.DataFrame) -> pl.DataFrame:
    """
    Purpose:
        Clean date by converting to DateTime, and creating year and month columns.
    Args:
        data: Dataset to work on.
    Returns:
        data: Dataset with cleaned date columns.
    """
    # Convert date to DateTime format.
    data = data.with_columns(pl.col("date").str.to_date("%Y-%m-%d")).set_sorted("date")

    # Get min and max dates for finding missed Pixels.
    min_date = data["date"].min()
    max_date = data["date"].max()
    all_dates = pl.date_range(min_date, max_date, interval="1d", eager=True)
    all_dates = pl.DataFrame({"date": all_dates})
    joined_dates = all_dates.join(data, on="date", how="left")

    missing_dates = joined_dates.filter(pl.col("average_score").is_null())

    print(
        f"You didn't enter a Pixel for these days:\n{missing_dates}\nThese days have been omitted.",
    )

    return data


def add_year_and_month_columns(data: pl.DataFrame) -> pl.DataFrame:
    """
    Purpose:
        Add year and month columns for further analysis as well as mean scores.
    Args:
        data: Dataset to work on.
    Returns:
        data: Dataset with year and month columns.
    """
    # Create new columns for year and year/month.
    data = data.with_columns([
        data["date"].dt.year().alias("year"),
        data["date"].dt.month().alias("month"),
    ])

    # Find mean for year & year/month.
    data = data.with_columns([
        pl.col("average_score").mean().over("year").alias("yearly_mean_score"),
        pl.col("average_score").mean().over(["year", "month"]).alias("monthly_mean_score"),
    ])

    return data


def create_word_and_char_columns(data: pl.DataFrame) -> pl.DataFrame:
    """
    Purpose:
        Convert empty "notes" entries to Null, and create "word_count" and "char_count" columns.
        Null entries in "notes" will result in Null in the new columns.
    Args:
        data: Dataset with "notes" column to work on.
    Returns:
        data:
            Dataset with empty notes replaced by Null,
            and new word/char count columns.
    """
    # If a notes entry for a day is empty, change it to Null.
    data = data.with_columns(
        pl.when(pl.col("notes").str.len_chars() == 0)
        .then(pl.lit(None))
        .otherwise(pl.col("notes"))
        .alias("notes"),
    )

    data = data.with_columns([
        # Count words by splitting with whitespace & list length.
        pl.col("notes").str.split(" ").list.len().alias("word_count"),
        # Count characters.
        pl.col("notes").str.len_chars().alias("char_count"),
    ])

    return data


def data_cleaning_driver(json_path: str) -> pl.DataFrame:
    """
    Purpose:
        Outline the data_cleaning pipeline and call methods in order.
    Args:
        json_path: String to JSON file. This will later be replaced by user upload.
    Returns:
        data: Cleaned Polars DataFrame.
    """
    data = json_to_dataframe(json_path)  # Load path to json file.
    data = daily_average_score(data)  # Add an average score per day.
    data = clean_date(data)  # Clean data column.
    data = add_year_and_month_columns(data)  # Add year and month columns with mean scores.
    data = create_word_and_char_columns(data)  # Fill null values in notes with None.

    return data


if __name__ == "__main__":
    json_path = "data/PIXELS-BACKUP-2025-09-12T17_33_51.458262.json"
    data = data_cleaning_driver(json_path)
    print(data.head(-15))
