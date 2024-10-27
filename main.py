from Frontend import serverRenewed
from Weather import WeatherFetch 
import os 
import time
import json
import schedule
import requests
from LocalAi import ollama,sendRequest,texttoSpeech
from queue import Queue
import threading
summary_queue = Queue()
faq_queue = Queue()

#All severe observed weather at coordinates - https://api.weather.gov/alerts/active?status=actual&message_type=alert&point=29.6516%2C-82.3248&urgency=Immediate,Expected&severity=Extreme,Severe&certainty=Observed,Likely&limit=10
#All severe Alerts US - https://api.weather.gov/alerts/active?status=actual&message_type=alert&urgency=Immediate,Expected&severity=Extreme,Severe&certainty=Observed,Likely&limit=10
#Example severe https://api.weather.gov/alerts?active=true&status=actual&message_type=alert,update&point=43.24%2C-71.55&urgency=Immediate,Expected&severity=Extreme,Severe&certainty=Observed,Likely&limit=500
wifi_available = True
weatherList = []

def check_wifi():
    global wifi_available
    try:
        # Attempt to connect to a reliable server
        requests.get("http://www.google.com", timeout=5)
        wifi_available = True
    except requests.ConnectionError:
        wifi_available = False
        ollama.start_ollama_model()
    return wifi_available

def writefile(data,file = "store.json"):
    with open(file, "w") as file:
        json.dump(data, file)

def fetchData(lng,lat):
    response = WeatherFetch.fetchNoaaReports(lng,lat)
    #save Data incase we lose power
    writefile(response)
    reportsList = WeatherFetch.createReportObjects(response)
    return reportsList
    

def offlineFetch():
    with open('store.json', 'r') as file:
        #data = WeatherFetch.createReportObjects(json.load(file))
        data = json.load(file)
    return data
        

def runTTS(summaryQueue,faq_queue):
    while True:
        print(summaryQueue)
        if not summaryQueue.empty():
            item = summaryQueue.get()
            print(f'Summarized: {item}')
            texttoSpeech.createLocalAudio(item,"summary")
            summaryQueue.task_done()

        # Process the FAQ queue if it's not empty
        if not faq_queue.empty():
            faqitem = faq_queue.get()
            print(f'Processed FAQ item: {faqitem}')
            faqitem = json.loads(faqitem)
            writefile(faqitem,"faq.json")
            print(faqitem)
            for number,item in enumerate(faqitem["FAQs"]):
                texttoSpeech.createLocalAudio(f'''Question: {item["question"]} Answer: {item["answer"]}''',f"question{number}")
            faq_queue.task_done()
        else:
            print(f"Queue is empty, waiting for items...")

            time.sleep(8)  # Sleep briefly to avoid busy waiting

#only happens online
def perform_tasks():
    print("Running Tasks")
    weatherReports = None
    offlineReport = None
    try:
        weatherReports = fetchData(lng,lat)
    except Exception as e:
         print(f"WeatherReport Online Unavailable Falling back: {e}")

    try:
        offlineReport = offlineFetch()
    except Exception as e:
        print(f"FallBack unavailable, entering general advice mode: {e}")
    '''Future expansion incorporate online IBM Model
    if weatherReports != None:
        print("Online Reports Found")
        #IBM(weather_data)  
        print(weatherReports[0].headline)'''
    
    if offlineReport != None:
        print("Offline but we have local storage")
        summary = sendRequest.generate_text(f"Provide a quick and concise paragraph summary of current weather conditions. Alert the User if they need to evacuate and inform them of the severity of the issue. Data: {offlineReport}")
        print(summary+"\n")

        try: 
            print("Queueings")
            summary_queue.put(summary)
        except Exception as e:
            print(f"JSON FAIL, queue fail {e}")

        faqs = sendRequest.generate_text("Judging from the weather report below, create a list of 10 faqs in JSON about this situation that may be asked. Report:" + json.dumps(offlineReport),'''
        Always respond in the below json format by creating a list of FAQs 
        Example:
            {"FAQs": [
        {
            "question": "What is a Red Flag Warning?",
            "answer": "A Red Flag Warning is issued when weather conditions could lead to rapid fire growth and spread, typically due to low humidity, strong winds, and dry vegetation."
        },
        {
            "question": "When is the Red Flag Warning in effect?",
            "answer": "The warning is in effect from 8 AM to 6 PM on Sunday, October 27, 2024."
        }
    ]}''')
        print(faqs)

        try:
            faq_queue.put(faqs)
        except Exception as e:
            print(f"JSON FAIL, queue fail {e}")
        

    else:
        print("Fallback Mode")
        summary = sendRequest.generate_text("There is no current weather reports on record. Please go over what to do in several common severe weather cases and best practices. Additionally, please inform the user about how to reestablish a connection if possible.")
        print(summary)
tts_thread = threading.Thread(target=runTTS, args=(summary_queue,faq_queue))
tts_thread.start()
flask_thread = threading.Thread(target=serverRenewed.runApp)
flask_thread.start()
schedule.every(5).seconds.do(perform_tasks)

if __name__ == '__main__':
    weatherReports =[]
    try:
        while(True):
            print("new loop")
            #isOnline = False
            city,lat,lng = WeatherFetch.getGeoLocation()
            if check_wifi() and lat != None and lng != None:
                fetchData(lng,lat)
                print("Online")
            else:
                print("Offline")
            schedule.run_pending()
            print("Sleep Time")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Program stopped by user.")



   #server.runApp()
   #we will use a data queue
    #q = queue.Queue()
    #flask_thread = threading.Thread(target=server.runApp)
    #fetch_thread = threading.Thread(target=fetchData, args=(q,))
    #store_thread = threading.Thread(target=storeFetchedData, args=(q,))
    

