import json
import requests
from bs4 import BeautifulSoup

count = 0

def writeDocData(org, docData):
    with open("scraped_data.json", 'a') as jsonFile:
        # jsonFile.write(json.dumps({f"{org}": docData}), indent=4)
        jsonFile.write(json.dumps({f"{org}": docData}, indent=4))


def scrapeSGR(url):
    global count
    postData = {
        'action' : 'GetDoctorDetails',
        'Department' : '',
        'hospital' : 1,
        'doctor' : ''
    }
    resp = requests.post(url, data=postData)
    jsonData = json.loads(resp.text)

    doctorList = {}
    for doctor in jsonData["DoctorList"]:
        soup = BeautifulSoup(requests.get(jsonData["DoctorList"][doctor]["detail_path"]).text, 'html.parser')
        interest_div = soup.find_all("div", {"class": "readmore js-read-more service-detail-block"})
        try:
            doc_treatment = interest_div[-1].p.contents[0].strip()
        except Exception as e:
            doc_treatment = ""
        count += 1
        doctorList[f"{count}"] = {
            "name": jsonData["DoctorList"][doctor]["FinalName"],
            "degree": jsonData["DoctorList"][doctor]["degree"],
            "dept": jsonData["DoctorList"][doctor]["dept_name"],
            "mobile": jsonData["DoctorList"][doctor]["Mobile"],
            "email": jsonData["DoctorList"][doctor]["EMail"],
            "treatment": doc_treatment,
        }
        print(count)
    
    writeDocData("american", doctorList)
    

def scrapeData(url):
    scrapeSGR(url)

if __name__ == "__main__": 
    with open("List of Hospitals URL.txt", 'r') as file:
        for url in file.readlines():
            scrapeData(url.strip())
            break