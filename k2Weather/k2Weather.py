import requests
import json
import sqlite3
import time 
from datetime import datetime



conn = sqlite3.connect('k2Weather.db')
print ("Opened database successfully")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS weather 
                    (ID INT PRIMARY KEY NOT NULL, 
                    currentTemp REAL NOT NULL, 
                    feelsTemp REAL NOT NULL, 
                    pressure INT NOT NULL, 
                    humidity INT NOT NULL, 
                    windSpeed REAL NOT NULL, 
                    visibility INT NOT NULL, 
                    cloud INT NOT NULL);''')



#static data
api_key = "d17d76775a861e9745db37876ac26391"
lat = "35.88"
lon = "76.51"



class accWeather:
    def __init__(self):
        self.current_temp = -1
        self.feels_temp = -1
        self.pressure = -1
        self.humidity = -1
        self.wind_speed = -1
        self.visibility = -1
        self.cloud = -1


    def read_acctual_weather(self):
        urlWeather = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&APPID=%s&units=metric" % (lat, lon, api_key)
        response = requests.get(urlWeather)
        data = json.loads(response.text)
        
        data_main = data["main"]
        self.current_temp = data_main["temp"]
        self.feels_temp = data_main["feels_like"]
        self.pressure = data_main["pressure"]
        self.humidity = data_main["humidity"]
        self.wind_speed = data["wind"]["speed"]
        self.visibility = data["visibility"]
        self.clouds = data["clouds"]["all"]
        
        

    def write_acctual_weather(self):
        print('Current temp: ' + str(self.current_temp) + "\N{DEGREE SIGN}C")
        print('Sensed temperature: ' + str(self.feels_temp) + '\N{DEGREE SIGN}C')
        print('Current pressure: ' + str(self.pressure) + 'hPa')
        print('Humidity: ' + str(self.humidity) + '%')
        print('Range of visibility: ' + str(self.visibility) + 'm')
        print('Wind speed: ' + str(self.wind_speed) + 'm/s')
        print('Cloudy: ' + str(self.clouds) + '%')
        idData = int(datetime.now().strftime("%Y%m%d%H%M"))
        sql = 'INSERT INTO weather VALUES (%d,%f,%f,%d,%d,%f,%d,%d);' % (idData,self.current_temp,self.feels_temp,self.pressure,self.humidity,self.wind_speed,self.visibility,self.clouds)
        c.execute(sql)
        conn.commit()

#actual forecast
urlForecast = "http://api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&APPID=%s&units=metric" % (lat, lon, api_key)
response = requests.get(urlForecast)
data = json.loads(response.text)
#print(data)

def main():
    x = datetime.now()
    while True:
        start = time.time()
        if (x.minute != datetime.now().minute):
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print("Day and Time of mesure:", dt_string)	
            accWeatherTemp = accWeather()
            accWeatherTemp.read_acctual_weather()
            accWeatherTemp.write_acctual_weather()
            x=datetime.now()
        
if __name__ == "__main__":

    main()