#Gets close enough geosearch
import geocoder
import requests

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


def getGeoLocation():
    g = geocoder.ip('me')
    print(g.city)
    print(g.lat)
    print(g.lng)
    return(g.city,g.lng,g.lat)
#https://api.weather.gov/alerts?active=true&status=actual&message_type=alert,update&point=29.6516%2C-82.3248&urgency=Immediate,Expected&severity=Extreme,Severe&certainty=Observed,Likely&limit=500
def fetchNoaaReports(lng,lat):
    #url = f"https://api.weather.gov/alerts?active=true&status=actual&message_type=alert,update&point={lng}%2C{lat}&urgency=Immediate,Expected&severity=Extreme,Severe&certainty=Observed,Likely&limit=500"
    url = "https://api.weather.gov/alerts?active=true&status=actual&message_type=alert,update&point=43.24%2C-71.55&urgency=Immediate,Expected&severity=Extreme,Severe&certainty=Observed,Likely&limit=500"
    print(url)
    response = requests.get(url)
    return response.json();

def createReportObjects(reportJson):
    reportList = [];
    print("Latest report for this location ")
    for item in reportJson['features']:
        feature = item['properties']
        reportList.append(Report(feature['effective'],feature['severity'],feature['certainty'],feature['urgency'],feature['event'],
        feature['headline'],feature['description'],feature['instruction'],feature['response']))
    return reportList



if __name__ == '__main__':
    cit,lng,lat = getGeoLocation()
    json = fetchNoaaReports(lng,lat)
    print(json)
    #print(json['features'])
    reportsList = createReportObjects(json)
    print(len(reportsList))



