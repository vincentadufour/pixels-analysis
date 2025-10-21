"""Description: Methods for data cleaning for pixel EDA."""

import string
from typing import NoReturn

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from textblob import TextBlob


# Formatting.
headline1 = "\n----------|"
headline2 = "|----------\n"
headline3 = "|---|"

# Number of top words to analyze.
TOP_N = 20

# Language to use for word analysis.
LANGUAGE = "english"


def heatmap_of_nulls(data: pd.DataFrame) -> NoReturn:
    """
    Purpose:
        Generate graph of heatmap of null values.
    Args:
        data: Polars Dataframe with Pixels data.
    """
    plt.figure(figsize=(10, 6))
    sns.heatmap(data.isna(), cbar=False, cmap="inferno")
    plt.title("Heatmap of Missing Data")
    plt.xlabel("Columns")
    plt.ylabel("Rows")

    plt.savefig("./plots/heatmap_of_nulls.png")
    plt.show()


def interactive_line_plot(data: pd.DataFrame) -> NoReturn:
    """
    Purpose:
        Generative interactive plot of monthly mean.
        TODO: Doesn't show the date when you interact with the graph.
    Args:
        data: Polars Dataframe with Pixels data.
    """
    fig = px.line(data, x=data.index, y="monthly_mean_score", title="Score Over Time")
    fig.show()


def interactive_seasonal_plot(data: pd.DataFrame) -> NoReturn:
    """
    Purpose:
        Generative seasonality plot.
    Args:
        data: Polars Dataframe with Pixels data.
    """
    data["smoothed"] = data["average_score"].rolling(window=7, center=True).mean()

    fig = px.line(
        data,
        x="date",
        y="smoothed",
        color="year",
        markers=True,
        title="Seasonal Plot of Score Across Years",
    )
    fig.update_layout(xaxis_title="month", yaxis_title="Average Score")
    fig.show()


def interactive_rolling_statistics_plot(data: pd.DataFrame) -> NoReturn:
    """
    Purpose:
        Generative rolling statistic plot that has a standard deviation.
    Args:
        data: Polars Dataframe with Pixels data.
    """
    window_size = 30

    rolling_mean = data["average_score"].rolling(window=window_size).mean()
    rolling_std = data["average_score"].rolling(window=window_size).std()

    fig = go.Figure()

    # Average score.
    fig.add_trace(go.Scatter(x=data["date"], y=data["average_score"], mode="lines", name="Score"))

    # Rolling mean based on window size.
    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=rolling_mean,
            mode="lines",
            name=f"{window_size}-Day Rolling Mean",
        ),
    )

    # Rolling standard deviation based on window size.
    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=rolling_std,
            mode="lines",
            name=f"{window_size}-Day Rolling Std Dev",
        ),
    )

    fig.update_layout(
        title="Rolling Statistics Plot: Score Over Time",
        xaxis_title="Date",
        yaxis_title="Score",
    )
    fig.show()


def box_plot(data: pd.DataFrame) -> NoReturn:
    """
    Purpose:
        Box plot of monthly and yearly averages.
    Args:
        data: Polars Dataframe with Pixels data.
    """
    # Monthly box plots.
    fig = px.box(data, x="month", y="average_score", title="Boxplot: Score by Month")
    fig.show()

    # Annual box plots.
    fig = px.box(data, x="year", y="average_score", title="Boxplot: Score by Year")
    fig.show()


def verbosity_plots(data: pd.DataFrame) -> NoReturn:
    """
    Purpose:
        Show a figure of four analytic plots:
            1. Regression plot of word count vs. score.
            2. Line plot of word count over time.
            3. Heatmap of word count over year and month.
            4. Bar plot of word count per year
    Args:
        data: Polars Dataframe with Pixels data.
    """
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))

    # regressional plot of word count vs. score
    sns.regplot(
        x="average_score",
        y="word_count",
        data=data,
        scatter_kws={"s": 50},
        line_kws={"color": "red"},
        ax=axs[0, 0],
    )
    axs[0, 0].set_title("Regressional Plot of Score & Word Count")
    axs[0, 0].set_xlabel("Score (per day)")
    axs[0, 0].set_ylabel("Word Count (per day)")

    # line plot of word count over time
    sns.lineplot(data, x=data.index, y="word_count", ax=axs[0, 1], color="darkred")
    axs[0, 1].set_title("Word Count on Timeline")
    axs[0, 1].set_xlabel("Date")
    axs[0, 1].set_ylabel("Word Count")

    # heatmap of word count over year and month
    heatmap_data = data.groupby(["year", "month"])["word_count"].mean().pivot_table()
    sns.heatmap(heatmap_data, annot=True, fmt=".2f", annot_kws={"size": 10}, ax=axs[1, 0])
    axs[1, 0].set_title("Heatmap of Word Count over Years & Months")

    # bar plot of word count per year
    fig = sns.barplot(
        data,
        x="year",
        y="word_count",
        palette="viridis",
        hue="year",
        legend=False,
        errorbar=None,
        ax=axs[1, 1],
    )
    fig.bar_label(fig.containers[1], fontsize=10)
    fig.bar_label(fig.containers[0], fontsize=10)
    fig.bar_label(fig.containers[2], fontsize=10)
    fig.bar_label(fig.containers[3], fontsize=10)
    axs[1, 1].set_title("Average Word Count per day by Year")
    axs[1, 1].set_xlabel("Year")
    axs[1, 1].set_ylabel("Average Word Count")

    # Show plot
    plt.tight_layout()
    plt.savefig("./verbosity_plots.png")
    plt.show()


