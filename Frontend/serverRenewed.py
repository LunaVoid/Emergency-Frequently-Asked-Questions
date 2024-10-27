from flask import Flask, render_template
import os
import json

class Report():
    def __init__(self, effectiveDate, severity, certainty, 
    urgency, event, headline, description, instruction, response):
        self.effectiveDate = effectiveDate
        self.severity = severity
        self.certainty = certainty
        self.urgency = urgency
        self.event = event
        self.headline = headline
        self.description = description
        self.instruction = instruction
        self.response = response


app = Flask(__name__)

def weatherDataFetcher(name = "store.json"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    json_path = os.path.join(script_dir, '../', name)
    print(json_path)
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return data  # Assuming data is structured as needed
    except FileNotFoundError:
        return ["File not found. Returning default data."]
    except json.JSONDecodeError:
        return ["Error decoding JSON. Returning default data."]
    except Exception as e:
        return [f"An error occurred: {str(e)}"]

def get_data():
    jsonData = weatherDataFetcher()  # Get actual data from the JSON
    ObjectList = createReportObjects(jsonData)
    for item in ObjectList:
        print(item.severity)
    return ObjectList

def createReportObjects(reportJson):
    reportList = [];
    print("Latest report for this location" + reportJson['updated'])
    for item in reportJson['features']:
        feature = item['properties']
        reportList.append(Report(feature['effective'],feature['severity'],feature['certainty'],feature['urgency'],feature['event'],
        feature['headline'],feature['description'],feature['instruction'],feature['response']))
    return reportList

def get_faq():
    faqs = weatherDataFetcher("faq.json")
    return faqs

@app.route('/')
def home():
    data = get_data()
    faq = get_faq()
    print(faq['FAQs'])
    faq = faq['FAQs']
    return render_template('index.html', data=data, faq=faq)

def runApp():
   app.run(port=5000, debug=False)
   print("Flask is on 127.0.0.1:5000")

if __name__ == '__main__':
    app.run(port=5000, debug=True)
    print("Flask is on 127.0.0.1:5000")
