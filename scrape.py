import re
import json
import urllib
import requests
from bs4 import BeautifulSoup

count = 0

def writeDocData(org, docData):
    print("Writing to file...")
    with open("scraped_data_" + org +".json", 'a') as jsonFile:
        jsonFile.write(json.dumps({f"{org}": docData}, indent=4))

def decode_email(encoded_email):
    l = "/cdn-cgi/l/email-protection#"
    t = encoded_email.split(l)[-1]
    r = int(t[:2], 16)
    decoded_email = ""
    for i in range(2, len(t), 2):
        char_code = int(t[i:i+2], 16) ^ r
        decoded_email += chr(char_code)
    try:
        decoded_email = urllib.parse.unquote(decoded_email)
    except Exception as e:
        print("Error decoding email:", e)
    return decoded_email

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
    
    writeDocData("sgr", doctorList)
    count = 0
    
def scrapeBombayHptl(url):
    global count
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    script_tags = soup.find_all('script')

    pattern = r'doctors:(.*) departments:'
    matches = re.findall(pattern, str(script_tags[6]).replace('\r\n                    ', ''), re.DOTALL)
    match = matches[:str(matches[0]).rfind(',')] + matches[str(matches[0]).rfind(',')+1:]
    docs_clean = ""
    for docs in match:
        docs_clean =  "{\"doctors\":" + docs.strip().rstrip(',') + "}"
    
    jsonData = json.loads(docs_clean)
    doctorList = {}

    for dept in jsonData["doctors"]:
        for doc in jsonData["doctors"][dept]:
            soup = BeautifulSoup(requests.get(url + doc['slug']).text, 'html.parser')
            # print(requests.get(url + doc['slug']).text)
            area_of_interest = ""
            phone_numbers = ""
            email = ""

            try:
                qualifications = soup.find('h5', string='Qualifications').find_next('p').get_text(strip=True)
                area_of_interest = soup.find('h5', string='Area Of Interest').find_next('p').get_text(strip=True)
                phone_links = soup.select('.details__content a[href^="tel:"]')
                phone_numbers = [link.get_text(strip=True) for link in phone_links]

                email_protection_link = soup.find('a', href=lambda href: href and href.startswith('/cdn-cgi/l/email-protection#'))
                email_protection_href = email_protection_link['href']
                email = decode_email(email_protection_href)
            except:
                try:
                    qualifications = soup.find('h5', string='Qualification').find_next('div', class_='details__content').find('p').text.strip()
                except:
                    qualifications = ""
            finally:
                count += 1
                doctorList[f"{count}"] = {
                    "name": doc["name"],
                    "degree": qualifications,
                    "dept": doc["department"],
                    "mobile": phone_numbers,
                    "email": email,
                    "treatment": area_of_interest,
                }
                print(count)
    writeDocData("bombayhospital", doctorList)
    count = 0

def scrapeData(url):
    # scrapeSGR(url)
    scrapeBombayHptl(url)

if __name__ == "__main__": 
    with open("List of Hospitals URL.txt", 'r') as file:
        for url in file.readlines():
            scrapeData(url.strip())
            break