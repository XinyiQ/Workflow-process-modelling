# WPS Execute Operation
 
import requests, os
 
payload = open(os.path.dirname(os.path.abspath(__file__)) +"\\Union.xml").read()
 
 
wpsServerUrl = "https://gisedu.itc.utwente.nl/student/s6039715/gpw/assignment/Assignment1/wps.py?"
 
response = requests.post(wpsServerUrl, data=payload)
print("Content-type: application/json")
print()
print(response.text)