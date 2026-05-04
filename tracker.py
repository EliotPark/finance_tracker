# tracker.py — Personal expense & income tracker (CLI)
# Shares data with splitwise.py via the same JSON file.
# Run: python3 tracker.py

import json
import os
import datetime

DATA_FILE  = "splitwise_data.json"
CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Travel", "Other"]


# ── Data layer ────────────────────────────────────────────────────────────────

def load():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "expenses": [], "transactions": []}
    with open(DATA_FILE) as f:
        data = json.load(f)
    if "transactions" not in data:
        data["transactions"] = []
    return data


def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Balance helpers ───────────────────────────────────────────────────────────

def compute_balance(data, user):
    bal = 0.0
    for t in data["transactions"]:
        if t["user"] != user:
            continue
        if t["type"] == "income":
            bal += t["amount"]
        else:
            bal -= t["amount"]
    return round(bal, 2)


def user_transactions(data, user):
    return sorted(
        [t for t in data["transactions"] if t["user"] == user],
        key=lambda t: (t["date"], t["id"]),
    )


# ── Display helpers ───────────────────────────────────────────────────────────

def print_balance(data, user):
    bal = compute_balance(data, user)
    sign = "+" if bal >= 0 else "-"
    color = "\033[92m" if bal >= 0 else "\033[91m"  # green / red
    reset = "\033[0m"
    print(f"\n  Balance for {user}: {color}{sign}${abs(bal):.2f}{reset}\n")


def print_statement(data, user):
    txns = user_transactions(data, user)
    if not txns:
        print("  No transactions yet.")
        return

    print(f"\n  {'Date':<12} {'Type':<8} {'Category':<16} {'Amount':>10}  {'Balance':>10}  Description")
    print("  " + "─" * 78)

    running = 0.0
    for t in txns:
        if t["type"] == "income":
            running += t["amount"]
            delta  = f"+${t['amount']:.2f}"
            color  = "\033[92m"
        else:
            running -= t["amount"]
            delta  = f"-${t['amount']:.2f}"
            color  = "\033[91m"
        reset = "\033[0m"
        bal_str = f"${running:.2f}"
        print(f"  {t['date']:<12} {t['type']:<8} {t.get('cat','Income'):<16} "
              f"{color}{delta:>10}{reset}  {bal_str:>10}  {t['desc']}")

    # Summary line
    income  = sum(t["amount"] for t in txns if t["type"] == "income")
    expense = sum(t["amount"] for t in txns if t["type"] == "expense")
    print("  " + "─" * 78)
    print(f"  {'':12} {'':8} {'':16} {'Income:':>10}  \033[92m${income:.2f}\033[0m")
    print(f"  {'':12} {'':8} {'':16} {'Spent:':>10}  \033[91m${expense:.2f}\033[0m")
    print(f"  {'':12} {'':8} {'':16} {'Balance:':>10}  ${income-expense:.2f}\n")


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_view_statement(data):
    if not data["users"]:
        print("No users yet. Add a user first (from Bill Split menu or add one here).")
        return
    print("\nSelect user:")
    for i, u in enumerate(data["users"], 1):
        print(f"  {i}. {u}")
    try:
        idx = int(input("Enter number: ")) - 1
        user = data["users"][idx]
    except (ValueError, IndexError):
        print("Invalid choice."); return

    print_balance(data, user)
    print_statement(data, user)


def cmd_add_expense(data):
    if not data["users"]:
        print("No users yet."); return

    print("\nSelect user:")
    for i, u in enumerate(data["users"], 1):
        print(f"  {i}. {u}")
    try:
        idx  = int(input("Enter number: ")) - 1
        user = data["users"][idx]
    except (ValueError, IndexError):
        print("Invalid choice."); return

    raw_date = input("Date (YYYY-MM-DD, Enter = today): ").strip()
    date = raw_date if raw_date else datetime.date.today().isoformat()

    desc = input("Description: ").strip() or "Expense"

    while True:
        try:
            amount = float(input("Amount ($): "))
            if amount > 0:
                break
        except ValueError:
            pass
        print("Enter a positive number.")

    print("Category:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"  {i}. {c}")
    while True:
        try:
            idx = int(input("Enter number: ")) - 1
            if 0 <= idx < len(CATEGORIES):
                cat = CATEGORIES[idx]
                break
        except ValueError:
            pass
        print("Invalid choice.")

    data["transactions"].append({
        "id":     str(int(datetime.datetime.now().timestamp() * 1000)),
        "date":   date,
        "user":   user,
        "desc":   desc,
        "amount": round(amount, 2),
        "cat":    cat,
        "type":   "expense",
    })
    save(data)
    print(f'\nAdded expense: {desc} — -${amount:.2f} for {user}.')
    print_balance(data, user)


def cmd_add_income(data):
    if not data["users"]:
        print("No users yet."); return

    print("\nSelect user:")
    for i, u in enumerate(data["users"], 1):
        print(f"  {i}. {u}")
    try:
        idx  = int(input("Enter number: ")) - 1
        user = data["users"][idx]
    except (ValueError, IndexError):
        print("Invalid choice."); return

    raw_date = input("Date (YYYY-MM-DD, Enter = today): ").strip()
    date = raw_date if raw_date else datetime.date.today().isoformat()

    desc = input("Description (e.g. Paycheck): ").strip() or "Income"

    while True:
        try:
            amount = float(input("Amount ($): "))
            if amount > 0:
                break
        except ValueError:
            pass
        print("Enter a positive number.")

    data["transactions"].append({
        "id":     str(int(datetime.datetime.now().timestamp() * 1000)),
        "date":   date,
        "user":   user,
        "desc":   desc,
        "amount": round(amount, 2),
        "cat":    "Income",
        "type":   "income",
    })
    save(data)
    print(f'\nAdded income: {desc} — +${amount:.2f} for {user}.')
    print_balance(data, user)


def cmd_add_user(data):
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty."); return
    if name in data["users"]:
        print(f'"{name}" already exists.'); return
    data["users"].append(name)
    save(data)
    print(f'Added "{name}".')


def cmd_all_balances(data):
    if not data["users"]:
        print("No users yet."); return
    print()
    for user in data["users"]:
        bal  = compute_balance(data, user)
        sign = "+" if bal >= 0 else "-"
        color = "\033[92m" if bal >= 0 else "\033[91m"
        reset = "\033[0m"
        print(f"  {user:<20} {color}{sign}${abs(bal):.2f}{reset}")
    print()


# ── Main loop ─────────────────────────────────────────────────────────────────

MENU = [
    ("View statement (bank view)",  cmd_view_statement),
    ("Add expense",                 cmd_add_expense),
    ("Add income / paycheck",       cmd_add_income),
    ("View all balances",           cmd_all_balances),
    ("Add user",                    cmd_add_user),
    ("Quit",                        None),
]


def main():
    print("=== Personal Tracker ===\n")
    data = load()
    while True:
        print()
        for i, (label, _) in enumerate(MENU, 1):
            print(f"  {i}. {label}")
        choice = input("\nChoose: ").strip()
        try:
            idx = int(choice) - 1
            label, fn = MENU[idx]
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue
        if fn is None:
            print("Goodbye!")
            break
        print(f"\n── {label} ──")
        fn(data)


if __name__ == "__main__":
    main()
