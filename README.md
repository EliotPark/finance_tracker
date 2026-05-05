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

CREDITS

We used several AI and online tools throughout this project.
For the frontend design, we used Lovable.ai to generate the initial CSS stylesheet, which gave us the dark theme, color scheme, typography, and overall visual layout of the site. We then made manual adjustments to fit our specific pages and components.
For the backend, we referenced the official Flask documentation (https://flask.palletsprojects.com/en/stable/installation/) to set up the server and learn how to serve static files, and a Medium article on Flask's jsonify method to understand how to send JSON responses from our API endpoints. (https://medium.com/@sujathamudadla1213/jsonify-method-in-flask-ecfa5e483c29). In addition to this, when faced with errors we referenced Stackoverflow, GeeksforGeeks, and ChatGPT to help us debug.
Finally, We used Claude to build the HTML pie charts and line charts on the Analytics page, including the Chart.js configuration and the logic that processes transaction data into chart-ready formats. We also used Claude to write the code in app.py that connects our backend Python logic (the tracker and bill split algorithms that we wrote) to the HTML frontend — specifically the two /api/state endpoints that let the browser read and write data.json.
