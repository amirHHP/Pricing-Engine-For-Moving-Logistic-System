from dataclasses import dataclass
from typing import List, Tuple
import math

@dataclass
class Driver:
    id: str
    name: str
    rating: float       # 0.0 to 5.0
    location_km: float  # Distance from Origin
    days_in_system: int # To identify "New" drivers
    is_busy: bool = False

class DispatchEngine:
    def __init__(self):
        # Weights for the Ranking Function (Quality > Proximity)
        self.w_quality = 0.7
        self.w_proximity = 0.3
        self.new_driver_bonus = 0.5 # Flat bonus to score for "Cold Start"

    def _calculate_score(self, driver: Driver) -> float:
        """
        Heuristic Scoring Function:
        Score = (w1 * Normalized_Rating) + (w2 * Normalized_Proximity) + Boost
        """
        # Normalize Rating (0-5 -> 0-1)
        norm_rating = driver.rating / 5.0
        
        # Normalize Proximity (Closer is better). 
        # Using 1 / (1 + distance) to prevent division by zero and invert value.
        norm_prox = 1 / (1 + driver.location_km)

        score = (self.w_quality * norm_rating) + (self.w_proximity * norm_prox)

        # Cold Start Logic: If new (< 7 days), give artificial boost
        if driver.days_in_system < 7:
            score += self.new_driver_bonus

        return score

    def rank_drivers(self, all_drivers: List[Driver]) -> List[Driver]:
        """
        Filters busy drivers and sorts available ones by Algorithm Score.
        """
        available = [d for d in all_drivers if not d.is_busy]
        # Sort descending (Higher score is better)
        return sorted(available, key=self._calculate_score, reverse=True)

    def create_batches(self, ranked_drivers: List[Driver]) -> List[List[Driver]]:
        """
        Implements the 'Cascading Dispatch' strategy.
        Batch 1: Top 10
        Batch 2: Next 10
        Batch 3: Everyone Remaining (Panic Mode)
        """
        batch_size = 10
        batches = []

        # Batch 1
        batches.append(ranked_drivers[:batch_size])
        
        # Batch 2
        if len(ranked_drivers) > batch_size:
            batches.append(ranked_drivers[batch_size : batch_size*2])
        
        # Batch 3 (All remaining)
        if len(ranked_drivers) > batch_size*2:
            batches.append(ranked_drivers[batch_size*2:])
            
        return batches