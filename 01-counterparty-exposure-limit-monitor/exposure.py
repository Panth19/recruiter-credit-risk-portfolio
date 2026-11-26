"""Monte Carlo exposure engine for illustrative commodity and FX forwards."""
import numpy as np
import pandas as pd

ASSETS = ["Copper", "Brent", "EURUSD"]
SPOT = {"Copper": 9000.0, "Brent": 80.0, "EURUSD": 1.09}
VOL = {"Copper": 0.28, "Brent": 0.32, "EURUSD": 0.10}
CORR = np.array([[1.00, 0.45, 0.05], [0.45, 1.00, 0.10], [0.05, 0.10, 1.00]])

def simulate(trades, limits, n_sims=5000, months=24, rate=0.035, seed=42):
    rng = np.random.default_rng(seed)
    dt = 1 / 12
    chol = np.linalg.cholesky(CORR)
    vols = np.array([VOL[a] for a in ASSETS])
    spots = np.empty((n_sims, months + 1, len(ASSETS)))
    spots[:, 0, :] = [SPOT[a] for a in ASSETS]
    for m in range(1, months + 1):
        z = rng.standard_normal((n_sims, len(ASSETS))) @ chol.T
        spots[:, m, :] = spots[:, m-1, :] * np.exp((-0.5 * vols**2) * dt + vols * np.sqrt(dt) * z)
    rows = []
    cpty_names = list(limits.counterparty)
    for m in range(months + 1):
        t = m * dt
        net = {c: np.zeros(n_sims) for c in cpty_names}
        for trade in trades.itertuples(index=False):
            if t > trade.maturity_years:
                continue
            idx = ASSETS.index(trade.asset)
            sign = 1.0 if trade.direction == "Buy" else -1.0
            tau = max(trade.maturity_years - t, 0.0)
            # PV of contractual settlement under a flat USD discount rate.
            mtm = sign * trade.quantity * (spots[:, m, idx] - trade.strike * np.exp(-rate * tau))
            net[trade.counterparty] += mtm
        for c in cpty_names:
            exposure = np.maximum(net[c], 0.0)  # counterparty-level close-out netting, no collateral
            rows.append({"month": m, "year_fraction": t, "counterparty": c,
                         "EPE": exposure.mean(), "PFE95": np.quantile(exposure, .95),
                         "PFE99": np.quantile(exposure, .99), "current_exposure": exposure[0] if m == 0 else np.nan})
    profile = pd.DataFrame(rows)
    summary = profile.groupby("counterparty").agg(peak_EPE=("EPE", "max"), peak_PFE95=("PFE95", "max"), peak_PFE99=("PFE99", "max")).reset_index()
    summary = summary.merge(limits, on="counterparty", how="left")
    summary["breach"] = summary.peak_PFE95 > summary.credit_limit
    summary["headroom_to_PFE95"] = summary.credit_limit - summary.peak_PFE95
    profile = profile.merge(limits, on="counterparty", how="left")
    profile["breach"] = profile.PFE95 > profile.credit_limit
    return profile, summary, spots
