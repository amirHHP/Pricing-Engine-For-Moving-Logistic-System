# Logistics Optimization Engine: Dynamic Pricing & Heuristic Dispatch

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange.svg)]()

## 1. Executive Summary

This repository hosts an algorithmic framework for solving the **Real-Time Logistics Assignment Problem (RTLAP)** in residential moving services. 

Unlike traditional "nearest-neighbor" systems, this engine prioritizes **Service Quality (CSAT)** over pure distance, while solving the supply-side acceptance problem using a **Probabilistic Pricing Model**. The system aims to minimize the "Time to Acceptance" ($t_{acc}$) while maximizing the probability of high-quality driver matches.

### Key Innovations
1.  **Logistic Acceptance Probability:** Modeling driver behavior using a Sigmoid function to optimize price points.
2.  **Cold-Start Injection:** A heuristic boost for new supply nodes (drivers) to ensure ecosystem retention.
3.  **Cascading Dispatch:** A batch-processing logic to reduce network race conditions and optimize matching.
4.  **Feedback Surge Loop:** A dynamic bridge where operational failures (no acceptance) trigger financial adjustments (surge pricing).

---

## 2. Mathematical Formulation

### 2.1. The Cost & Complexity Model
The base operational cost ($C_{op}$) is calculated as a vector of physical constraints, vehicle specifications, and environmental factors.

$$
C_{op} = (M_{veh} \cdot M_{env}) \times [\beta_0 + (\beta_d \cdot d) + (\beta_w \cdot w) + (\beta_f \cdot \Delta f) + (\beta_h \cdot h)]
$$

| Parameter | Symbol | Description |
| :--- | :---: | :--- |
| **Vehicle Multiplier** | $M_{veh}$ | 1.0 (Mini), 1.5 (Van), 2.2 (Truck) |
| **Weather Multiplier** | $M_{env}$ | 1.4 if `bad_weather` else 1.0 |
| **Distance** | $d$ | Euclidean distance between origin and destination |
| **Labor** | $w$ | Number of workers required |
| **Verticality** | $\Delta f$ | Sum of floors (Origin + Destination) |

### 2.2. The Driver Acceptance Model (Sigmoid)
We treat driver acceptance as a stochastic process dependent on the Profit Margin ($M$). The probability $P(A)$ follows a logistic curve:

$$
P(A | M) = \frac{1}{1 + e^{-k(M - M_0)}}
$$

* $M_0$: The inflection point where acceptance probability is 50%.
* $k$: The steepness coefficient (sensitivity of drivers to price changes).

### 2.3. The Dispatch Scoring Heuristic
To assign the "Best" driver rather than just the "Closest," we utilize a weighted scoring function ($S$) for every available driver $d_i$:

$$
S_{d_i} = (w_q \cdot \frac{R_i}{R_{max}}) + (w_p \cdot \frac{1}{1+D_i}) + \delta_{cold\_start}
$$

* **Quality Weight ($w_q$):** Set to `0.7` to prioritize high ratings.
* **Proximity Weight ($w_p$):** Set to `0.3`.
* **Cold Start Boost ($\delta$):** A scalar bonus applied if `days_in_system < 7` to incentivize new driver engagement.

---

## 3. Algorithmic Architecture

The system operates in a feedback loop between the **Dispatch Engine** and the **Pricing Engine**.

### The Cascading Batch Strategy (Time-Decay Surge)
To avoid "spamming" all drivers and creating race conditions, the dispatch algorithm uses a temporal cascade. If a batch expires without acceptance, the system escalates the price.

1.  **Iteration 1 ($T=0s$):**
    * **Target:** Top 10 Ranked Drivers (High Quality).
    * **Price:** Standard $P(A) \approx 0.85$.
2.  **Iteration 2 ($T=10s$):**
    * **Target:** Next 10 Ranked Drivers.
    * **Price:** **Surge 1.15x** (To compensate for lower quality match).
3.  **Iteration 3 ($T=20s$):**
    * **Target:** Broadcast to All (Panic Mode).
    * **Price:** **Surge 1.32x** (Maximize acceptance chance immediately).

---

## 4. Repository Structure

```bash
├── dispatch_engine.py   # Driver Ranking, Cold-Start Logic, and Batch Clustering
├── pricing_engine.py    # Logistic Regression Model, Weather/Vehicle Logic
├── visualize_model.py   # Script to generate P(A) vs Margin curves (Matplotlib)
├── simulation.py        # Main Controller: Runs the Batch/Surge Loop
├── README.md            # Documentation
└── requirements.txt     # Dependencies (numpy, matplotlib)