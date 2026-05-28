import random
import matplotlib.pyplot as plt

# ── Parameters ───────────────────────────────────────────────────────────────
N_CUSTOMERS = 1_000
MONTHS      = 36
STATES      = ['Loyal', 'Occasional', 'Churned']

# Transition matrix  [from Loyal, from Occasional, from Churned]
# Each sub-list = [P(->Loyal), P(->Occasional), P(->Churned)]
TRANSITION = {
    'Loyal':      [0.70, 0.20, 0.10],
    'Occasional': [0.30, 0.40, 0.30],
    'Churned':    [0.10, 0.20, 0.70],
}

# ── Task 1: Implement Markov Model ───────────────────────────────────────────
def run_simulation(start_state: str = 'Loyal'):
    """
    Simulate N_CUSTOMERS over MONTHS months.
    Returns a dict of lists: monthly count for each state.
    """
    # Initialise all customers in start_state
    customer_states = [start_state] * N_CUSTOMERS

    history = {s: [] for s in STATES}

    for month in range(MONTHS):
        # ── Task 2: Track states each month ──────────────────────────────
        counts = {s: 0 for s in STATES}
        for state in customer_states:
            counts[state] += 1
        for s in STATES:
            history[s].append(counts[s])

        # Transition every customer to next state
        new_states = []
        for state in customer_states:
            probs     = TRANSITION[state]
            new_state = random.choices(STATES, weights=probs, k=1)[0]
            new_states.append(new_state)
        customer_states = new_states

    return history, customer_states  # final states = month 36

# ── Run simulation starting from 'Loyal' ─────────────────────────────────────
history, final_states = run_simulation(start_state='Loyal')

# ── Task 3: Visualise ────────────────────────────────────────────────────────
month_axis = list(range(1, MONTHS + 1))
colors     = {'Loyal': 'steelblue', 'Occasional': 'darkorange', 'Churned': 'tomato'}

plt.figure(figsize=(11, 6))
for state in STATES:
    plt.plot(month_axis, history[state], label=state, color=colors[state], linewidth=2)

plt.title('Customer State Distribution Over 36 Months (Markov Chain)\nStarting State: All Loyal', fontsize=13)
plt.xlabel('Month')
plt.ylabel('Number of Customers (out of 1,000)')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('assignment3_markov.png', dpi=150)
plt.show()

# ── Reflection helper numbers ────────────────────────────────────────────────
month36_counts = {s: history[s][-1] for s in STATES}  # index -1 = month 36

print("=" * 60)
print("ASSIGNMENT 3 — KEY NUMBERS FOR YOUR REFLECTION")
print("=" * 60)
print(f"\nCustomers at MONTH 36 (starting all Loyal):")
for s in STATES:
    print(f"  {s:<12}: {month36_counts[s]}")

# Estimate steady-state from last few months
print("\nAverage over last 6 months (≈ steady state):")
for s in STATES:
    avg = sum(history[s][-6:]) / 6
    print(f"  {s:<12}: {avg:.1f}")

# ── Optional: re-run starting from Churned to verify memoryless property ─────
print("\n" + "─" * 60)
print("Re-running with ALL customers starting as 'Churned'...")
history_c, _ = run_simulation(start_state='Churned')
print(f"\nCustomers at MONTH 36 (starting all Churned):")
for s in STATES:
    print(f"  {s:<12}: {history_c[s][-1]}")
print("\n(Compare with 'starting Loyal' — should be very similar at month 36)")
print("=" * 60)
print("\nLine graph saved to: assignment3_markov.png")
