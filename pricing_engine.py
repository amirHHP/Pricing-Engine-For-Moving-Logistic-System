from enum import Enum
from dataclasses import dataclass

class VehicleType(Enum):
    MINI_TRUCK = 1.0  # Base multiplier
    VAN = 1.5
    TRUCK = 2.2

@dataclass
class MoveRequest:
    distance_km: float
    vehicle_type: VehicleType
    is_bad_weather: bool = False
    # ... other fields from previous code ...

class PricingEngine:
    def __init__(self):
        self.base_rates = {
            VehicleType.MINI_TRUCK: 30.0,
            VehicleType.VAN: 50.0,
            VehicleType.TRUCK: 90.0
        }
        self.weather_multiplier = 1.4  # 40% increase for bad weather

    def calculate_price(self, req: MoveRequest, attempt_number: int = 1) -> float:
        """
        Calculates price based on vehicle, weather, and iteration attempt.
        """
        # 1. Base Price by Vehicle
        price = self.base_rates[req.vehicle_type] + (req.distance_km * 2.0)
        
        # 2. Weather Penalty
        if req.is_bad_weather:
            price *= self.weather_multiplier

        # 3. Dynamic Repricing (Increase price by 15% for every failed batch)
        # Attempt 1 = 1.0x, Attempt 2 = 1.15x, Attempt 3 = 1.32x
        surge_factor = 1.15 ** (attempt_number - 1)
        
        return round(price * surge_factor, 2)