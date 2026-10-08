# Genetic Algorithm
**Optimization of OneMax and LeadingOnes Problems**

---

## 1. Objective

The goal of this project is to implement and evaluate a genetic algorithm using binary chromosomes. The algorithm is tested on two optimization problems:

- **OneMax** - maximizes the total number of `1` bits in a chromosome.
- **LeadingOnes** - maximizes the number of consecutive `1` bits starting from the beginning of a chromosome.

Both problems have an optimal fitness equal to the chromosome length `D`.

## 2. Algorithm Design

Each individual is represented as a binary chromosome of length `D`.

The algorithm follows these steps:

1. **Initialization** - generate a random population.
2. **Elitism** - preserve the best individuals in the next generation.
3. **Selection** - select two parents using roulette or rank selection.
4. **Crossover** - generate two offspring using one-point or two-point crossover.
5. **Mutation** - independently flip each offspring bit with a specified probability.
6. **Replacement** - add offspring to the new population and repeat until the evaluation budget is exhausted.

Elite individuals retain their previously calculated fitness values.

## 3. Experimental Setup

Experiments are performed for three chromosome lengths, with **10 independent runs** per configuration.

| Dimension | Fitness Evaluations | Runs |
|:---:|---:|:---:|
| 10D | 1,000 | 10 |
| 30D | 3,000 | 10 |
| 100D | 10,000 | 10 |

### Default Parameters

| Parameter | Value |
|---|---|
| Population size | 20 |
| Elitism ratio | 10% |
| Crossover probability | 100% |
| Mutation probability | 0.5% per bit |
| Selection method | Rank |
| Crossover method | One-point |

### Parameter Variations

To investigate parameter influence, six additional configurations are compared against the baseline:

| Configuration | Modified Parameter |
|---|---|
| Population 50 | Population size → 50 |
| Elitism 20% | Elitism ratio → 20% |
| Crossover 70% | Crossover probability → 70% |
| Mutation 1% | Mutation probability → 1% |
| Roulette | Rank → Roulette selection |
| Two-point | One-point → Two-point crossover |

Only one parameter is changed at a time to make comparisons easier.

## 4. Experimental Results

### 4.1 Baseline Performance

The following statistics represent the final best fitness values obtained across 10 runs.

| Problem | Dimension | Best | Worst | Mean | Median | Std. Dev. |
|---|---|---|---|---|---|---|
| OneMax | 10D | 10 | 10 | 10.00 | 10.00 | 0.00 |
| OneMax | 30D | 30 | 30 | 30.00 | 30.00 | 0.00 |
| OneMax | 100D | 100 | 100 | 100.00 | 100.00 | 0.00 |
| LeadingOnes | 10D | 10 | 9 | 9.90 | 10.00 | 0.32 |
| LeadingOnes | 30D | 30 | 11 | 22.90 | 24.00 | 5.67 |
| LeadingOnes | 100D | 88 | 41 | 70.90 | 68.50 | 13.21 |

*Standard deviation is calculated using the sample standard deviation.*

### 4.2 Best Configurations

The best tested configurations were selected primarily by average fitness, followed by the number of successful runs and convergence speed.

| Problem | Dimension | Best Configuration | Mean Fitness | Optimal Runs |
|---|---|---|---|---|
| OneMax | 10D | Baseline | 10.00 | 10/10 |
| OneMax | 30D | Mutation 1% | 30.00 | 10/10 |
| OneMax | 100D | Two-point | 100.00 | 10/10 |
| LeadingOnes | 10D | Population 50 | 10.00 | 10/10 |
| LeadingOnes | 30D | Mutation 1% | 29.60 | 9/10 |
| LeadingOnes | 100D | Mutation 1% | 76.70 | 0/10 |

### 4.3 Convergence Analysis

The convergence graphs show the **average best-so-far fitness over 10 runs** as a function of the number of fitness evaluations. The horizontal dashed line represents the optimal fitness.

Complete statistics for all 42 experimental configurations are available in [`genetic_results/summary.csv`](genetic_results/summary.csv).

## 5. Discussion

**OneMax**

The algorithm successfully reached the optimum in all 10 baseline runs for every dimension. Parameter changes mainly influenced convergence speed rather than final solution quality.

**LeadingOnes**

The problem became more difficult as dimensionality increased. Increasing mutation probability from 0.5% to 1% improved the results, particularly in 30D, where the number of successful runs increased from 1/10 to 9/10.

In 100D, none of the tested configurations reached the global optimum within the evaluation budget. However, the 1% mutation configuration achieved the highest average fitness of 76.70.

## 6. Conclusion

The experiments demonstrate that the genetic algorithm effectively solves the OneMax problem, while LeadingOnes requires more careful parameter selection, particularly at higher dimensions.

Among the tested configurations, increasing mutation probability to **1%** provided the most noticeable improvement for LeadingOnes.

Overall, the results confirm that population size, elitism, selection, crossover, and mutation parameters influence both convergence speed and solution quality. Further experiments with additional parameter combinations and more independent runs could provide more reliable conclusions.

---

## 7. Convergence Graphs

The following graphs compare the average convergence of all tested configurations over 10 runs.

### OneMax

- [OneMax – 10D](genetic_results/OneMax_10D.png)
- [OneMax – 30D](genetic_results/OneMax_30D.png)
- [OneMax – 100D](genetic_results/OneMax_100D.png)

### LeadingOnes

- [LeadingOnes – 10D](genetic_results/LeadingOnes_10D.png)
- [LeadingOnes – 30D](genetic_results/LeadingOnes_30D.png)
- [LeadingOnes – 100D](genetic_results/LeadingOnes_100D.png)