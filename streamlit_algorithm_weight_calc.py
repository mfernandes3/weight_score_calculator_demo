import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


def calculate_weighted_score(soft_tags, NPS, distance, w1, w2, w3):
    if all(value == 0 for value in [soft_tags, NPS, distance]) or all(weight == 0 for weight in [w1, w2, w3]):
        return 0  # If all values are zero or all weights are zero, return zero directly
    weighted_score = (soft_tags * w1) + (NPS * w2) + (distance * w3)

    # Assuming raw weighted score could be any real number
    min_raw_score = 0
    max_raw_score = 1000

    mapped_score = ((weighted_score - min_raw_score) / (max_raw_score - min_raw_score)) * 1000

    return round(mapped_score, 2)


def plot_weighted_score(soft_tags_values, NPS_values, distance_values, w1, w2, w3):
    scores = []
    colors = []  # List to store the colors of the bars
    for soft_tags, NPS, distance in zip(soft_tags_values, NPS_values, distance_values):
        result = calculate_weighted_score(soft_tags, NPS, distance, w1, w2, w3)
        scores.append(result)
        if result > 0:
            colors.append("green")  # Positive score, set color to green
        elif result < 0:
            colors.append("red")  # Negative score, set color to red
        else:
            colors.append("gray")  # Zero score, set color to gray

    # Create a Matplotlib figure
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

    # Plot the data as a bar plot side by side
    bar_width = 0.3
    index = np.arange(len(soft_tags_values))
    ax1.bar(index, soft_tags_values, bar_width, label="Soft Tags to exclude", color="orange")
    ax1.bar(index + bar_width, NPS_values, bar_width, label="NPS", color="magenta")
    ax1.bar(index + 2 * bar_width, distance_values, bar_width, label="Distance", color="cyan")
    ax1.set_xlabel("Input data")
    ax1.set_ylabel("Value")
    ax1.legend()

    # Plot the weights
    ax2.bar(index, [w1], bar_width, label="Weight 1", color="orange")
    ax2.bar(index + bar_width, [w2], bar_width, label="Weight 2", color="magenta")
    ax2.bar(index + 2 * bar_width, [w3], bar_width, label="Weight 3", color="cyan")
    ax2.set_xlabel("Input data")
    ax2.set_ylabel("Weight")
    ax2.legend()

    # Plot the weighted scores with colors
    ax3.bar(range(len(scores)), scores, color=colors)
    ax3.set_xlabel("Score")
    ax3.set_ylabel("Weighted Score")
    ax3.set_ylim(-100, 100)
    ax3.set_xticks(range(len(scores)))
    ax3.legend(["Weighted Score"])  # Add legend label

    # Display the plot using Streamlit's `st.pyplot()` function
    st.pyplot(fig)


def main():
    st.title("Weighted Score Calculator")
        # Move sliders to the sidebar
    with st.sidebar:
        # Get user input for values and weights
        soft_tags_values = st.slider("Soft Tags to Exclude Value", min_value=0, max_value=10, value=[0])
        NPS_values = st.slider("NPS Value", min_value=0, max_value=10, value=[0])
        distance_values = st.slider("Distance Value", min_value=0, max_value=30, value=[0])
        weight_soft_tags = st.slider("Weight for Soft Tags", min_value=-10, max_value=10, value=0)
        weight_NPS = st.slider("Weight for NPS", min_value=-10, max_value=10, value=0)
        weight_distance = st.slider("Weight for Distance", min_value=-10, max_value=10, value=0)

        # Calculate the weighted score
        result = calculate_weighted_score(
            soft_tags_values[0], NPS_values[0], distance_values[0], weight_soft_tags, weight_NPS, weight_distance
        )

    # Display the weighted score
    st.text("Weighted Score: {}".format(result))

    # Generate and display the plot
    plot_weighted_score(soft_tags_values, NPS_values, distance_values, weight_soft_tags, weight_NPS, weight_distance)


if __name__ == "__main__":
    main()
