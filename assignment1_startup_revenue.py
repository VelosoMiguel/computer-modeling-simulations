import random
import matplotlib.pyplot as plt
import statistics

# ── Parameters ──────────────────────────────────────────────────────────────
MEAN_NEW_CUSTOMERS = 100          # mean of Normal distribution
STD_NEW_CUSTOMERS  = 20           # standard deviation
CHURN_MIN          = 0.05         # uniform churn lower bound
CHURN_MAX          = 0.15         # uniform churn upper bound
PRICE_PER_CUSTOMER = 50           # $ per customer per month
OPERATING_COST     = 8000         # $ per month
MONTHS             = 12
TRIALS             = 10_000
STARTING_CUSTOMERS = 0            # Month 0 starts with 0 customers

# ── Task 1 & 2: Simulation wrapped in 10,000-trial loop ─────────────────────
yearly_profits = []

for _ in range(TRIALS):
    customers     = STARTING_CUSTOMERS
    yearly_profit = 0.0

    for month in range(MONTHS):
        # Draw new customers (cannot be negative)
        new_customers = max(0, random.gauss(MEAN_NEW_CUSTOMERS, STD_NEW_CUSTOMERS))
        churn_rate    = random.uniform(CHURN_MIN, CHURN_MAX)

        customers     = (customers + new_customers) * (1 - churn_rate)
        customers     = max(0, customers)                     # safety floor

        monthly_profit = (customers * PRICE_PER_CUSTOMER) - OPERATING_COST
        yearly_profit += monthly_profit

    yearly_profits.append(yearly_profit)

# ── Task 3: Visualise distribution ──────────────────────────────────────────
plt.figure(figsize=(10, 6))
plt.hist(yearly_profits, bins=80, color='steelblue', edgecolor='white', alpha=0.85)
plt.axvline(0, color='red', linestyle='--', linewidth=1.5, label='Break-even ($0)')
plt.axvline(statistics.mean(yearly_profits), color='orange', linestyle='-',
            linewidth=1.5, label=f'Mean = ${statistics.mean(yearly_profits):,.0f}')
plt.title('Distribution of Yearly Profit Across 10,000 Monte Carlo Trials', fontsize=14)
plt.xlabel('Total Yearly Profit ($)')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig('assignment1_histogram.png', dpi=150)
plt.show()

# ── Reflection helper numbers (print so you can reference them in your write-up) ──
profitable_trials = sum(1 for p in yearly_profits if p > 0)
probability_profit = profitable_trials / TRIALS

sorted_profits   = sorted(yearly_profits)
percentile_5_idx = int(0.05 * TRIALS) - 1          # 0-indexed position of 5th percentile
value_at_5th     = sorted_profits[percentile_5_idx]

mean_profit   = statistics.mean(yearly_profits)
median_profit = statistics.median(yearly_profits)
stdev_profit  = statistics.stdev(yearly_profits)

print("=" * 60)
print("ASSIGNMENT 1 — KEY NUMBERS FOR YOUR REFLECTION")
print("=" * 60)
print(f"Total trials          : {TRIALS:,}")
print(f"Profitable trials     : {profitable_trials:,}")
print(f"P(profit > 0)         : {profitable_trials} / {TRIALS} = {probability_profit:.4f}  ({probability_profit*100:.2f}%)")
print(f"\n5th-percentile index  : position {percentile_5_idx + 1} (1-based)")
print(f"5th-percentile value  : ${value_at_5th:,.2f}")
print(f"\nMean yearly profit    : ${mean_profit:,.2f}")
print(f"Median yearly profit  : ${median_profit:,.2f}")
print(f"Std dev               : ${stdev_profit:,.2f}")
print(f"Min outcome           : ${sorted_profits[0]:,.2f}")
print(f"Max outcome           : ${sorted_profits[-1]:,.2f}")
print("=" * 60)
print("\nHistogram saved to: assignment1_histogram.png")
