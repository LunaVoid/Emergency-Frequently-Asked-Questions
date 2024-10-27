from flask import Flask, render_template
import os
import json

app = Flask(__name__)

def weatherDataFetcher():
   try:
      script_dir = os.path.dirname(os.path.abspath(__file__))
      json_path = os.path.join(script_dir, '..', 'store.json')
      with open(json_path, 'r') as file:
         #data = WeatherFetch.createReportObjects(json.load(file))
         data = json.load(file)
         data = ["One","Two"]
      return data
   except:
      a = ["One","Two"]
      return a

def get_data():
   jsonData = [1,2,3] #weatherDataFetcher()
   return jsonData


@app.route('/')
def home():
   data = get_data()
   print("here")
   print(data)
   return render_template('index.html', data = data )

def runApp():
   app.run(port=5000, debug=False)
   print("Flask is on 127.0.0.1:5000")

if __name__ == '__main__':
   app.run(port=5000, debug=True)
   print("Flask is on 127.0.0.1:5000")
