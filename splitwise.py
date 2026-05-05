import json
import os
import datetime

DATA_FILE  = "data.json"
CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Travel", "Other"]


def load():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "expenses": []}
    with open(DATA_FILE) as f:
        return json.load(f)

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def calc_settlements(data):
    bal = {u: 0.0 for u in data["users"]}

    # Build a net balance for each person. Positive means someone is owed money,
    # negative means they owe money. The payer is skipped because they already covered their share.
    for ex in data["expenses"]:
        n = len(ex["split_with"])
        if n == 0:
            continue
        share = ex["amount"] / n
        for person in ex["split_with"]:
            if person == ex["payer"]:
                continue
            bal[ex["payer"]] += share
            bal[person]      -= share

    creditors = sorted(
        [{"name": k, "amount":  round(v, 2)} for k, v in bal.items() if v >  0.005],
        key=lambda x: -x["amount"]
    )
    debtors = sorted(
        [{"name": k, "amount": -round(v, 2)} for k, v in bal.items() if v < -0.005],
        key=lambda x: -x["amount"]
    )

    # Greedy matching: pair the biggest creditor with the biggest debtor each round.
    # This minimizes the total number of payments needed to settle everyone up.
    settlements = []
    while creditors and debtors:
        cr, db = creditors[0], debtors[0]
        amt = round(min(cr["amount"], db["amount"]), 2)
        if amt > 0.005:
            settlements.append({"from": db["name"], "to": cr["name"], "amount": amt})
        cr["amount"] = round(cr["amount"] - amt, 2)
        db["amount"] = round(db["amount"] - amt, 2)
        if cr["amount"] < 0.005:
            creditors.pop(0)
        if db["amount"] < 0.005:
            debtors.pop(0)

    return settlements

def pick(prompt, options):
    for i, o in enumerate(options, 1):
        print(f"  {i}. {o}")
    while True:
        raw = input(prompt)
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print(f"Enter a number between 1 and {len(options)}.")

def pick_people(prompt, users, required=None):
    """Let the user select a subset of people. required is always included."""
    print(prompt)
    for i, u in enumerate(users, 1):
        tag = " (payer — always included)" if u == required else ""
        print(f"  {i}. {u}{tag}")
    raw = input("Enter numbers separated by commas (or press Enter for everyone): ").strip()
    if not raw:
        return list(users)
    chosen = []
    for part in raw.split(","):
        try:
            idx = int(part.strip()) - 1
            if 0 <= idx < len(users):
                chosen.append(users[idx])
        except ValueError:
            pass
    if required and required not in chosen:
        chosen.append(required)
    return chosen if chosen else list(users)

def cmd_add_user(data):
    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    if name in data["users"]:
        print(f'"{name}" is already in the group.')
        return
    data["users"].append(name)
    save(data)
    print(f'Added "{name}".')

def cmd_add_expense(data):
    if len(data["users"]) < 2:
        print("Add at least 2 people first.")
        return

    print("\nWho paid?")
    payer = pick("Enter number: ", data["users"])

    raw_date = input(f"Date (YYYY-MM-DD, Enter = today): ").strip()
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
    cat = pick("Enter number: ", CATEGORIES)

    split_with = pick_people(
        "\nWho is splitting this expense?",
        data["users"],
        required=payer
    )

    # Note: this script uses "split_with" (snake_case) but the web frontend uses "splitWith" (camelCase).
    # Expenses added here will not be recognized by billsplit.html and vice versa.
    expense = {
        "id": str(int(datetime.datetime.now().timestamp() * 1000)),
        "date": date,
        "payer": payer,
        "desc": desc,
        "amount": round(amount, 2),
        "cat": cat,
        "split_with": split_with,
    }
    data["expenses"].append(expense)
    save(data)

    per = round(amount / len(split_with), 2)
    print(f'\nAdded: {desc} — ${amount:.2f} paid by {payer}, split {len(split_with)} ways (${per:.2f} each).')


def cmd_show_expenses(data):
    if not data["expenses"]:
        print("No expenses recorded.")
        return
    print(f"\n{'Date':<12} {'Payer':<12} {'Amount':>8}  {'Category':<14} Description")
    print("─" * 70)
    for ex in sorted(data["expenses"], key=lambda x: x["date"], reverse=True):
        print(f"{ex['date']:<12} {ex['payer']:<12} ${ex['amount']:>7.2f}  {ex['cat']:<14} {ex['desc']}")


def cmd_show_settlements(data):
    settlements = calc_settlements(data)
    if not settlements:
        print("All settled up!" if data["expenses"] else "No expenses yet.")
        return
    print(f"\n{'Optimized settlements (' + str(len(settlements)) + ' transaction' + ('' if len(settlements)==1 else 's') + ')':}")
    print("─" * 40)
    for s in settlements:
        print(f"  {s['from']} → pays → {s['to']}   ${s['amount']:.2f}")

def cmd_show_users(data):
    if not data["users"]:
        print("No people in the group.")
    else:
        print("People: " + ", ".join(data["users"]))

def cmd_clear(data):
    confirm = input("Clear ALL data? This cannot be undone. (yes/no): ").strip().lower()
    if confirm == "yes":
        data["users"].clear()
        data["expenses"].clear()
        save(data)
        print("Cleared.")
    else:
        print("Cancelled.")

MENU = [
    ("Add person", cmd_add_user),
    ("Add expense", cmd_add_expense),
    ("Show expenses", cmd_show_expenses),
    ("Show settlements", cmd_show_settlements),
    ("Show people", cmd_show_users),
    ("Clear all data", cmd_clear),
    ("Quit", None),
]

def main():
    # Load the shared data.json once at startup, then pass it into each command.
    # Every command that changes data calls save() itself before returning.
    print("=== Bill Split (Splitwise-style) ===\n")
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
