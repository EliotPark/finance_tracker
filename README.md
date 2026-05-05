# finance_tracker
Final Project for CS32

1. Personal expense tracker where users can log their purchases and spending
2. Graphs and visual summaries to show total spending, spending by category, and how often the user spends
3. Simple calculations such as average purchase price, number of purchases, and other spending statistics
4. Uses a JSON object to store transactions with a unique timestamp-based id, along with transaction data like user, amount, etc.
5. Multiple user support so different people can have their own accounts and expense records
6. Bill-splitting feature inspired by apps like Splitwise to divide shared expenses between users


## data.json structure

This is documented here (as part of the comments required for "documenting the project) instead of inside data.json itself because JSON does not allow comments.

The data structure in the data.json file has four top-level keys:

**users** - a flat list of name strings for everyone in the group. Every transaction and recurring rule references a name from this list.

**transactions** - every individual ledger entry across all users. Each entry has an id, date, user, desc, amount, cat (category), and type (either "expense" or "income"). Entries created automatically by the Bill Split tool also carry source: "splitwise" and a splitwiseId so they can be identified and regenerated without touching manually added transactions.

**expenses** - the shared bills added in the Bill Split tool. Each expense stores the full amount, who paid (payer), and the list of people splitting it (splitWith). These are the source of truth for bill splitting. Whenever the state is saved from billsplit.html, the splitwise entries in transactions are wiped and re-derived from this list.

**recurring** - rules for repeating payments. Each rule has a desc, amount, cat, type, freq (weekly / biweekly / monthly / yearly), startDate, and user. These are never added to transactions directly. Instead, tracker.html reads the rules at render time and projects future occurrences for the next 6 months without writing anything back to the file.
SETUP
Requires Python 3.10+ and Flask. 
Install with: pip install flask


# Running the program

Put all project files in the same folder, nagivate to the root directory, and run: 
python3 app.py

Then open http://localhost:5000 in your browser (the link should also show up in your terminal)
Changes save automatically to data.json.

# Credits

We used several AI and online tools throughout this project.
For the frontend design, we used Lovable.ai to generate the initial CSS stylesheet, which gave us the dark theme, color scheme, typography, and overall visual layout of the site. We then made manual adjustments to fit our specific pages and components.
For the backend, we referenced the official Flask documentation (https://flask.palletsprojects.com/en/stable/installation/) to set up the server and learn how to serve static files, and a Medium article on Flask's jsonify method to understand how to send JSON responses from our API endpoints. (https://medium.com/@sujathamudadla1213/jsonify-method-in-flask-ecfa5e483c29). In addition to this, when faced with errors we referenced Stackoverflow, GeeksforGeeks, and ChatGPT to help us debug.
Finally, We used Claude to build the HTML pie charts and line charts on the Analytics page, including the Chart.js configuration and the logic that processes transaction data into chart-ready formats. We also used Claude to write the code in app.py that connects our backend Python logic (the tracker and bill split algorithms that we wrote) to the HTML frontend — specifically the two /api/state endpoints that let the browser read and write data.json.

IMPORTANT ADDITION!!
One thing I forgot to include in the video: We initially tried to deploy the website using github pages and host it non-locally but found that we weren't able to update the json database. This meant that every time we refreshed with cmd+shift+R, all of the data would be erased, rendering the website useless. Thats why we switched to a Flask API and localhost. Before doing this, we didnt need any of the code in app.py, simply the HTML pages and the code in tracker and splitwise.py.
