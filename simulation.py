from pricing_engine import PricingEngine, MoveRequest, VehicleType
from dispatch_engine import DispatchEngine, Driver
import time
import argparse

def create_driver_pool(scenario="default"):
    """Create different driver pools based on scenario"""
    scenarios = {
        "default": [
            Driver("D1", "Old Pro", rating=4.9, location_km=10.0, days_in_system=100),
            Driver("D2", "Newbie", rating=4.5, location_km=2.0, days_in_system=2),
            Driver("D3", "Average", rating=3.5, location_km=1.0, days_in_system=50),
        ],
        "many_drivers": [
            Driver("D1", "Top Rated", rating=5.0, location_km=5.0, days_in_system=200),
            Driver("D2", "Experienced", rating=4.8, location_km=3.0, days_in_system=150),
            Driver("D3", "New Star", rating=4.7, location_km=1.5, days_in_system=3),
            Driver("D4", "Veteran", rating=4.6, location_km=8.0, days_in_system=300),
            Driver("D5", "Close Pro", rating=4.5, location_km=0.5, days_in_system=100),
            Driver("D6", "Mid Range", rating=4.0, location_km=7.0, days_in_system=80),
            Driver("D7", "New Driver", rating=3.8, location_km=2.0, days_in_system=1),
            Driver("D8", "Average", rating=3.5, location_km=4.0, days_in_system=60),
            Driver("D9", "Far Away", rating=4.2, location_km=15.0, days_in_system=120),
            Driver("D10", "Close New", rating=3.9, location_km=1.0, days_in_system=5),
            Driver("D11", "Backup 1", rating=3.7, location_km=6.0, days_in_system=40),
            Driver("D12", "Backup 2", rating=3.6, location_km=9.0, days_in_system=30),
        ],
        "few_drivers": [
            Driver("D1", "Only Option", rating=4.0, location_km=5.0, days_in_system=50),
            Driver("D2", "Far Backup", rating=3.5, location_km=20.0, days_in_system=100),
        ],
        "new_drivers": [
            Driver("D1", "Day 1", rating=4.5, location_km=2.0, days_in_system=1),
            Driver("D2", "Day 2", rating=4.3, location_km=3.0, days_in_system=2),
            Driver("D3", "Day 3", rating=4.0, location_km=1.5, days_in_system=3),
            Driver("D4", "Day 5", rating=3.8, location_km=4.0, days_in_system=5),
        ],
        "busy_drivers": [
            Driver("D1", "Available", rating=4.5, location_km=2.0, days_in_system=50, is_busy=False),
            Driver("D2", "Busy", rating=4.9, location_km=1.0, days_in_system=100, is_busy=True),
            Driver("D3", "Available", rating=4.0, location_km=5.0, days_in_system=80, is_busy=False),
            Driver("D4", "Busy", rating=4.7, location_km=3.0, days_in_system=120, is_busy=True),
        ]
    }
    return scenarios.get(scenario, scenarios["default"])

def run_simulation(order=None, drivers=None, show_details=True):
    """
    Run the simulation with custom or default inputs.
    
    Args:
        order: MoveRequest object (optional)
        drivers: List of Driver objects (optional)
        show_details: Whether to show detailed output
    """
    # Setup Engines
    pricer = PricingEngine()
    dispatcher = DispatchEngine()

    # Use provided order or create default
    if order is None:
        order = MoveRequest(distance_km=15.0, vehicle_type=VehicleType.VAN, is_bad_weather=True)
    
    # Use provided drivers or create default
    if drivers is None:
        drivers = create_driver_pool("default")

    print("=" * 60)
    print("SIMULATION START")
    print("=" * 60)
    
    # Display Order Details
    print(f"\n📦 ORDER DETAILS:")
    print(f"   Distance: {order.distance_km} km")
    print(f"   Vehicle: {order.vehicle_type.name}")
    print(f"   Bad Weather: {'Yes' if order.is_bad_weather else 'No'}")
    
    # Display Driver Pool
    print(f"\n👥 DRIVER POOL ({len(drivers)} drivers):")
    for driver in drivers:
        status = "BUSY" if driver.is_busy else "Available"
        print(f"   {driver.name}: Rating={driver.rating}, Distance={driver.location_km}km, "
              f"Days={driver.days_in_system}, Status={status}")

    print("\n" + "-" * 60)
    print("--- 1. RANKING PHASE ---")
    print("-" * 60)
    ranked_drivers = dispatcher.rank_drivers(drivers)
    
    if show_details:
        print("\nRanking Results (sorted by score):")
        for idx, driver in enumerate(ranked_drivers[:5], 1):  # Show top 5
            score = dispatcher._calculate_score(driver)
            print(f"   {idx}. {driver.name}: Score={score:.3f} "
                  f"(Rating={driver.rating}, Distance={driver.location_km}km)")
    
    print(f"\n🏆 Winner: {ranked_drivers[0].name} (Highest Score)")

    print("\n" + "-" * 60)
    print("--- 2. BATCHING & DYNAMIC PRICING PHASE ---")
    print("-" * 60)
    batches = dispatcher.create_batches(ranked_drivers)

    for i, batch in enumerate(batches):
        attempt = i + 1
        current_price = pricer.calculate_price(order, attempt_number=attempt)
        
        print(f"\n📢 Batch {attempt}: Broadcasting to {len(batch)} drivers")
        print(f"   Drivers in batch: {', '.join([d.name for d in batch])}")
        print(f"   💰 Dynamic Price Offer: ${current_price:.2f}")
        
        # Show price breakdown
        base_price = pricer.base_rates[order.vehicle_type] + (order.distance_km * 2.0)
        weather_price = base_price * pricer.weather_multiplier if order.is_bad_weather else base_price
        surge_factor = 1.15 ** (attempt - 1)
        
        if show_details:
            print(f"   Breakdown:")
            print(f"      Base: ${base_price:.2f}")
            if order.is_bad_weather:
                print(f"      Weather multiplier (1.4x): ${weather_price:.2f}")
            print(f"      Surge factor (attempt {attempt}): {surge_factor:.2f}x")
        
        # Simulation Logic
        if attempt == 3:
            print(f"   ⚠️  Strategy: 'Panic Broadcast' to all remaining drivers")
        
        # Simulating time delay between batches
        # time.sleep(10)
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)

