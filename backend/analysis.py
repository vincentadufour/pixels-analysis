"""Description: Module of analysis methods."""

import textwrap
from typing import NoReturn

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Formatting.
headline1 = "\n----------|"
headline2 = "|----------\n"
headline3 = "|---|"


def compare_average_score_with_term(data: pd.DataFrame, term: str, print_note: str = 0) -> NoReturn:
    """
    Purpose:
        Uses a search term to show a plot with average score for days that include
        word in notes against average score.
    Args:
        data: Pandas Dataframe of Pixel data.
        term: Search term.
        print_note: How many notes that include search term to print.
    """
    # Boolean column if term is in note.
    data["contains_term"] = data["notes"].str.contains(term, case=False)

    # Get average score for days with term and without term.
    avg_score_for_term = data.groupby("contains_term")["average_score"].mean().reset_index()
    avg_score_for_term["contains_term"] = avg_score_for_term["contains_term"].map({
        True: f'Contains "{term}"',
        False: f'Does Not Contain "{term}"',
    })

    # Sum of term.
    term_sum = data["contains_term"].sum()

    # Bar plot.
    plt.figure(figsize=(10, 6))
    fig = sns.barplot(
        data=avg_score_for_term,
        x="contains_term",
        y="average_score",
        hue="contains_term",
        palette="tab10",
        legend=False,
    )

    # Overall average score line for dataset.
    overall_avg = avg_score_for_term["average_score"].mean()
    plt.axhline(y=overall_avg, color="gray", linestyle="--", label="Overall Average Score")

    # Average score markers on score bars.
    for index, row in avg_score_for_term.iterrows():
        fig.text(index, row["average_score"] + 0.05, f"{row['average_score']:.2f}", ha="center")

    # Add counts to legend.
    not_term_count = len(data) - term_sum
    counts = [f'Count of "{term}": {term_sum}', f'Count of non-"{term}": {not_term_count}']
    plt.legend(counts, loc="upper left")

    plt.title(f'Average Score for Days with and without "{term}" in Notes')
    plt.ylabel("Score")
    plt.xlabel("")
    plt.ylim(0, 5.5)

    plt.savefig("./plots/analysis.png")
    plt.show()

    # Iterates through and prints notes including search term.
    if print_note:
        count = 0
        how_many_prints = 0

        for _i, row in data.iterrows():
            if count == print_note:
                break

            if row["contains_term"]:
                wrapped_note = textwrap.fill(row["notes"])
                print(
                    f"{headline1} Date: {row['date'].strftime('%Y-%m-%d')}"
                    f"{headline3} Score: {row['average_score']} {headline2}{wrapped_note}",
                )

                # Counts how many successful prints occurred.
                how_many_prints += 1

                # Checks to see if all notes were requested.
                if count != "all":
                    count += 1

            else:
                continue

        print("\nHow many prints?:", how_many_prints)
