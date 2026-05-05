# finance_tracker
Final Project for CS32

1. Personal expense tracker where users can log their purchases and spending
2. Graphs and visual summaries to show total spending, spending by category, and how often the user spends
3. Simple calculations such as average purchase price, number of purchases, and other spending statistics
4. Uses a JSON object to store transactions with a unique timestamp-based id, along with transaction data like user, amount, etc.
5. Multiple user support so different people can have their own accounts and expense records
6. Bill-splitting feature inspired by apps like Splitwise to divide shared expenses between users

SETUP
Requires Python 3.10+ and Flask. 
Install with: pip install flask

RUNNING
Put all project files in the same folder, nagivate to the root directory, and run: 
python3 app.py

Then open http://localhost:5000 in your browser (the link should also show up in your terminal)
Changes save automatically to data.json.
