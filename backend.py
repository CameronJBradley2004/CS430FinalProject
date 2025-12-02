#import Flask, request, and jsonify
from flask import Flask, make_response, request, jsonify
import pymssql
from sqlalchemy import create_engine
from sqlalchemy import URL
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import secrets
from datetime import timedelta
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def process():
	data = request.get_json()

	#Pull JSON data into username and password variable
	username = data.get('username')
	password = data.get('password')

	if not username or not password:
		return jsonify({"status": "error", "message": "Email or password missing"}), 400

	#Hash the password
	password_hash = hashlib.sha256(password.encode()).hexdigest()

	#Connect to the database
	conn = pymssql.connect(
		server='192.168.10.132',
		user='SA',
		password='Password1234!@#$',
		database='Spending',
		port=1433
	)

	cursor = conn.cursor()

	cursor.execute("UPDATE Credentials SET [PasswordHash]=%s WHERE UserID=24", (password_hash, username))
	conn.commit()
	#Check the password has using the username as the key
	cursor.execute("SELECT [PasswordHash] FROM Credentials c JOIN [Users] u ON c.UserID = u.UserID WHERE u.Username=%s", (username,))
	row = cursor.fetchone()
	db_hash = row[0]
	if db_hash == password_hash:
		UserID = 24
		token = secrets.token_hex(16)
		cursor.execute("UPDATE Credentials SET [Token]=%s WHERE UserID=24", (token))


		data = {"status": "success", "message": "successful login"}
		response = make_response(jsonify(data))
		response.set_cookie('sharktowels_auth_token', token, httponly=True, secure=True, max_age=timedelta(days=1), samesite='None')
		conn.close()
		return response
	else:
		conn.close()
		return jsonify({"status": "error", "message": "Invalid Password"}), 401
	#If successful
	#then see if api token is empty
	#	if yes; generate a new one and fill the database with it and put it into variable
	# 	if no; grab the one out of the database and put into variable

	#return variableS

@app.route('/tables', methods=['POST'])
def tables():
	data = request.get_json()
	token = request.cookies.get("sharktowels_auth_token")

	conn_string = URL.create(
		"mssql+pyodbc",
		username= 'SA',
		password= 'Password1234!@#$',
		host= '192.168.10.132',
		port= 1433,
		database = 'Spending',
		query = {
			"driver":"ODBC Driver 18 for SQL Server",
			"TrustServerCertificate":"yes",
			}
		)

	conn = create_engine(conn_string)

	pie_df = pd.read_sql_query(f'''
				SELECT Purchases.Category, Purchases.Subcategory, Payments.Amount
				FROM Purchases
				JOIN Payments ON Purchases.PaymentID = Payments.PaymentID
				WHERE UserID = 24
				ORDER BY Purchases.TimeDate
				''', conn)

	#Last chart
	category_bar_df = pd.read_sql_query(f'''
		SELECT Purchases.Category, Purchases.Subcategory, Payments.Amount
		FROM Purchases
		JOIN Payments ON Purchases.PaymentID = Payments.PaymentID
		WHERE Purchases.UserID = 24
		ORDER BY Purchases.Category
		''', conn)

	fig1 = px.bar(category_bar_df, x = "Category", y = "Amount", color = "Subcategory", title = "Spending per Category")
	#Second to last chart

	grouped_amount = pie_df.groupby(["Category", "Subcategory"])["Amount"].sum().reset_index(name="total")

	categories = grouped_amount["Category"].unique()

	fig2 = go.Figure()

	for i, category in enumerate(categories):
		category_df = grouped_amount[grouped_amount["Category"] == category]

		fig2.add_trace(

		go.Pie(
			labels = category_df["Subcategory"],
			values = category_df["total"],
			name = category,
			visible = (i == 0),
			hovertemplate = "%{label}: $%{value}<extra></extra>"
		)

	)

	fig2.update_layout(

	updatemenus=[

		dict(
			buttons = [
				dict(
					label = category,
					method = "update",
					args = [
						{"visible": [j == i for j in range(len(categories))]},
						{"title": f"Number of Purchases in: {category}"}
					]
				)
			for i, category in enumerate(categories)
			],
			direction = "down",
			x = 1,
			y = 1,
			)

	],
	title = f"Cost Breakdown of Purchases in: {categories[0]}"
	)
	# First Graph
	area_df = pd.read_sql_query(f'''
		SELECT Purchases.TimeDate, Purchases.Category, Purchases.Subcategory, Payments.Amount 
		FROM Purchases
		JOIN Payments ON Purchases.PaymentID = Payments.PaymentID
		WHERE UserID = 24
		ORDER BY Purchases.TimeDate
	''', conn)

	area_df["runningAmount"] = area_df.sort_values("TimeDate") \
		.groupby("Category")["Amount"] \
		.cumsum()

	pivoted_area_df = area_df.pivot_table(
		index="TimeDate",
		columns="Category",
		values="runningAmount",
		aggfunc="last"
	)

	pivoted_area_df = pivoted_area_df.ffill()

	pivoted_area_df.head()

	fig3 = go.Figure()

	for category in pivoted_area_df.columns:
		fig3.add_trace(
		go.Scatter(
			x=pivoted_area_df.index,
			y=pivoted_area_df[category],
			mode="lines",
			stackgroup="one",
			name=category
		)
		)

	fig3.update_layout(
		title="Cumulative Spending By Category",
		xaxis_title="Time",
		yaxis_title="Running Amount",
		hovermode="x unified",
			xaxis=dict(
				rangeselector=dict(
					buttons=list([
						dict(count=1,
							label="1m",
							step="month",
							stepmode="backward"),
						dict(count=6,
							label="6m",
							step="month",
							stepmode="backward"),
						dict(count=1,
							label="YTD",
							step="year",
							stepmode="todate"),
						dict(count=1,
							label="1y",
							step="year",
							stepmode="backward"),
						dict(step="all")
					])
				),
			)
	)
	# Second Graph

	pie_df.head()

	categories = pie_df['Category'].unique()
	subcategories = pie_df['Subcategory'].unique()

	grouped_count = pie_df.groupby(["Category", "Subcategory"]).size().reset_index(name="count")

	categories = grouped_count["Category"].unique()

	fig4 = go.Figure()

	for i, category in enumerate(categories):
		category_df = grouped_count[grouped_count["Category"] == category]

		fig4.add_trace(

			go.Pie(
				labels = category_df["Subcategory"],
				values = category_df["count"],
				name = category,
				visible = (i == 0),
				hovertemplate = "%{label}, %{value}<extra></extra>"
			)

		)

	fig4.update_layout(

		updatemenus=[

			dict(
				buttons = [
					dict(
						label = category,
						method = "update",
						args = [
							{"visible": [j == i for j in range(len(categories))]},
							{"title": f"Number of Purchases in: {category}"}
						]
					)
			for i, category in enumerate(categories)
		],
		direction = "down",
		x = 1,
		y = 1,
	)

		],
	title = f"Number of Purchases in: {categories[0]}"
	)

	return jsonify({
	"plot1": fig1.to_json(),
	"plot2": fig2.to_json(),
	"plot3": fig3.to_json(),
	"plot4": fig4.to_json()
	})

if __name__ == '__main__':
	app.run(debug=True)
