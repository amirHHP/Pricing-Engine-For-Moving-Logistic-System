import math
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class MoveRequest:
    """Data Transfer Object for Move Request parameters."""
    distance_km: float
    num_workers: int
    total_floors: int  # Sum of origin and destination floors
    num_heavy_items: int
    walking_distance_m: float

class LogisticPricingModel:
    """
    A variable pricing engine that optimizes for driver acceptance 
    based on job complexity and operational costs.
    """
    
    def __init__(self, base_rate: float = 50.0):
        self.base_rate = base_rate
        # Weights (Betas) derived from historical data or heuristic analysis
        self.weights = {
            'distance_coeff': 2.5,   # Cost per km
            'worker_coeff': 30.0,    # Cost per worker
            'floor_coeff': 10.0,     # Cost per floor level
            'heavy_item_coeff': 15.0,# Cost per heavy item
            'walk_coeff': 0.5        # Cost per meter of walking
        }
        # Logistic parameters for Driver Acceptance Probability
        self.acceptance_steepness = 0.15  # 'k' in sigmoid function
        self.acceptance_midpoint = 20.0   # The margin ($) where acceptance is 50%

    def calculate_operational_cost(self, req: MoveRequest) -> float:
        """Calculates the raw operational complexity cost (linear regression model)."""
        cost = self.base_rate
        cost += req.distance_km * self.weights['distance_coeff']
        cost += req.num_workers * self.weights['worker_coeff']
        cost += req.total_floors * self.weights['floor_coeff']
        cost += req.num_heavy_items * self.weights['heavy_item_coeff']
        cost += req.walking_distance_m * self.weights['walk_coeff']
        return round(cost, 2)

    def estimate_acceptance_probability(self, margin: float) -> float:
        """
        Models driver acceptance using a Sigmoid function.
        As margin (profit for driver) increases, probability of acceptance approaches 1.
        """
        # Sigmoid function: 1 / (1 + e^-k(x - x0))
        try:
            prob = 1 / (1 + math.exp(-self.acceptance_steepness * (margin - self.acceptance_midpoint)))
            return prob
        except OverflowError:
            return 0.0 if margin < self.acceptance_midpoint else 1.0

    def optimize_price_for_target_acceptance(self, req: MoveRequest, target_prob: float = 0.85) -> dict:
        """
        Reverse solves the logistic function to find the required price 
        to achieve a specific driver acceptance rate (e.g., 85%).
        """
        base_cost = self.calculate_operational_cost(req)
        
        # Inverse Sigmoid (Logit) to find required margin for target probability
        # margin = M0 - (1/k) * ln(1/P - 1)
        if target_prob <= 0 or target_prob >= 1:
            raise ValueError("Target probability must be between 0 and 1 (exclusive).")
            
        required_margin = self.acceptance_midpoint - (1 / self.acceptance_steepness) * math.log((1 / target_prob) - 1)
        final_price = base_cost + required_margin

        return {
            "operational_cost": base_cost,
            "required_margin": round(required_margin, 2),
            "final_price": round(final_price, 2),
            "target_acceptance_rate": f"{target_prob*100}%"
        }

# --- Example Usage ---
if __name__ == "__main__":
    # Simulate a difficult move
    request = MoveRequest(
        distance_km=15.5,
        num_workers=3,
        total_floors=4,      # e.g., 2 floors origin, 2 destination
        num_heavy_items=2,   # Piano, Safe
        walking_distance_m=150
    )

    model = LogisticPricingModel()
    
    # Calculate Optimal Price for 90% Driver Acceptance
    result = model.optimize_price_for_target_acceptance(request, target_prob=0.90)
    
    print(f"--- Optimization Result ---")
    print(f"Base Operational Cost: ${result['operational_cost']}")
    print(f"Dynamic Margin Needed: ${result['required_margin']}")
    print(f"Recommended Price:     ${result['final_price']}")