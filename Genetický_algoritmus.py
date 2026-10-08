
import csv
import random
import statistics
from pathlib import Path

import matplotlib.pyplot as plt


def one_max(individual):
    return sum(individual)


def leading_ones(individual):
    result = 0

    for bit in individual:
        if bit == 1:
            result += 1
        else:
            break

    return result


def create_individual(dimension):
    return [random.randint(0, 1) for _ in range(dimension)]


def selection_weights(fitness_values, selection_type):
    if selection_type == "roulette":
        if sum(fitness_values) == 0:
            return None
        return fitness_values

    if selection_type == "rank":
        indexes = list(range(len(fitness_values)))
        random.shuffle(indexes)
        indexes.sort(key=lambda i: fitness_values[i])

        weights = [0] * len(fitness_values)
        for rank, index in enumerate(indexes, start=1):
            weights[index] = rank
        return weights

    raise ValueError("Unknown selection type")


def one_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def two_point_crossover(parent1, parent2):
    point1, point2 = sorted(random.sample(range(1, len(parent1)), 2))
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2


def crossover(parent1, parent2, crossover_type):
    if crossover_type == "one_point":
        return one_point_crossover(parent1, parent2)
    if crossover_type == "two_point":
        return two_point_crossover(parent1, parent2)
    raise ValueError("Unknown crossover type")


def mutate(individual, mutation_probability):
    child = individual.copy()
    for i in range(len(child)):
        if random.random() < mutation_probability:
            child[i] = 1 - child[i]
    return child


def genetic_algorithm(
    dimension,
    fitness_function,
    max_evaluations,
    population_size=20,
    elitism_ratio=0.1,
    crossover_probability=1.0,
    mutation_probability=0.005,
    selection_type="rank",
    crossover_type="one_point"
):
    if dimension < 2 or (crossover_type == "two_point" and dimension < 3):
        raise ValueError("Dimension is too small for crossover")
    if population_size < 2 or population_size > max_evaluations:
        raise ValueError("Invalid population size")
    if not 0 <= elitism_ratio < 1:
        raise ValueError("Elitism ratio must be between 0 and 1")
    if not 0 <= crossover_probability <= 1 or not 0 <= mutation_probability <= 1:
        raise ValueError("Probabilities must be between 0 and 1")

    population = [create_individual(dimension) for _ in range(population_size)]
    fitness_values = []
    convergence = []
    best_fitness = 0
    evaluations = 0

    for individual in population:
        fitness = fitness_function(individual)
        fitness_values.append(fitness)
        evaluations += 1
        best_fitness = max(best_fitness, fitness)
        convergence.append(best_fitness)

    while evaluations < max_evaluations:
        sorted_indexes = sorted(
            range(len(population)),
            key=lambda i: fitness_values[i],
            reverse=True
        )
        elite_count = min(int(population_size * elitism_ratio), population_size - 1)

        new_population = [population[i].copy() for i in sorted_indexes[:elite_count]]
        new_fitness_values = [fitness_values[i] for i in sorted_indexes[:elite_count]]
        weights = selection_weights(fitness_values, selection_type)

        while len(new_population) < population_size and evaluations < max_evaluations:
            parent1, parent2 = random.choices(population, weights=weights, k=2)

            if random.random() < crossover_probability:
                child1, child2 = crossover(parent1, parent2, crossover_type)
            else:
                child1, child2 = parent1.copy(), parent2.copy()

            for child in (mutate(child1, mutation_probability), mutate(child2, mutation_probability)):
                if len(new_population) >= population_size or evaluations >= max_evaluations:
                    break

                fitness = fitness_function(child)
                evaluations += 1
                best_fitness = max(best_fitness, fitness)

                new_population.append(child)
                new_fitness_values.append(fitness)
                convergence.append(best_fitness)

        population = new_population
        fitness_values = new_fitness_values

    return best_fitness, convergence


