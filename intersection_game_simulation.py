"""Reproducible Monte Carlo exploration of a stylized two-player Go/Yield game.

This is a game-theoretic toy model, NOT a physical traffic simulator. It does
not estimate real-world collision probability, delay, throughput, or safety.

Run from the repository root:
    python intersection_game_simulation.py

Outputs are written to data/ and figures/.
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
FIGURES_DIR = ROOT / "figures"
SEED = 20261024
N = 10_000
D = 1.0       # cost of yielding while the other player goes
W = 2.0       # cost of mutual yielding
C_BASE = 5.0  # cost when both players choose Go
C_VALUES = np.arange(2.0, 10.01, 0.5)
OUTCOME_LABELS = ["Go/Go", "Go/Yield", "Yield/Go", "Yield/Yield"]


def equilibrium_go_probability(C: float, D: float, W: float) -> float:
    """Return the symmetric mixed-strategy equilibrium probability of Go."""
    if not (C > D > 0 and W > 0):
        raise ValueError("Parameters must satisfy C > D > 0 and W > 0.")
    return W / (C - D + W)


def simulate(C: float, D: float, W: float, n: int = N, seed: int = SEED) -> dict:
    """Simulate n independent action pairs using the symmetric equilibrium."""
    if n <= 0:
        raise ValueError("n must be a positive integer")
    p = equilibrium_go_probability(C, D, W)
    rng = np.random.default_rng(seed)
    a_go = rng.random(n) < p
    b_go = rng.random(n) < p
    counts = {
        "Go/Go": int(np.count_nonzero(a_go & b_go)),
        "Go/Yield": int(np.count_nonzero(a_go & ~b_go)),
        "Yield/Go": int(np.count_nonzero(~a_go & b_go)),
        "Yield/Yield": int(np.count_nonzero(~a_go & ~b_go)),
    }
    result = {
        "C": float(C), "D": float(D), "W": float(W), "N": int(n),
        "seed": int(seed), "p_theory": float(p),
        **{k: v / n for k, v in counts.items()},
        **{f"{k}_count": v for k, v in counts.items()},
        "pA_empirical": float(np.mean(a_go)),
        "pB_empirical": float(np.mean(b_go)),
    }
    theoretical = [p * p, p * (1-p), (1-p) * p, (1-p) * (1-p)]
    expected_counts = np.asarray(theoretical) * n
    chi = chisquare([counts[k] for k in OUTCOME_LABELS], f_exp=expected_counts)
    result["chi_square"] = float(chi.statistic)
    result["chi_square_df"] = 3
    result["chi_square_p_value"] = float(chi.pvalue)
    return result


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    FIGURES_DIR.mkdir(exist_ok=True)

    baseline = simulate(C_BASE, D, W, N, SEED)
    write_csv(DATA_DIR / "baseline_results.csv", [baseline])
    print("Baseline simulation")
    for key, value in baseline.items():
        print(f"{key}: {value}")

    sweep_rows = []
    for c in C_VALUES:
        # Deterministic seed per parameter value, matching the supplied script.
        res = simulate(float(c), D, W, N, SEED + int(c * 100))
        sweep_rows.append({
            "C": float(c),
            "p_theory": res["p_theory"],
            "Go_Go_empirical_frequency": res["Go/Go"],
            "N": N,
            "seed": res["seed"],
        })
    write_csv(DATA_DIR / "conflict_penalty_sweep.csv", sweep_rows)

    # Figure 1: theoretical equilibrium Go probability as C varies.
    cs = np.asarray([r["C"] for r in sweep_rows])
    ps = np.asarray([r["p_theory"] for r in sweep_rows])
    plt.figure()
    plt.plot(cs, ps, marker="o")
    plt.xlabel("Conflict penalty C (normalized utility units)")
    plt.ylabel("Equilibrium probability of Go, p*")
    plt.title("Equilibrium Go probability vs conflict penalty")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "equilibrium_sweep.png", dpi=180)
    plt.close()

    # Figure 2: theoretical and Monte Carlo baseline outcome frequencies.
    p = baseline["p_theory"]
    theoretical = [p*p, p*(1-p), (1-p)*p, (1-p)*(1-p)]
    empirical = [baseline[k] for k in OUTCOME_LABELS]
    x = np.arange(len(OUTCOME_LABELS))
    width = 0.36
    plt.figure()
    plt.bar(x-width/2, theoretical, width, label="Theoretical")
    plt.bar(x+width/2, empirical, width, label=f"Monte Carlo (N={N:,})")
    plt.xticks(x, OUTCOME_LABELS, rotation=12, ha="right")
    plt.ylabel("Outcome frequency")
    plt.title("Theoretical vs Monte Carlo outcome frequencies")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "monte_carlo_validation.png", dpi=180)
    plt.close()

    print("\nGenerated data/baseline_results.csv")
    print("Generated data/conflict_penalty_sweep.csv")
    print("Generated figures/equilibrium_sweep.png")
    print("Generated figures/monte_carlo_validation.png")


if __name__ == "__main__":
    main()
