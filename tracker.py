# tracker.py — Simple expense tracker that saves to a CSV file
# Run this file: python3 tracker.py

import csv       # for reading/writing CSV files
import datetime  # for getting today's date
import os        # for checking if a file exists


# --- SETTINGS ---

# name of the file where expenses are saved
CSV_FILE = "expenses.csv"

# list of categories the user can pick from
CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Bills", "Other"]


# --- HELPER FUNCTIONS ---

def get_amount():
    """Ask the user for a dollar amount and make sure it's a valid number."""
    while True:
        answer = input("How much did you spend? $")
        try:
            # try to turn their answer into a number
            amount = float(answer)
            if amount <= 0:
                print("Please enter a positive number.")
            else:
                return amount
        except ValueError:
            # they typed something that isn't a number
            print("That's not a valid number. Try again.")


def get_category():
    """Show a numbered list of categories and let the user pick one."""
    print("Pick a category:")
    # print each category with a number next to it
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {cat}")

    while True:
        answer = input("Enter the number: ")
        try:
            choice = int(answer)
            # make sure the number is in the valid range
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            else:
                print(f"Pick a number between 1 and {len(CATEGORIES)}.")
        except ValueError:
            print("That's not a valid number. Try again.")


def get_description():
    """Ask for a short description of the expense."""
    return input("Short description: ")


def get_date():
    """Ask for the date. If they press Enter, use today's date."""
    today = datetime.date.today().strftime("%m/%d/%Y")
    answer = input(f"Date (press Enter for today — {today}): ")

    # if they just pressed Enter, use today
    if answer.strip() == "":
        return today
    else:
        return answer.strip()


def get_split():
    """Ask who the expense was split with. Returns a list of names."""
    answer = input("Split with anyone? Enter names separated by commas (or press Enter to skip): ")

    # if they pressed Enter, no one to split with
    if answer.strip() == "":
        return []

    # split the names by comma and clean up extra spaces
    names = [name.strip() for name in answer.split(",")]
    return names


def calculate_per_person(amount, names):
    """Calculate how much each person owes (including you)."""
    # total people = you + everyone you listed
    total_people = len(names) + 1
    per_person = amount / total_people
    return round(per_person, 2)


def print_summary(date, amount, category, description, names, per_person):
    """Print a nice summary of the expense."""
    print("\n--- Expense Logged ---")
    print(f"  Date:        {date}")
    print(f"  Amount:      ${amount:.2f}")
    print(f"  Category:    {category}")
    print(f"  Description: {description}")

    # only show split info if there are other people
    if names:
        print(f"  Split with:  {', '.join(names)}")
        print(f"  Per person:  ${per_person:.2f} each ({len(names) + 1} people)")
    print("---------------------\n")


def save_to_csv(date, amount, category, description, names, per_person):
    """Save one row of expense data to the CSV file."""
    # check if the file already exists
    file_exists = os.path.exists(CSV_FILE)

    # open the file in "append" mode so we add to the end (not overwrite)
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        # if the file is brand new, write the header row first
        if not file_exists:
            writer.writerow(["Date", "Amount", "Category", "Description", "Split With", "Per Person"])

        # turn the list of names into a single string (e.g. "Alice; Bob")
        split_with = "; ".join(names) if names else ""

        # write the expense as one row
        writer.writerow([date, amount, category, description, split_with, per_person])


# --- MAIN PROGRAM ---

def main():
    """Main loop — ask for expenses until the user wants to stop."""
    print("=== Expense Tracker ===\n")

    while True:
        # ask all the questions
        amount = get_amount()
        category = get_category()
        description = get_description()
        date = get_date()
        names = get_split()

        # calculate split (if no names, per_person is just the full amount)
        if names:
            per_person = calculate_per_person(amount, names)
        else:
            per_person = amount

        # show the user what was logged
        print_summary(date, amount, category, description, names, per_person)

        # save it to the CSV file
        save_to_csv(date, amount, category, description, names, per_person)
        print(f"Saved to {CSV_FILE}!")

        # ask if they want to add another
        again = input("Add another expense? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break
        print()  # blank line before next expense


# this runs the main function when you execute the file
if __name__ == "__main__":
    main()