import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def calculate_weighted_score(soft_tags, NPS, distance, w1, w2, w3):
    """
    Calculate the weighted score based on the given parameters.

    Parameters:
    soft_tags (float): The soft tags value.
    NPS (float): The NPS value.
    distance (float): The distance value.
    w1 (float): The weight for soft tags.
    w2 (float): The weight for NPS.
    w3 (float): The weight for distance.

    Returns:
    float: The calculated weighted score.
    """
    if all(value == 0 for value in [soft_tags, NPS, distance]) or all(
        weight == 0 for weight in [w1, w2, w3]
    ):
        return 0  # If all values are zero or all weights are zero, return zero directly
    weighted_score = (soft_tags * w1) + (NPS * w2) + (distance * w3)

    # Assuming raw weighted score could be any real number
    min_raw_score = 0
    max_raw_score = 100

    mapped_score = (
        (weighted_score - min_raw_score) / (max_raw_score - min_raw_score)
    ) * 100

    return round(mapped_score, 2)


def plot_weighted_score(soft_tags, NPS, distance, w1, w2, w3):
    """
    Plots the weighted score based on the input data and weights.

    Parameters:
    soft_tags (float): Number of Soft Tags to exclude.
    NPS (float): NPS (Net Promoter Score).
    distance (float): Distance in kilometers.
    w1 (float): Weight 1.
    w2 (float): Weight 2.
    w3 (float): Weight 3.

    Returns:
    None
    """
    result = calculate_weighted_score(soft_tags, NPS, distance, w1, w2, w3)

    # Create a Matplotlib figure
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    # Plot the data as a bar plot side by side
    bar_width = 0.3
    ax1.bar(
        0, soft_tags, bar_width, label="Number of Soft Tags to exclude", color="orange"
    )
    ax1.bar(bar_width, NPS, bar_width, label="NPS", color="magenta")
    ax1.bar(2 * bar_width, distance, bar_width, label="Distance (km)", color="cyan")
    ax1.set_xlabel("Input data")
    ax1.set_ylabel("Value")
    ax1.legend()

    # Plot the weights
    ax2.bar(0, w1, bar_width, label="Weight 1", color="orange")
    ax2.bar(bar_width, w2, bar_width, label="Weight 2", color="magenta")
    ax2.bar(2 * bar_width, w3, bar_width, label="Weight 3", color="cyan")
    ax2.set_xlabel("Input data")
    ax2.set_ylabel("Weight")
    ax2.legend()

    # Plot the weighted score with color
    color = "green" if result > 0 else ("red" if result < 0 else "gray")
    ax3.bar(0, result, color=color)
    ax3.set_xlabel("Score")
    ax3.set_ylabel("Weighted Score")
    ax3.set_ylim(-100, 100)
    ax3.set_xticks([0])
    ax3.legend(["Weighted Score"])  # Add legend label

    # Display the plot using Streamlit's `st.pyplot()` function
    st.pyplot(fig)


def main():
    """
    Main function that calculates and displays the weighted score.

    This function takes user input for values and weights, calculates the weighted score using the
    `calculate_weighted_score` function, and displays the result along with a plot using the
    `plot_weighted_score` function.
    """
    st.title("Weighted Score Calculator")
    # Move sliders to the sidebar
    with st.sidebar:
        # Get user input for values and weights
        soft_tags = st.slider(
            "Number of Soft Tags to Exclude Value",
            min_value=0,
            max_value=6,
            value=0,
            step=1,
        )
        NPS = st.slider("NPS Value", min_value=0, max_value=100, value=0, step=5)
        distance = st.slider(
            "Distance (km)", min_value=0, max_value=30, value=0, step=5
        )
        weight_soft_tags = st.slider(
            "Weight for Soft Tags", min_value=-1.0, max_value=1.0, value=0.0, step=0.1
        )
        weight_NPS = st.slider(
            "Weight for NPS", min_value=-1.0, max_value=1.0, value=0.0, step=0.1
        )
        weight_distance = st.slider(
            "Weight for Distance", min_value=-1.0, max_value=1.0, value=0.0, step=0.1
        )

    # Calculate the weighted score
    result = calculate_weighted_score(
        soft_tags, NPS, distance, weight_soft_tags, weight_NPS, weight_distance
    )

    # Display the weighted score
    st.text("Weighted Score: {}".format(result))

    # Generate and display the plot
    plot_weighted_score(
        soft_tags, NPS, distance, weight_soft_tags, weight_NPS, weight_distance
    )


if __name__ == "__main__":
    main()
