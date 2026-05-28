import numpy as np
import matplotlib.pyplot as plt

# ── Parameters ──────────────────────────────────────────────────────────────
LAMBDA         = 15          # Poisson average daily demand
DAYS           = 30
SELL_PRICE     = 50          # $ per unit sold
UNIT_COST      = 30          # $ per unit purchased upfront
SALVAGE_VALUE  = 10          # $ per leftover unit
TRIALS         = 10_000
STOCK_LEVELS   = [300, 450, 600]

# ── Task 1: Simulation function ──────────────────────────────────────────────
def simulate_profit(initial_stock: int) -> float:
    """Simulate a 30-day sales period and return total profit."""
    stock = initial_stock
    units_sold = 0

    for _ in range(DAYS):
        daily_demand = np.random.poisson(LAMBDA)
        sold_today   = min(daily_demand, stock)
        units_sold  += sold_today
        stock        = max(0, stock - daily_demand)

    leftover = stock
    profit   = (units_sold * SELL_PRICE) + (leftover * SALVAGE_VALUE) - (initial_stock * UNIT_COST)
    return profit

# ── Task 2: Evaluate each stocking level ────────────────────────────────────
results = {}  # stock_level -> list of profits

for level in STOCK_LEVELS:
    profits = [simulate_profit(level) for _ in range(TRIALS)]
    results[level] = profits

# ── Visualise ────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)
colors = ['steelblue', 'darkorange', 'seagreen']

for ax, level, color in zip(axes, STOCK_LEVELS, colors):
    ax.hist(results[level], bins=60, color=color, edgecolor='white', alpha=0.85)
    ax.axvline(np.mean(results[level]), color='red', linestyle='--',
               linewidth=1.5, label=f'Mean = ${np.mean(results[level]):,.0f}')
    ax.set_title(f'Stock Level = {level} units')
    ax.set_xlabel('Profit ($)')
    ax.set_ylabel('Frequency')
    ax.legend(fontsize=8)

plt.suptitle('Assignment 2 — Profit Distribution by Stocking Level (10,000 Trials)', fontsize=13)
plt.tight_layout()
plt.savefig('assignment2_inventory.png', dpi=150)
plt.show()

# ── Reflection helper numbers ────────────────────────────────────────────────
print("=" * 60)
print("ASSIGNMENT 2 — KEY NUMBERS FOR YOUR REFLECTION")
print("=" * 60)
for level in STOCK_LEVELS:
    p       = results[level]
    avg     = np.mean(p)
    min_val = np.min(p)
    max_val = np.max(p)
    pct5    = np.percentile(p, 5)
    print(f"\nStock Level: {level} units")
    print(f"  Average profit  : ${avg:,.2f}")
    print(f"  Min profit      : ${min_val:,.2f}")
    print(f"  Max profit      : ${max_val:,.2f}")
    print(f"  5th percentile  : ${pct5:,.2f}")
    print(f"  P(loss)         : {sum(1 for x in p if x < 0)/TRIALS*100:.1f}%")

best_level = max(STOCK_LEVELS, key=lambda lvl: np.mean(results[lvl]))
print(f"\nHighest average profit stocking level: {best_level} units")
print("=" * 60)
print("\nHistogram saved to: assignment2_inventory.png")