def run_experiment(problem_name, fitness_function, dimension, runs, settings):
    max_evaluations = 100 * dimension
    final_results = []
    all_convergences = []
    first_optimum_evaluations = []

    for run in range(runs):
        random.seed(1000 + run + dimension * 10 + (0 if problem_name == "OneMax" else 100000))
        best, convergence = genetic_algorithm(
            dimension=dimension,
            fitness_function=fitness_function,
            max_evaluations=max_evaluations,
            **settings
        )

        final_results.append(best)
        all_convergences.append(convergence)
        if best == dimension:
            first_optimum_evaluations.append(convergence.index(dimension) + 1)

    average_convergence = [sum(values) / runs for values in zip(*all_convergences)]
    stats = {
        "best": max(final_results),
        "worst": min(final_results),
        "mean": statistics.mean(final_results),
        "median": statistics.median(final_results),
        "std": statistics.stdev(final_results),
        "optimal_runs": len(first_optimum_evaluations),
        "avg_optimum_evaluations": (
            statistics.mean(first_optimum_evaluations)
            if first_optimum_evaluations else None
        )
    }
    return stats, average_convergence


def draw_graph(problem_name, dimension, curves, output_dir):
    plt.figure(figsize=(11, 6))

    for label, convergence in curves.items():
        plt.plot(range(1, len(convergence) + 1), convergence, label=label)

    plt.axhline(dimension, linestyle="--", color="gray", linewidth=1, label="Optimum")
    plt.title(f"{problem_name} - Average Convergence - {dimension}D (10 runs)")
    plt.xlabel("Fitness Evaluations")
    plt.ylabel("Best Fitness (average)")
    plt.legend(fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    file_name = output_dir / f"{problem_name}_{dimension}D.png"
    plt.savefig(file_name, dpi=150)
    plt.close()
    print(f"Graph saved: {file_name}")


def main():
    base_settings = {
        "population_size": 20,
        "elitism_ratio": 0.10,
        "crossover_probability": 1.0,
        "mutation_probability": 0.005,
        "selection_type": "rank",
        "crossover_type": "one_point"
    }

    experiments = [
        ("Baseline", {}),
        ("Population 50", {"population_size": 50}),
        ("Elitism 20%", {"elitism_ratio": 0.20}),
        ("Crossover 70%", {"crossover_probability": 0.70}),
        ("Mutation 1%", {"mutation_probability": 0.01}),
        ("Roulette", {"selection_type": "roulette"}),
        ("Two-point", {"crossover_type": "two_point"})
    ]

    problems = [("OneMax", one_max), ("LeadingOnes", leading_ones)]
    dimensions = [10, 30, 100]
    runs = 10
    output_dir = Path(__file__).resolve().parent / "genetic_results"
    output_dir.mkdir(exist_ok=True)
    summary_rows = []

    for problem_name, fitness_function in problems:
        for dimension in dimensions:
            print(f"\n{'=' * 85}")
            print(f"{problem_name} - {dimension}D, {runs} runs, {100 * dimension} evaluations per run")
            print(f"{'=' * 85}")
            print(f"{'Configuration':<18} {'Best':>5} {'Worst':>6} {'Mean':>7} {'Median':>7} {'Std':>7} {'Optimal':>8}")

            curves = {}
            group_rows = []

            for label, changes in experiments:
                settings = {**base_settings, **changes}
                stats, average_convergence = run_experiment(
                    problem_name, fitness_function, dimension, runs, settings
                )
                curves[label] = average_convergence

                row = {
                    "problem": problem_name,
                    "dimension": dimension,
                    "configuration": label,
                    **settings,
                    **stats
                }
                group_rows.append(row)
                summary_rows.append(row)

                print(
                    f"{label:<18} {stats['best']:>5} {stats['worst']:>6} "
                    f"{stats['mean']:>7.2f} {stats['median']:>7.2f} "
                    f"{stats['std']:>7.2f} {stats['optimal_runs']:>5}/{runs}"
                )

            best = max(
                group_rows,
                key=lambda row: (
                    row["mean"], row["optimal_runs"],
                    -row["avg_optimum_evaluations"]
                    if row["avg_optimum_evaluations"] is not None else float("-inf")
                )
            )
            print(f"Best configuration: {best['configuration']}")
            draw_graph(problem_name, dimension, curves, output_dir)

    csv_file = output_dir / "summary.csv"
    with csv_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"\nResults saved to: {output_dir}")
    print(f"Summary saved to: {csv_file}")


if __name__ == "__main__":
    main()
