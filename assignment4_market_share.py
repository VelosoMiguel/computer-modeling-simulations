import random
import numpy as np
import matplotlib.pyplot as plt

# ── Parameters ───────────────────────────────────────────────────────────────
TOTAL_CUSTOMERS   = 10_000
MONTHS            = 24
REVENUE_PER_CUST  = 100      # $ per customer per month
CAMPAIGN_COST     = 50_000   # flat one-time fee
TRIALS            = 100
BRANDS            = ['A', 'B', 'C']

# ── Baseline Transition Matrix ───────────────────────────────────────────────
# transition[from_brand][to_brand]
BASELINE = {
    'A': {'A': 0.80, 'B': 0.10, 'C': 0.10},
    'B': {'A': 0.15, 'B': 0.75, 'C': 0.10},
    'C': {'A': 0.15, 'B': 0.10, 'C': 0.75},
}

# ── Campaign Transition Matrix ────────────────────────────────────────────────
# B->A increases by 0.05 (0.15 -> 0.20); reduce B->B by 0.05 (0.75 -> 0.70)
# C->A increases by 0.05 (0.15 -> 0.20); reduce C->C by 0.05 (0.75 -> 0.70)
CAMPAIGN = {
    'A': {'A': 0.80, 'B': 0.10, 'C': 0.10},   # unchanged
    'B': {'A': 0.20, 'B': 0.70, 'C': 0.10},   # B->A +0.05, B->B -0.05
    'C': {'A': 0.20, 'B': 0.10, 'C': 0.70},   # C->A +0.05, C->C -0.05
}

# Verify rows sum to 1.0
for label, matrix in [("Baseline", BASELINE), ("Campaign", CAMPAIGN)]:
    for brand in BRANDS:
        total = sum(matrix[brand].values())
        assert abs(total - 1.0) < 1e-9, f"{label} row {brand} sums to {total}"

# ── Task 1 & 2: Simulation function ─────────────────────────────────────────
def simulate_market(matrix: dict) -> float:
    """
    Simulate 24 months of brand competition.
    Returns Brand A's total cumulative revenue over 24 months.
    """
    # Equal start: ~3,333 each (use integer split)
    counts = {b: TOTAL_CUSTOMERS // 3 for b in BRANDS}
    remainder = TOTAL_CUSTOMERS - sum(counts.values())
    counts['A'] += remainder          # give extra to A

    brand_a_revenue = 0.0

    for _ in range(MONTHS):
        # Revenue this month = customers with A * $100
        brand_a_revenue += counts['A'] * REVENUE_PER_CUST

        # Transition each customer stochastically
        new_counts = {b: 0 for b in BRANDS}
        for from_brand in BRANDS:
            n_customers = counts[from_brand]
            to_brands   = list(matrix[from_brand].keys())
            weights     = list(matrix[from_brand].values())
            # Vectorised multinomial draw for speed
            draws = np.random.multinomial(n_customers, weights)
            for i, to_brand in enumerate(to_brands):
                new_counts[to_brand] += draws[i]
        counts = new_counts

    return brand_a_revenue

# ── Task 3: Run 100 trials each ──────────────────────────────────────────────
print("Running 100 baseline trials...", flush=True)
baseline_revenues = [simulate_market(BASELINE) for _ in range(TRIALS)]

print("Running 100 campaign trials...", flush=True)
campaign_revenues = [simulate_market(CAMPAIGN) for _ in range(TRIALS)]

# Net campaign revenues (subtract cost)
campaign_net = [r - CAMPAIGN_COST for r in campaign_revenues]

# ── Visualise ────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

axes[0].hist(baseline_revenues, bins=25, color='steelblue', edgecolor='white', alpha=0.85)
axes[0].axvline(np.mean(baseline_revenues), color='red', linestyle='--', linewidth=1.5,
                label=f'Mean = ${np.mean(baseline_revenues):,.0f}')
axes[0].set_title('Baseline: Brand A Cumulative Revenue\n(100 trials, 24 months)')
axes[0].set_xlabel('Cumulative Revenue ($)')
axes[0].set_ylabel('Frequency')
axes[0].legend()

axes[1].hist(campaign_revenues, bins=25, color='seagreen', edgecolor='white', alpha=0.85)
axes[1].axvline(np.mean(campaign_revenues), color='red', linestyle='--', linewidth=1.5,
                label=f'Mean = ${np.mean(campaign_revenues):,.0f}')
axes[1].axvline(np.mean(baseline_revenues), color='steelblue', linestyle=':', linewidth=1.5,
                label=f'Baseline mean')
axes[1].set_title('With Campaign: Brand A Cumulative Revenue\n(before subtracting $50k cost)')
axes[1].set_xlabel('Cumulative Revenue ($)')
axes[1].set_ylabel('Frequency')
axes[1].legend()

plt.suptitle('Assignment 4 — Market Share Competition (100 Monte Carlo Trials)', fontsize=12)
plt.tight_layout()
plt.savefig('assignment4_market.png', dpi=150)
plt.show()

# ── Reflection helper numbers ────────────────────────────────────────────────
avg_baseline = np.mean(baseline_revenues)
avg_campaign = np.mean(campaign_revenues)
revenue_lift = avg_campaign - avg_baseline
net_gain     = revenue_lift - CAMPAIGN_COST

# Trials where campaign (net of cost) is WORSE than baseline
worse_trials = sum(1 for c, b in zip(campaign_net, baseline_revenues) if c < b)

print("\n" + "=" * 65)
print("ASSIGNMENT 4 — KEY NUMBERS FOR YOUR REFLECTION")
print("=" * 65)
print("\n--- Campaign Transition Matrix Used ---")
for brand in BRANDS:
    row = CAMPAIGN[brand]
    print(f"  From {brand}: A={row['A']:.2f}  B={row['B']:.2f}  C={row['C']:.2f}  (sum={sum(row.values()):.2f})")

print(f"\n--- Revenue Results (100 trials, 24 months) ---")
print(f"  Avg baseline revenue        : ${avg_baseline:>15,.2f}")
print(f"  Avg campaign revenue        : ${avg_campaign:>15,.2f}")
print(f"  Revenue lift                : ${revenue_lift:>15,.2f}")
print(f"  Campaign cost               : ${CAMPAIGN_COST:>15,.2f}")
print(f"  Net gain after cost         : ${net_gain:>15,.2f}")
print(f"  ROI > campaign cost?        : {'YES ✓' if net_gain > 0 else 'NO ✗'}")
print(f"\n  Trials where campaign (net) worse than baseline: {worse_trials} / {TRIALS}")
print(f"  P(campaign worse)           : {worse_trials/TRIALS*100:.1f}%")
print("=" * 65)
print("\nHistogram saved to: assignment4_market.png")
