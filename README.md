# Dynamic Pricing & Acceptance Optimization Algorithm

## Abstract
This repository contains a probabilistic pricing engine designed for the urban logistics sector (specifically residential moving services). The algorithm addresses the optimization problem of minimizing customer wait time by maximizing driver job acceptance rates via dynamic pricing.

## Mathematical Formulation

The core challenge is balancing the **Operational Complexity Cost ($C_{op}$)** against the **Driver Acceptance Probability ($P(A)$)**.

### 1. Complexity Modeling
We model the operational effort as a linear vector of the physical constraints:

$$C_{op} = \beta_0 + \sum_{i=1}^{n} \beta_i x_i$$

Where feature vector $x$ includes:
- Euclidean Distance ($d$)
- Labor Magnitude ($L_w$)
- Vertical Displacement (Building Levels) ($h_{lvl}$)
- Heavy Item Penalty ($p_{heavy}$)
- Last-Mile Walking Distance ($d_{walk}$)

### 2. Acceptance Probability (Sigmoid)
To ensure system reliability (minimized wait times), we treat driver acceptance as a stochastic process dependent on the incentivization margin ($M$). We utilize a logistic function to model this behavior:

$$P(A | M) = \frac{1}{1 + e^{-k(M - M_0)}}$$

This allows the system to inversely solve for the required Price ($P$) to achieve a target Service Level Agreement (SLA), such as a 95% acceptance rate within 5 minutes.

## Key Features
* **Vectorized Cost Calculation:** Scalable input parameters for varying job difficulties.
* **Inverse-Sigmoid Optimization:** Calculates the precise price point needed to achieve a target acceptance probability.
* **Parameter Weighting:** Configurable coefficients ($\beta$) to adapt to different market conditions or geographies.

## Usage

```python
from pricing_engine import LogisticPricingModel, MoveRequest

# Define the physical constraints of the job
job = MoveRequest(
    distance_km=12.0,
    num_workers=2,
    total_floors=3,
    num_heavy_items=1,
    walking_distance_m=50
)

# Initialize model
model = LogisticPricingModel()

# Solve for price ensuring 85% probability of immediate driver acceptance
quote = model.optimize_price_for_target_acceptance(job, target_prob=0.85)
