"""
Speed benchmark: PyWorld3-03 vs fast_pyworld3

Measures execution time for both implementations.
Note: PyWorld3-03 fast mode is disabled due to bugs.
"""

import gc
import statistics
import sys
import time

import numpy as np

# Number of runs for statistical significance
NUM_RUNS = 10
WARMUP_RUNS = 2


def benchmark_pyworld3_03(num_runs: int = NUM_RUNS) -> dict:
    """Benchmark PyWorld3-03 implementation"""
    sys.path.insert(0, r"../PyWorld3-03")
    from pyworld3 import World3 as World3_Old

    times = []

    # Warmup runs
    for _ in range(WARMUP_RUNS):
        world3 = World3_Old(year_min=1900, year_max=2100, dt=0.5)
        world3.init_world3_constants()
        world3.init_world3_variables()
        world3.set_world3_table_functions()
        world3.set_world3_delay_functions()
        world3.run_world3(fast=False)
        del world3
        gc.collect()

    # Timed runs
    for i in range(num_runs):
        gc.collect()

        start = time.perf_counter()

        world3 = World3_Old(year_min=1900, year_max=2100, dt=0.5)
        world3.init_world3_constants()
        world3.init_world3_variables()
        world3.set_world3_table_functions()
        world3.set_world3_delay_functions()
        world3.run_world3(fast=False)

        end = time.perf_counter()
        times.append(end - start)

        del world3

    return {
        "times": times,
        "mean": statistics.mean(times),
        "std": statistics.stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
        "median": statistics.median(times),
    }


def benchmark_new_world_3(num_runs: int = NUM_RUNS) -> dict:
    """Benchmark fast_pyworld3 implementation"""
    sys.path.insert(
        0,
        r"src",
    )
    from fast_pyworld3.core import World3, World3Config

    times = []

    # Warmup runs
    for _ in range(WARMUP_RUNS):
        config = World3Config(year_min=1900, year_max=2100, dt=0.5)
        world3 = World3(config)
        world3.init_constants()
        world3.init_variables()
        world3.set_table_functions()
        world3.set_delay_functions()
        world3.run()
        del world3
        gc.collect()

    # Timed runs
    for i in range(num_runs):
        gc.collect()

        start = time.perf_counter()

        config = World3Config(year_min=1900, year_max=2100, dt=0.5)
        world3 = World3(config)
        world3.init_constants()
        world3.init_variables()
        world3.set_table_functions()
        world3.set_delay_functions()
        world3.run()

        end = time.perf_counter()
        times.append(end - start)

        del world3

    return {
        "times": times,
        "mean": statistics.mean(times),
        "std": statistics.stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
        "median": statistics.median(times),
    }


