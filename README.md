# finance_tracker
Final Project for CS32

1. Personal expense tracker where users can log their purchases and spending
2. Graphs and visual summaries to show total spending, spending by category, and how often the user spends
3. Simple calculations such as average purchase price, number of purchases, and other spending statistics
4. Use of dictionaries and a database/file system to store and organize expense data
5. Multiple user support so different people can have their own accounts and expense records
6. Bill-splitting feature inspired by apps like Splitwise to divide shared expenses between users

4/8/26 - Eliot
- Added bare bones framework for website with a landing page and two subpages (one for billsplit and one for trackers)
- New idea - Auto sort transactions into categories using huge hard coded lists of food spots, clothing stores, etc. If none match, give the user to select given a drop down menu.

## data.json structure

This is documented here (as part of the comments required for "documenting the project) instead of inside data.json itself because JSON does not allow comments.

The data structure in the data.json file has four top-level keys:

**users** - a flat list of name strings for everyone in the group. Every transaction and recurring rule references a name from this list.

**transactions** - every individual ledger entry across all users. Each entry has an id, date, user, desc, amount, cat (category), and type (either "expense" or "income"). Entries created automatically by the Bill Split tool also carry source: "splitwise" and a splitwiseId so they can be identified and regenerated without touching manually added transactions.

**expenses** - the shared bills added in the Bill Split tool. Each expense stores the full amount, who paid (payer), and the list of people splitting it (splitWith). These are the source of truth for bill splitting. Whenever the state is saved from billsplit.html, the splitwise entries in transactions are wiped and re-derived from this list.

**recurring** - rules for repeating payments. Each rule has a desc, amount, cat, type, freq (weekly / biweekly / monthly / yearly), startDate, and user. These are never added to transactions directly. Instead, tracker.html reads the rules at render time and projects future occurrences for the next 6 months without writing anything back to the file.
