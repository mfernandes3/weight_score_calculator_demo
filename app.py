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


def calculate_weighted_score(jameda, NPS, google, w1, w2, w3, jameda_premium=False):
    """Calculate the weighted score based on the given parameters."""
    # Adjust Jameda weight if premium account (reduce influence)
    if jameda_premium:
        w1 *= 0.7  # Reduce Jameda influence by 30% for premium accounts

    # Normalize inputs considering their different scales and meanings
    norm_jameda = normalize_input(jameda, 0, 5)  # Higher is better (1-5 scale)
    norm_nps = normalize_input(NPS, -100, 100)  # Higher is better
    norm_google = normalize_input(google, 0, 5)  # Higher is better (1-5 scale)

    # Apply scale factors to account for different importance levels
    jameda_factor = 1.0  # Base factor
    nps_factor = 0.7  # Slightly less impact as it's more volatile
    google_factor = 1.0  # Equal importance to Jameda

    # Check for zero weights
    total_weight = abs(w1) + abs(w2) + abs(w3)
    if total_weight == 0:
        return 0

    # Calculate normalized weighted score with scale factors
    weighted_score = (
        (norm_jameda * w1 * jameda_factor)
        + (norm_nps * w2 * nps_factor)
        + (norm_google * w3 * google_factor)
    ) / total_weight

    # Map to 0 to 100 range (changed from -100 to 100 for better interpretation)
    mapped_score = weighted_score * 100

    return round(mapped_score, 2)


def plot_weighted_score(jameda, NPS, google, w1, w2, w3):
    """Plots the weighted score based on the input data and weights."""
    result = calculate_weighted_score(jameda, NPS, google, w1, w2, w3)

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
    labels = ["Jameda", "NPS", "Google"]
    values = [jameda, NPS, google]
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
    labels = ["Jameda\nWeight", "NPS\nWeight", "Google\nWeight"]
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

    # Plot 3: Final Score
    color = "#2ECC71" if result > 0 else ("#E74C3C" if result < 0 else "#95A5A6")
    ax3.bar(["Final Score"], [result], bar_width * 1.5, color=color)
    ax3.set_title("Weighted Score", pad=20, fontsize=14, fontweight="bold")
    ax3.set_ylabel("Score (0 to 100)", fontsize=12)

    # Adjust y-axis limits to accommodate negative scores
    ax3.set_ylim(-110, 110)  # Adjusted to show negative values properly

    # Add horizontal lines for better readability
    ax3.axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    for y in [25, 75]:
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


def calculate_trust_level(jameda_count, nps_count, google_count):
    """
    Calculate trust level based on number of ratings for each source
    """
    # Calculate individual trust scores (0-1)
    total_sources = 0
    trust_sum = 0

    if jameda_count > 0:
        trust_sum += (jameda_count / 10) * 0.3  # Normalize by expecting 10 reviews
        total_sources += 1

    if nps_count > 0:
        trust_sum += (nps_count / 20) * 0.4  # Normalize by expecting 20 responses
        total_sources += 1

    if google_count > 0:
        trust_sum += (google_count / 10) * 0.3  # Normalize by expecting 10 reviews
        total_sources += 1

    # Calculate average trust score, handling case where no sources exist
    trust_score = trust_sum / total_sources if total_sources > 0 else 0

    # Convert to trust level
    if trust_score >= 0.5:
        return "High", trust_score
    elif trust_score >= 0.2:
        return "Medium", trust_score
    else:
        return "Low", trust_score


def main():
    """
    Main function that calculates and displays the weighted score.

    This function takes user input for values and weights, calculates the weighted score using the
    `calculate_weighted_score` function, and displays the result along with a plot using the
    `plot_weighted_score` function.
    """
    st.title("BD-Physician Niceness Index Calculator")

    # Update explanation
    st.markdown("""
    This calculator generates the BD-Physician Niceness Index based on:
    - **Internal Data**: NPS (Net Promoter Score)
    - **External Data**: Jameda and Google Ratings

    """)

    with st.sidebar:
        st.header("Input Parameters")

        # Add premium account toggle
        jameda_premium = st.checkbox(
            "Jameda Premium Account",
            help="Check if the physician has a premium Jameda account",
        )

        # Rating counts (number of reviews)
        st.subheader("Number of Ratings")
        jameda_count = st.number_input("Number of Jameda Reviews", min_value=0, value=4)
        nps_count = st.number_input("Number of NPS Responses", min_value=0, value=30)
        google_count = st.number_input("Number of Google Reviews", min_value=0, value=3)

        # Rating values (actual scores)
        st.subheader("Rating Values")
        jameda = st.slider(
            "Jameda Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.1
        )
        NPS = st.slider("NPS Value", min_value=-100, max_value=100, value=70, step=5)
        google = st.slider(
            "Google Rating", min_value=1.0, max_value=5.0, value=4.0, step=0.1
        )

        # Add explanation about scaling
        st.markdown("""
        ### How the scoring works:
        - **Jameda**: Higher is better (1 to 5)
        - **NPS**: Higher is better (-100 to 100)
        - **Google**: Higher is better (1 to 5)
        
        """)

        # Add help text for weights
        st.info("""
        Weights (-1 to 1) determine each factor's influence:
        """)

        # Get user input for values and weights with defaults
        weight_jameda = st.slider(
            "Weight for Jameda", min_value=-1.0, max_value=1.0, value=0.3, step=0.1
        )
        weight_NPS = st.slider(
            "Weight for NPS", min_value=-1.0, max_value=1.0, value=0.4, step=0.1
        )
        weight_google = st.slider(
            "Weight for Google", min_value=-1.0, max_value=1.0, value=0.3, step=0.1
        )

        # Add weight validation
        total_weight = abs(weight_jameda) + abs(weight_NPS) + abs(weight_google)
        if total_weight == 0:
            st.warning("⚠️ All weights are set to 0. The score will be 0.")

    # Calculate the weighted score
    result = calculate_weighted_score(
        jameda, NPS, google, weight_jameda, weight_NPS, weight_google, jameda_premium
    )

    # Calculate and display trust level
    trust_level, trust_score = calculate_trust_level(
        jameda_count, nps_count, google_count
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Trust Level")
        st.text(f"Trust Level: {trust_level} ({trust_score:.2f})")
        st.text("Based on:")
        st.text(f"• Jameda: {jameda_count} reviews")
        st.text(f"• NPS: {nps_count} responses")
        st.text(f"• Google: {google_count} reviews")

    with col2:
        # Display the weighted score
        st.subheader("Score")
        st.text("Weighted Score: {}".format(result))

    # Generate and display the plot
    plot_weighted_score(jameda, NPS, google, weight_jameda, weight_NPS, weight_google)

    # Add score interpretation
    st.subheader("Score Interpretation")
    col1, col2 = st.columns(2)

    with col1:
        if result > 0:
            st.success(f"Positive score ({result}): Good match")
        elif result < 0:
            st.error(f"Negative score ({result}): Not a good match")
        else:
            st.info("Neutral score (0): Unclear")

    with col2:
        if trust_level == "High":
            st.success(f"Trust Level: {trust_level} ({trust_score:.2f})")
        elif trust_level == "Low":
            st.error(f"Trust Level: {trust_level} ({trust_score:.2f})")
        else:
            st.warning(f"Trust Level: {trust_level} ({trust_score:.2f})")


if __name__ == "__main__":
    main()