def benchmark_phases_pyworld3_03() -> dict:
    """Benchmark individual phases of PyWorld3-03"""
    sys.path.insert(
        0, r"../PyWorld3-03"
    )
    from pyworld3 import World3 as World3_Old

    phase_times = {
        "init": [],
        "constants": [],
        "variables": [],
        "tables": [],
        "delays": [],
        "run": [],
    }

    for _ in range(NUM_RUNS):
        gc.collect()

        start = time.perf_counter()
        world3 = World3_Old(year_min=1900, year_max=2100, dt=0.5)
        phase_times["init"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.init_world3_constants()
        phase_times["constants"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.init_world3_variables()
        phase_times["variables"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.set_world3_table_functions()
        phase_times["tables"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.set_world3_delay_functions()
        phase_times["delays"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.run_world3(fast=False)
        phase_times["run"].append(time.perf_counter() - start)

        del world3

    return {
        name: {
            "mean": statistics.mean(t),
            "std": statistics.stdev(t) if len(t) > 1 else 0,
        }
        for name, t in phase_times.items()
    }


def benchmark_phases_new_world_3() -> dict:
    """Benchmark individual phases of new_world_3"""
    sys.path.insert(
        0,
        r"src",
    )
    from fast_pyworld3.core import World3, World3Config

    phase_times = {
        "init": [],
        "constants": [],
        "variables": [],
        "tables": [],
        "delays": [],
        "run": [],
    }

    for _ in range(NUM_RUNS):
        gc.collect()

        start = time.perf_counter()
        config = World3Config(year_min=1900, year_max=2100, dt=0.5)
        world3 = World3(config)
        phase_times["init"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.init_constants()
        phase_times["constants"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.init_variables()
        phase_times["variables"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.set_table_functions()
        phase_times["tables"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.set_delay_functions()
        phase_times["delays"].append(time.perf_counter() - start)

        start = time.perf_counter()
        world3.run()
        phase_times["run"].append(time.perf_counter() - start)

        del world3

    return {
        name: {
            "mean": statistics.mean(t),
            "std": statistics.stdev(t) if len(t) > 1 else 0,
        }
        for name, t in phase_times.items()
    }


def compare_results() -> dict:
    """Compare output values between PyWorld3-03 and new_world_3"""
    sys.path.insert(
        0, r"../PyWorld3-03"
    )
    sys.path.insert(
        0,
        r"src",
    )

    from pyworld3 import World3 as World3_Old
    from fast_pyworld3.core import World3, World3Config

    # Run PyWorld3-03
    world3_old = World3_Old(year_min=1900, year_max=2100, dt=0.5)
    world3_old.init_world3_constants()
    world3_old.init_world3_variables()
    world3_old.set_world3_table_functions()
    world3_old.set_world3_delay_functions()
    world3_old.run_world3(fast=False)

    # Run new_world_3
    config = World3Config(year_min=1900, year_max=2100, dt=0.5)
    world3_new = World3(config)
    world3_new.init_constants()
    world3_new.init_variables()
    world3_new.set_table_functions()
    world3_new.set_delay_functions()
    world3_new.run()

    # Compare key variables
    variables_to_compare = [
        ("pop", "Total Population", world3_old.pop, world3_new.pop.pop),
        ("io", "Industrial Output", world3_old.io, world3_new.cap.io),
        ("fpc", "Food Per Capita", world3_old.fpc, world3_new.agr.fpc),
        ("ppolx", "Pollution Index", world3_old.ppolx, world3_new.pol.ppolx),
        ("nr", "Natural Resources", world3_old.nr, world3_new.res.nr),
    ]

    results = {}
    for var_name, var_label, old_vals, new_vals in variables_to_compare:
        # Remove NaN values for comparison
        valid_mask = ~(np.isnan(old_vals) | np.isnan(new_vals))
        old_valid = old_vals[valid_mask]
        new_valid = new_vals[valid_mask]

        if len(old_valid) == 0:
            continue

        # Calculate comparison metrics
        abs_diff = np.abs(old_valid - new_valid)
        rel_diff = abs_diff / (np.abs(old_valid) + 1e-10)  # Avoid division by zero

        results[var_name] = {
            "label": var_label,
            "mean_abs_error": np.mean(abs_diff),
            "max_abs_error": np.max(abs_diff),
            "mean_rel_error": np.mean(rel_diff) * 100,  # As percentage
            "max_rel_error": np.max(rel_diff) * 100,  # As percentage
            "correlation": np.corrcoef(old_valid, new_valid)[0, 1],
            "n_points": len(old_valid),
        }

    return results


def benchmark_dt_variations() -> dict:
    """Benchmark with different time step sizes"""
    sys.path.insert(
        0, r"../PyWorld3-03"
    )
    sys.path.insert(
        0,
        r"src",
    )

    from pyworld3 import World3 as World3_Old
    from fast_pyworld3.core import World3, World3Config

    results = {}
    dt_values = [1.0, 0.5, 0.25, 0.125]

    for dt in dt_values:
        # PyWorld3-03
        gc.collect()
        times_old = []
        for _ in range(5):
            start = time.perf_counter()
            world3 = World3_Old(year_min=1900, year_max=2100, dt=dt)
            world3.init_world3_constants()
            world3.init_world3_variables()
            world3.set_world3_table_functions()
            world3.set_world3_delay_functions()
            world3.run_world3(fast=False)
            times_old.append(time.perf_counter() - start)
            del world3

        # new_world_3
        gc.collect()
        times_new = []
        for _ in range(5):
            start = time.perf_counter()
            config = World3Config(year_min=1900, year_max=2100, dt=dt)
            world3 = World3(config)
            world3.init_constants()
            world3.init_variables()
            world3.set_table_functions()
            world3.set_delay_functions()
            world3.run()
            times_new.append(time.perf_counter() - start)
            del world3

        n_steps = int(200 / dt) + 1
        results[dt] = {
            "n_steps": n_steps,
            "pyworld3_03": statistics.mean(times_old),
            "new_world_3": statistics.mean(times_new),
        }

    return results


def print_results(name: str, results: dict):
    """Print benchmark results"""
    print(f"\n{name}")
    print(f"  Mean:   {results['mean'] * 1000:8.2f} ms")
    print(f"  Std:    {results['std'] * 1000:8.2f} ms")
    print(f"  Min:    {results['min'] * 1000:8.2f} ms")
    print(f"  Max:    {results['max'] * 1000:8.2f} ms")
    print(f"  Median: {results['median'] * 1000:8.2f} ms")


def main():
    print("=" * 70)
    print("WORLD3 SPEED BENCHMARK")
    print(f"Runs: {NUM_RUNS} (+ {WARMUP_RUNS} warmup)")
    print("=" * 70)

    # Standard benchmark
    print("\n" + "-" * 70)
    print("1. BENCHMARK COMPARISON")
    print("-" * 70)

    print("\nRunning PyWorld3-03...")
    old_standard = benchmark_pyworld3_03()
    print_results("PyWorld3-03", old_standard)

    print("\nRunning new_world_3...")
    new_standard = benchmark_new_world_3()
    print_results("new_world_3", new_standard)

    speedup = old_standard["mean"] / new_standard["mean"]
    diff_pct = (
        (new_standard["mean"] - old_standard["mean"]) / old_standard["mean"] * 100
    )
    print("\n  Comparison:")
    print(f"    Speedup ratio: {speedup:.3f}x")
    print(f"    Difference: {diff_pct:+.1f}%")
    if speedup > 1:
        print(f"    new_world_3 is {speedup:.2f}x FASTER")
    else:
        print(f"    new_world_3 is {1 / speedup:.2f}x SLOWER")

    # Results comparison
    print("\n" + "-" * 70)
    print("2. RESULTS VALIDATION")
    print("-" * 70)

    print("\nComparing output values...")
    comparison = compare_results()

    print("\nKey Variables Comparison:")
    print(
        f"{'Variable':<20} | {'Correlation':>12} | {'Mean Rel Err':>13} | {'Max Rel Err':>12}"
    )
    print("-" * 63)

    all_match = True
    for var_name, data in comparison.items():
        corr = data["correlation"]
        mean_err = data["mean_rel_error"]
        max_err = data["max_rel_error"]

        # Check if results are close enough (>99.9% correlation, <1% mean error)
        matches = corr > 0.999 and mean_err < 1.0
        status = "✓" if matches else "✗"
        all_match = all_match and matches

        print(
            f"{data['label']:<20} | {corr:>11.6f} | {mean_err:>11.4f} % | {max_err:>10.4f} % {status}"
        )

    if all_match:
        print("\n✓ All variables match within acceptable tolerance")
    else:
        print("\n⚠ Some variables show significant differences")

    # Phase breakdown
    print("\n" + "-" * 70)
    print("3. PHASE BREAKDOWN")
    print("-" * 70)

    print("\nPyWorld3-03 phases:")
    old_phases = benchmark_phases_pyworld3_03()
    for phase, data in old_phases.items():
        print(
            f"  {phase:12s}: {data['mean'] * 1000:8.2f} ms (+/- {data['std'] * 1000:.2f})"
        )

    print("\nnew_world_3 phases:")
    new_phases = benchmark_phases_new_world_3()
    for phase, data in new_phases.items():
        print(
            f"  {phase:12s}: {data['mean'] * 1000:8.2f} ms (+/- {data['std'] * 1000:.2f})"
        )

    print("\nPhase comparison (new vs old):")
    for phase in old_phases:
        old_t = old_phases[phase]["mean"]
        new_t = new_phases[phase]["mean"]
        if old_t > 0:
            ratio = new_t / old_t
            print(
                f"  {phase:12s}: {ratio:.2f}x {'(slower)' if ratio > 1 else '(faster)'}"
            )

    # dt variations
    print("\n" + "-" * 70)
    print("4. TIME STEP VARIATIONS")
    print("-" * 70)

    dt_results = benchmark_dt_variations()
    print(
        f"\n{'dt':>6s} | {'Steps':>6s} | {'PyWorld3-03':>12s} | {'new_world_3':>12s} | {'Ratio':>8s}"
    )
    print("-" * 55)
    for dt, data in dt_results.items():
        ratio = data["pyworld3_03"] / data["new_world_3"]
        print(
            f"{dt:6.3f} | {data['n_steps']:6d} | {data['pyworld3_03'] * 1000:10.2f} ms | {data['new_world_3'] * 1000:10.2f} ms | {ratio:7.2f}x"
        )

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(
        f"\nOverall: new_world_3 is {old_standard['mean'] / new_standard['mean']:.2f}x {'faster' if old_standard['mean'] > new_standard['mean'] else 'slower'}"
    )

    # Identify bottlenecks
    print("\nBottleneck Analysis (new_world_3):")
    total = sum(d["mean"] for d in new_phases.values())
    for phase, data in sorted(
        new_phases.items(), key=lambda x: x[1]["mean"], reverse=True
    ):
        pct = data["mean"] / total * 100
        print(f"  {phase:12s}: {pct:5.1f}% of total time")


if __name__ == "__main__":
    main()
