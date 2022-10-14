import requests
from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		new_city = request.form.get('city')
		if new_city:
			with sql.connect("database.db") as con:
				cur=con.cursor()
				cur.execute("INSERT INTO Cities (name) VALUES (?)",[new_city])
				con.commit()
	
	with sql.connect("database.db") as con:
		cur=con.cursor()
		cur.execute("SELECT * FROM CITIES")
		cities = cur.fetchall()

	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

	weather_data = []

	for city in cities:

		r = requests.get(url.format(city[0])).json()
		#print(r)

		weather = {
			'city' : city[0],
			'temperature' : r['main']['temp'],
			'description' : r['weather'][0]['description'],
			'icon' : r['weather'][0]['icon'],
		}

		weather_data.append(weather)


	return render_template('weather.html', weather_data=weather_data)


if __name__ == '__main__':
   app.run(debug = True)