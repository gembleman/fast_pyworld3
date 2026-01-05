"""Example usage of the World3 model"""

from world3.core import World3, World3Config, hello_world3


def run_standard_scenario() -> None:
    """Run the standard Business as Usual scenario"""
    print("=" * 60)
    print("World3 Model - Standard Scenario")
    print("=" * 60)

    # Run the built-in hello world function
    hello_world3()


def run_custom_scenario() -> None:
    """Example of running a custom scenario"""
    print("\n" + "=" * 60)
    print("World3 Model - Custom Scenario")
    print("Early Technology Implementation")
    print("=" * 60 + "\n")

    # Create configuration
    config = World3Config(
        year_min=1900,
        year_max=2100,
        dt=0.5,
        pyear=1975,
        pyear_res_tech=1985,  # Earlier resource technology
        pyear_pp_tech=1985,  # Earlier pollution technology
    )

    # Create and initialize model
    world3 = World3(config)
    world3.init_constants(
        nri=1.5e12,  # 50% more resources
    )
    world3.init_variables()
    world3.set_table_functions()
    world3.set_delay_functions()

    # Run simulation
    print("Running simulation...")
    world3.run()
    print("Simulation complete!\n")

    # Display results
    results = world3.get_results()

    print("Key Results at 2100:")
    print(f"  Population:              {results['pop'][-1]:>12,.0f}")
    print(f"  Life Expectancy:         {results['le'][-1]:>12.1f} years")
    print(f"  IOPC:                    {results['iopc'][-1]:>12.2f} $/person/year")
    print(f"  Food per Capita:         {results['fpc'][-1]:>12.2f} kg/person/year")
    print(f"  Pollution Index:         {results['ppolx'][-1]:>12.2f}")
    print(f"  Resources Remaining:     {results['nrfr'][-1]:>12.1%}")
    print(f"  Human Welfare Index:     {results['hwi'][-1]:>12.3f}")

    # Compare with standard scenario
    print("\n" + "-" * 60)
    print("Note: This is a demonstration of how to run custom scenarios.")
    print("Full implementation of all sector updates required for accurate results.")
    print("-" * 60)


if __name__ == "__main__":
    # Run standard scenario
    run_standard_scenario()

    # Run custom scenario
    # run_custom_scenario()
