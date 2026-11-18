# Game-Theoretic Modeling of Autonomous Vehicle Interaction at Unsignalized Intersections

This repository contains the Python implementation and reproducible outputs for a stylized, symmetric two-player Game of Chicken model in which each autonomous vehicle chooses **Go** or **Yield**.

## Scope and limitations

This is a mathematical game-theory model with Monte Carlo sampling. It is **not** a physical traffic simulator and does not estimate real-world collision probability, crash rates, vehicle trajectories, delay, throughput, or safety performance. The payoff parameters are normalized model costs, not values calibrated from traffic observations.

## Repository contents

```text
.
├── intersection_game_simulation.py   # Model, Monte Carlo simulation, CSV and plot generation
├── requirements.txt                  # Python dependencies
├── data/
│   ├── baseline_results.csv          # Baseline outcome frequencies, counts and chi-square test
│   └── conflict_penalty_sweep.csv    # Parameter sweep over conflict penalty C
├── figures/
│   ├── equilibrium_sweep.png         # Equilibrium Go probability against C
│   └── monte_carlo_validation.png    # Theoretical vs simulated baseline outcomes
└── media/
    └── simulation_demo.mp4           # Optional illustrative demonstration video
```

## Model and baseline parameters

The symmetric mixed-strategy equilibrium probability of choosing Go is

\[
p^* = \frac{W}{C-D+W},
\]

under the parameter conditions \(C>D>0\) and \(W>0\).

The baseline values used in the supplied simulation are:

| Parameter | Value | Meaning |
|---|---:|---|
| `C` | 5.0 | Cost when both players choose Go |
| `D` | 1.0 | Cost of yielding while the other player goes |
| `W` | 2.0 | Cost of mutual yielding |
| `N` | 10,000 | Monte Carlo trials |
| `SEED` | 20261024 | Baseline random seed |

The parameter sweep evaluates `C` from 2.0 to 10.0 in increments of 0.5. A deterministic seed is assigned to each sweep value (`SEED + int(C * 100)`).

## Requirements

- Python 3.9 or newer
- NumPy
- Matplotlib
- SciPy

## Reproduce the outputs

1. Clone or download this repository.
2. Open a terminal in the repository's root directory.
3. (Recommended) Create and activate a virtual environment.
4. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Run the simulation:

   ```bash
   python intersection_game_simulation.py
   ```

The script prints the baseline results and writes the CSV files to `data/` and plots to `figures/`. Running it again with the same software environment and seed reproduces the same random samples and outputs.

## Coverage note for manuscript replication

The uploaded source file supplied for preparing this repository implements the baseline Monte Carlo experiment and the conflict-penalty (`C`) sweep. It does not, by itself, implement every additional analysis described in the manuscript (for example, the 2,000-replicate experiment and any separate confidence-interval or `D`/`W` sensitivity analyses). Those analyses should be added and independently checked before describing this repository as a complete reproduction package for every table and figure in the manuscript.

The baseline output generated from the supplied seed is `Yield/Yield = 0.4476` (4,476 of 10,000 trials); the theoretical probability is `0.4444`. If the manuscript body reports `0.444` as the *simulated* frequency, correct that wording/value or clearly identify it as the theoretical probability. The manuscript's table reports the simulated value `0.4476`.

## Statistical test

The script performs a Pearson chi-square goodness-of-fit test comparing the four observed baseline outcome counts with the theoretical probabilities implied by independent play at the equilibrium Go probability. The test has 3 degrees of freedom. This is a check of the Monte Carlo sample against the model's theoretical distribution; it is not a test of real-world traffic safety.

## Reproducibility notes

- Baseline seed: `20261024`.
- Baseline sample size: `10,000`.
- Sweep seeds are deterministically derived from the baseline seed and the corresponding `C` value.
- CSV output includes counts as well as frequencies to make the reported values auditable.
- The model assumes independent action draws by the two players at the symmetric mixed-strategy probability.

## Citation

If you use this code, please cite the associated manuscript:

> S. Srinivasan, S. Karthikeya, and Rashikaa KV, “Game-Theoretic Modeling of Autonomous Vehicle Interaction at Unsignalized Intersections: A Nash Equilibrium Analysis of the Game of Chicken,” [publication details to be added after publication].

## License

No license has been specified for this repository. Unless a license is added, standard copyright restrictions apply; reuse permissions are not automatically granted.
