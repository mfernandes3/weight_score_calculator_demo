import matplotlib.pyplot as plt
import streamlit as st


def normalize_input(value, min_val, max_val, inverse=False):
    """
    Normalize input value to range [0,1]

    Parameters:
        inverse (bool): If True, a higher raw value results in a lower normalized value
    """
    if max_val == min_val:
        return 0
    normalized = (value - min_val) / (max_val - min_val)
    return 1 - normalized if inverse else normalized


def calculate_weighted_score(soft_tags, NPS, distance, w1, w2, w3):
    """Calculate the weighted score based on the given parameters."""
    # Normalize inputs considering their different scales and meanings
    # For soft_tags and distance, lower is better, so we use inverse normalization
    norm_soft_tags = normalize_input(soft_tags, 0, 6, inverse=True)  # Lower is better
    norm_nps = normalize_input(NPS, 0, 100)  # Higher is better
    norm_distance = normalize_input(distance, 0, 30, inverse=True)  # Lower is better

    # Apply scale factors to account for different importance levels
    # These factors can be adjusted based on business requirements
    soft_tags_factor = 1.0  # Base factor
    nps_factor = 0.7  # Slightly less impact as it's more volatile
    distance_factor = 0.5  # Less impact as it's more variable

    # Check for zero weights
    total_weight = abs(w1) + abs(w2) + abs(w3)
    if total_weight == 0:
        return 0

    # Calculate normalized weighted score with scale factors
    weighted_score = (
        (norm_soft_tags * w1 * soft_tags_factor)
        + (norm_nps * w2 * nps_factor)
        + (norm_distance * w3 * distance_factor)
    ) / total_weight

    # Map to -100 to 100 range
    mapped_score = weighted_score * 100

    return round(mapped_score, 2)


def plot_weighted_score(soft_tags, NPS, distance, w1, w2, w3):
    """Plots the weighted score based on the input data and weights."""
    result = calculate_weighted_score(soft_tags, NPS, distance, w1, w2, w3)

    # Create a larger Matplotlib figure with better spacing
    fig = plt.figure(figsize=(20, 8))
    gs = plt.GridSpec(1, 3, figure=fig, width_ratios=[1, 1, 1.2], wspace=0.3)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])

    # Define colors and style
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]  # Modern color palette
    bar_width = 0.6

    # Plot 1: Input Values
    labels = ["Soft Tags", "NPS", "Distance"]
    values = [soft_tags, NPS, distance]
    bars1 = ax1.bar(labels, values, bar_width, color=colors)
    ax1.set_title("Input Values", pad=20, fontsize=14, fontweight="bold")
    ax1.set_ylabel("Value", fontsize=12)
    ax1.grid(True, alpha=0.2, linestyle="--")

    # Add value labels on top of bars
    for bar in bars1:
        height = bar.get_height()
        ax1.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:g}",
            ha="center",
            va="bottom",
        )

    # Plot 2: Weights
    labels = ["Soft Tags\nWeight", "NPS\nWeight", "Distance\nWeight"]
    weights = [w1, w2, w3]
    bars2 = ax2.bar(labels, weights, bar_width, color=colors)
    ax2.set_title("Weights", pad=20, fontsize=14, fontweight="bold")
    ax2.set_ylabel("Weight Value", fontsize=12)
    ax2.grid(True, alpha=0.2, linestyle="--")
    ax2.set_ylim(-1.2, 1.2)  # Give some padding for the weight range

    # Add value labels on top/bottom of bars
    for bar in bars2:
        height = bar.get_height()
        position = height if height >= 0 else height
        va = "bottom" if height >= 0 else "top"
        ax2.text(
            bar.get_x() + bar.get_width() / 2.0,
            position,
            f"{height:.1f}",
            ha="center",
            va=va,
        )

    # Plot 3: Final Score with improved design
    color = "#2ECC71" if result > 0 else ("#E74C3C" if result < 0 else "#95A5A6")
    ax3.bar(["Final Score"], [result], bar_width * 1.5, color=color)
    ax3.set_title("Weighted Score", pad=20, fontsize=14, fontweight="bold")
    ax3.set_ylabel("Score (-100 to 100)", fontsize=12)

    # Add horizontal lines for better readability
    ax3.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    for y in [-50, 50]:
        ax3.axhline(y=y, color="gray", linestyle="--", alpha=0.3)

    # Set y-axis limits with padding
    ax3.set_ylim(-110, 110)
    ax3.grid(True, alpha=0.2, linestyle="--")

    # Add score value label
    ax3.text(
        0,
        result,
        f"{result:+.1f}",
        ha="center",
        va="bottom" if result >= 0 else "top",
        fontsize=14,
        fontweight="bold",
    )

    # Add a background color for better visibility
    fig.patch.set_facecolor("#F8F9FA")
    for ax in [ax1, ax2, ax3]:
        ax.set_facecolor("#FFFFFF")
        # Improve tick label size
        ax.tick_params(axis="both", which="major", labelsize=10)

    # Replace the suptitle and tight_layout with explicit spacing
    fig.subplots_adjust(top=0.85, bottom=0.15, wspace=0.3)
    fig.suptitle("Weighted Score Analysis", fontsize=16, fontweight="bold", y=0.95)

    # Remove the tight_layout call entirely

    # Display the plot using Streamlit
    st.pyplot(fig)


