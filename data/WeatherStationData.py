import requests

url = 'https://grobliro-device.dataplicity.io/'

res = requests.get(url+'SensorData.csv')
res.raise_for_status()
print(res.status_code == requests.codes.ok)
print(len(res.text))
print(res.text)
sdf = open('C:/Users/roman/Documents/GitHub/WeatherStation/data/SensorData.csv','wb')
for chunk in res.iter_content(100000):
    sdf.write(chunk)
sdf.close()
