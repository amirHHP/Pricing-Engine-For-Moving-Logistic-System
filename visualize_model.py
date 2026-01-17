import matplotlib.pyplot as plt
import numpy as np
# Import the model class from your main script (assuming it's named pricing_engine.py)
from pricing_engine import LogisticPricingModel

def generate_acceptance_curve_plot(filename="acceptance_curve.png"):
    """
    Generates a visual representation of the Sigmoid Driver Acceptance function.
    """
    model = LogisticPricingModel()

    # 1. Generate Data based on model parameters
    # Create a range of potential margins from -$10 to $60
    margins_x = np.linspace(-10, 60, 300)
    
    # Calculate probability for each margin point using the model's sigmoid function
    probabilities_y = [model.estimate_acceptance_probability(m) for m in margins_x]

    # 2. Create the Plot
    plt.figure(figsize=(10, 6))
    plt.plot(margins_x, probabilities_y, label='Acceptance Probability Function (Sigmoid)', color='#2c3e50', linewidth=2.5)

    # 3. Annotate Key Optimization Points
    # Point A: The midpoint (defined in the model as $20 margin = 50% acceptance)
    midpoint_margin = model.acceptance_midpoint
    midpoint_prob = 0.5
    plt.scatter([midpoint_margin], [midpoint_prob], color='red', zorder=5)
    plt.annotate(f'Midpoint ($20, 50%)', xy=(midpoint_margin, midpoint_prob), xytext=(midpoint_margin+5, midpoint_prob-0.1),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=8))

    # Point B: A target optimization point (e.g., requiring 90% acceptance)
    # We calculate exactly what margin gives 90%
    target_prob = 0.90
    # Inverse logit formula derived from model: M0 - (1/k) * ln(1/P - 1)
    target_margin = model.acceptance_midpoint - (1 / model.acceptance_steepness) * np.log((1 / target_prob) - 1)
    
    plt.scatter([target_margin], [target_prob], color='green', zorder=5)
    # Draw dotted lines showing the optimization path
    plt.hlines(y=target_prob, xmin=-10, xmax=target_margin, colors='green', linestyles='dotted', alpha=0.6)
    plt.vlines(x=target_margin, ymin=0, ymax=target_prob, colors='green', linestyles='dotted', alpha=0.6)
    plt.annotate(f'Target SLA (90%)\nRequires ~${target_margin:.2f} Margin', 
                 xy=(target_margin, target_prob), xytext=(target_margin-25, target_prob-0.15),
                 arrowprops=dict(facecolor='green', shrink=0.05, width=1, headwidth=8), color='green')


    # 4. Styling the Graph for Academic Presentation
    plt.title("Driver Acceptance Dynamics vs. Incentivization Margin", fontsize=14, pad=20)
    plt.xlabel("Offered Margin ($ Profit above Operational Cost)", fontsize=12)
    plt.ylabel("Probability of Driver Acceptance P(A)", fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xlim(-10, 60)
    plt.ylim(-0.05, 1.05)
    
    # Add a shaded region indicating high-probability zone
    plt.fill_between(margins_x, probabilities_y, 0, where=(probabilities_y >= 0.8), color='green', alpha=0.1, label="High Acceptance Zone (>80%)")
    
    plt.legend(loc='lower right')
    plt.tight_layout()

    # 5. Save the image
    plt.savefig(filename, dpi=300)
    print(f"Graph successfully generated and saved to {filename}")

if __name__ == "__main__":
    generate_acceptance_curve_plot()