def main():
    """
    Main function that calculates and displays the weighted score.

    This function takes user input for values and weights, calculates the weighted score using the
    `calculate_weighted_score` function, and displays the result along with a plot using the
    `plot_weighted_score` function.
    """
    st.title("Weighted Score Calculator")

    # Add explanation
    st.markdown("""
    This calculator helps you compute a weighted score based on three parameters:
    - **Soft Tags**: Number of tags to exclude (0-6)
    - **NPS**: Net Promoter Score (0-100)
    - **Distance**: Distance in kilometers (0-30)
    
    Adjust the weights in the sidebar to control how each parameter influences the final score.
    Positive weights increase the score, negative weights decrease it.
    """)

    with st.sidebar:
        st.header("Input Parameters")

        # Add explanation about scaling
        st.markdown("""
        ### How the scoring works:
        - **Soft Tags**: Lower is better (0-6)
        - **NPS**: Higher is better (0-100)
        - **Distance**: Lower is better (0-30km)
        
        The values are automatically normalized and scaled to ensure fair comparison.
        """)

        # Add help text for weights
        st.info("""
        Weights (-1 to 1) determine each factor's influence:
        • Soft Tags: Strongest impact per unit
        • NPS: Moderate impact due to wider range
        • Distance: Lower impact due to variability
        """)

        # Get user input for values and weights with defaults
        soft_tags = st.slider(
            "Number of Soft Tags to Exclude Value",
            min_value=0,
            max_value=6,
            value=1,
            step=1,
        )
        NPS = st.slider("NPS Value", min_value=0, max_value=100, value=70, step=5)
        distance = st.slider(
            "Distance (km)", min_value=0, max_value=30, value=10, step=5
        )
        weight_soft_tags = st.slider(
            "Weight for Soft Tags", min_value=-1.0, max_value=1.0, value=-0.1, step=0.1
        )
        weight_NPS = st.slider(
            "Weight for NPS", min_value=-1.0, max_value=1.0, value=0.7, step=0.1
        )
        weight_distance = st.slider(
            "Weight for Distance", min_value=-1.0, max_value=1.0, value=-0.2, step=0.1
        )

        # Add weight validation
        total_weight = abs(weight_soft_tags) + abs(weight_NPS) + abs(weight_distance)
        if total_weight == 0:
            st.warning("⚠️ All weights are set to 0. The score will be 0.")

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

    # Add score interpretation
    st.subheader("Score Interpretation")
    if result > 0:
        st.success(f"Positive score ({result}): Good match")
    elif result < 0:
        st.error(f"Negative score ({result}): Not a good match")
    else:
        st.info("Neutral score (0): Unclear")


if __name__ == "__main__":
    main()