def preprocess_text(note: str) -> str:
    """
    Purpose:
        Cleans note string by casting to lower case and remove punctuation.
    Args:
        note: String from note.
    Returns:
        note: Cleaned string for note.
    """
    if note is None:
        return ""

    note = note.lower()
    note = note.translate(str.maketrans("", "", string.punctuation))
    return note


def top_common_words(data: pd.DataFrame, language: str) -> NoReturn:
    """
    Purpose:
        Show common words used in notes.
        TODO: Need to add an option to select as many languages as CountVectorizer supports.
        TODO: Also feed it in as a list so people can select multiple languages.
    Args:
        data: Polars Dataframe with Pixels data.
        language: Language used in notes for matching words.
    """
    data["cleaned_notes"] = data["notes"].apply(preprocess_text)

    # Use CountVectorizer to count word occurrences.
    vectorizer = CountVectorizer(stop_words=language)
    word_count = vectorizer.fit_transform(data["cleaned_notes"])

    # Create a DataFrame with word counts
    word_counts = pd.DataFrame(word_count.toarray(), columns=vectorizer.get_feature_names_out())
    total_word_counts = word_counts.sum().sort_values(ascending=False)

    # Convert to DataFrame for better visualization.
    word_counts_df = pd.DataFrame(total_word_counts).reset_index()
    word_counts_df.columns = ["word", "count"]

    # Visualize the most common words.
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        x="count",
        y="word",
        data=word_counts_df.head(TOP_N),
        palette="magma",
        hue="word",
        legend=False,
    )
    plt.title(f"Top {TOP_N} Most Common Words in Journal Entries")
    plt.xlabel("Frequency")
    plt.ylabel("Words")

    # Bar labels.
    for p in ax.patches:
        width = p.get_width()
        ax.text(width + 0.5, p.get_y() + p.get_height() / 2, f"{int(width)}", va="center")

    plt.savefig("./top_common_words.png")
    plt.show()


def get_sentiment(text: str) -> float:
    """
    Purpose:
        Analyses text and returns a sentiment polarity.
    Args:
        text: Text to perform analysis on.
    Returns:
        Float for sentiment polarity.
    """
    # Some notes are null.
    if not text:
        return 0.0

    # Returns a score between -1 and 1 as a "sentiment polarity".
    return TextBlob(text).sentiment.polarity


def sentiment_vs_score(data: pd.DataFrame) -> NoReturn:
    """
    Purpose:
        Plot that shows sentiment analysis of daily note vs. score for notes.
        This shows how on good days, the sentiment analysis is usually good,
        while usually poor on bad days.
    Args:
        data: Polars Dataframe with Pixels data.
    """
    data_notes_only = data.dropna(subset=["notes"])
    data_notes_only["sentiment"] = data_notes_only["notes"].apply(get_sentiment)

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="sentiment", y="average_score", data=data_notes_only)
    plt.title("Sentiment vs. Score")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Score")

    plt.savefig("./sentiment_vs_score.png")
    plt.show()


def top_bigrams(data: pd.DataFrame, language: str) -> NoReturn:
    """
    Purpose:
        Shows most common biagrams in notes.
    Args:
        data: Pandas DataFrame of pixels data.
        language: Language used in notes for matching words.
    """
    data["cleaned_notes"] = data["notes"].apply(preprocess_text)

    # Bigram analysis.
    vectorizer = CountVectorizer(stop_words=language, ngram_range=(2, 2))
    bigram_count = vectorizer.fit_transform(data["cleaned_notes"])
    bigram_counts = pd.DataFrame(
        bigram_count.toarray(),
        columns=vectorizer.get_feature_names_out(),
    )
    total_bigram_counts = bigram_counts.sum().sort_values(ascending=False)

    # Convert to DataFrame for visualization.
    bigram_counts_df = pd.DataFrame(total_bigram_counts).reset_index()
    bigram_counts_df.columns = ["bigram", "count"]

    # Visualize top bigrams.
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(
        x="count",
        y="bigram",
        data=bigram_counts_df.head(TOP_N),
        palette="viridis",
        hue="bigram",
    )
    plt.title(f"Top {TOP_N} Most Common Bigrams in Journal Entries")
    plt.xlabel("Frequency")
    plt.ylabel("Bigrams")

    for p in ax.patches:
        width = p.get_width()
        ax.text(width + 0.5, p.get_y() + p.get_height() / 2, f"{int(width)}", va="center")

    plt.savefig("./plots/top_bigrams.png")
    plt.show()


def plot_all_graphs(data: pd.DataFrame) -> NoReturn:
    """
    Purpose:
        Driver to plot all graphs after converting to Polars to Pandas.
    """
    # heatmap_of_nulls(data)
    # interactive_line_plot(data)
    # interactive_seasonal_plot(data)
    # interactive_rolling_statistics_plot(data)
    # box_plot(data)
    # verbosity_plots(data)
    # top_common_words(data, LANGUAGE)
    # sentiment_vs_score(data)
    # top_bigrams(data, LANGUAGE)