def run_scenario(scenario_name):
    """Run predefined scenarios"""
    scenarios = {
        "short_trip": {
            "order": MoveRequest(distance_km=5.0, vehicle_type=VehicleType.MINI_TRUCK, is_bad_weather=False),
            "drivers": create_driver_pool("default")
        },
        "long_trip": {
            "order": MoveRequest(distance_km=50.0, vehicle_type=VehicleType.TRUCK, is_bad_weather=False),
            "drivers": create_driver_pool("many_drivers")
        },
        "bad_weather": {
            "order": MoveRequest(distance_km=20.0, vehicle_type=VehicleType.VAN, is_bad_weather=True),
            "drivers": create_driver_pool("default")
        },
        "few_options": {
            "order": MoveRequest(distance_km=10.0, vehicle_type=VehicleType.VAN, is_bad_weather=False),
            "drivers": create_driver_pool("few_drivers")
        },
        "new_drivers": {
            "order": MoveRequest(distance_km=12.0, vehicle_type=VehicleType.VAN, is_bad_weather=False),
            "drivers": create_driver_pool("new_drivers")
        },
        "busy_market": {
            "order": MoveRequest(distance_km=15.0, vehicle_type=VehicleType.VAN, is_bad_weather=False),
            "drivers": create_driver_pool("busy_drivers")
        }
    }
    
    if scenario_name not in scenarios:
        print(f"Unknown scenario: {scenario_name}")
        print(f"Available scenarios: {', '.join(scenarios.keys())}")
        return
    
    config = scenarios[scenario_name]
    print(f"\n🎬 Running scenario: {scenario_name.upper()}\n")
    run_simulation(order=config["order"], drivers=config["drivers"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run logistics pricing simulation")
    parser.add_argument("--scenario", type=str, help="Predefined scenario to run",
                       choices=["short_trip", "long_trip", "bad_weather", "few_options", 
                               "new_drivers", "busy_market"])
    parser.add_argument("--distance", type=float, help="Distance in km")
    parser.add_argument("--vehicle", type=str, choices=["MINI_TRUCK", "VAN", "TRUCK"],
                       help="Vehicle type")
    parser.add_argument("--weather", action="store_true", help="Bad weather conditions")
    parser.add_argument("--driver-pool", type=str, 
                       choices=["default", "many_drivers", "few_drivers", "new_drivers", "busy_drivers"],
                       help="Driver pool scenario")
    
    args = parser.parse_args()
    
    if args.scenario:
        # Run predefined scenario
        run_scenario(args.scenario)
    else:
        # Run with custom or default parameters
        order = None
        drivers = None
        
        if args.distance or args.vehicle or args.weather:
            vehicle_type = VehicleType[args.vehicle] if args.vehicle else VehicleType.VAN
            distance = args.distance if args.distance else 15.0
            order = MoveRequest(distance_km=distance, vehicle_type=vehicle_type, 
                              is_bad_weather=args.weather)
        
        if args.driver_pool:
            drivers = create_driver_pool(args.driver_pool)
        
        run_simulation(order=order, drivers=drivers)