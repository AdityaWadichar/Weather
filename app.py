import requests
import sqlite3 as sql
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key='Very secrete'


@app.route('/', methods=['GET', 'POST'])
def index():
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
	if request.method == 'POST':
		new_city = request.form.get('city')
		if new_city:
			r = requests.get(url.format(new_city)).json()
			if not r['cod']=='404':
				with sql.connect("database.db") as con:
					cur=con.cursor()
					cur.execute("INSERT INTO Cities (name) VALUES (?)",[new_city])
					con.commit()
			else:
				flash("City not found")
	
	with sql.connect("database.db") as con:
		cur=con.cursor()
		cur.execute("SELECT * FROM CITIES")
		cities = cur.fetchall()

	
	weather_data = []

	for city in cities:

		r = requests.get(url.format(city[0])).json()
		print(r['cod'])
		weather = {
			'city' : city[0],
			'temperature' : r['main']['temp'],
			'description' : r['weather'][0]['description'],
			'icon' : r['weather'][0]['icon'],
		}

		weather_data.append(weather)


	return render_template('weather.html', weather_data=weather_data)

@app.route('/del')
def delete():
	with sql.connect("database.db") as con:
		cur=con.cursor()
		cur.execute("DELETE FROM CITIES")
	return redirect(url_for('index')) 


if __name__ == '__main__':
   app.run(debug = True)
