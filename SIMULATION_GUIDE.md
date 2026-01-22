# Simulation Guide

This guide shows you how to run different simulation scenarios to test various logistics pricing situations.

## Quick Start

### Run with Default Settings
```bash
python simulation.py
```

### Run Predefined Scenarios

1. **Short Trip** - Small vehicle, short distance, good weather
   ```bash
   python simulation.py --scenario short_trip
   ```

2. **Long Trip** - Large truck, long distance
   ```bash
   python simulation.py --scenario long_trip
   ```

3. **Bad Weather** - Weather multiplier applied
   ```bash
   python simulation.py --scenario bad_weather
   ```

4. **Few Options** - Limited driver availability
   ```bash
   python simulation.py --scenario few_options
   ```

5. **New Drivers** - Testing cold-start boost for new drivers
   ```bash
   python simulation.py --scenario new_drivers
   ```

6. **Busy Market** - Some drivers are busy/unavailable
   ```bash
   python simulation.py --scenario busy_market
   ```

## Custom Parameters

### Custom Order Parameters

**Example 1: Custom distance and vehicle**
```bash
python simulation.py --distance 30 --vehicle TRUCK
```

**Example 2: Add weather conditions**
```bash
python simulation.py --distance 20 --vehicle VAN --weather
```

**Example 3: Combine with driver pool**
```bash
python simulation.py --distance 25 --vehicle TRUCK --weather --driver-pool many_drivers
```

### Available Options

- **Distance**: `--distance <number>` (in km)
- **Vehicle**: `--vehicle {MINI_TRUCK, VAN, TRUCK}`
- **Weather**: `--weather` (flag for bad weather)
- **Driver Pool**: `--driver-pool {default, many_drivers, few_drivers, new_drivers, busy_drivers}`

## Programmatic Usage

You can also use the simulation functions directly in Python:

```python
from simulation import run_simulation, create_driver_pool
from pricing_engine import MoveRequest, VehicleType

# Create custom order
order = MoveRequest(
    distance_km=18.5,
    vehicle_type=VehicleType.VAN,
    is_bad_weather=True
)

# Create custom driver pool
drivers = create_driver_pool("many_drivers")
# Or create your own:
# drivers = [
#     Driver("D1", "Custom Driver", rating=4.8, location_km=3.0, days_in_system=50),
#     Driver("D2", "Another Driver", rating=4.5, location_km=5.0, days_in_system=30),
# ]

# Run simulation
run_simulation(order=order, drivers=drivers, show_details=True)
```

## Understanding the Output

The simulation shows:

1. **Order Details**: Distance, vehicle type, weather conditions
2. **Driver Pool**: All available drivers with their characteristics
3. **Ranking Phase**: How drivers are scored and ranked
4. **Batching Phase**: How drivers are grouped into batches
5. **Pricing**: Dynamic pricing with breakdown showing:
   - Base price
   - Weather multiplier (if applicable)
   - Surge factor (increases with each attempt)

## Key Concepts

- **Cold Start Boost**: New drivers (< 7 days) get a bonus score boost
- **Dynamic Pricing**: Price increases by 15% for each failed batch attempt
- **Batching Strategy**: 
  - Batch 1: Top 10 drivers
  - Batch 2: Next 10 drivers  
  - Batch 3: All remaining (panic mode)
- **Scoring**: 70% weight on driver rating, 30% on proximity

## Examples

### Test High-Demand Situation
```bash
python simulation.py --distance 50 --vehicle TRUCK --weather --driver-pool few_drivers
```

### Test New Driver Incentivization
```bash
python simulation.py --scenario new_drivers
```

### Test Multiple Batches
```bash
python simulation.py --scenario long_trip
```
