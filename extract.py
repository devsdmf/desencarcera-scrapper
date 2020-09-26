
import requests
from bs4 import BeautifulSoup
import csv

class Complaint:

    def __init__(self, id, prison, subject, description):
        self.id = id
        self.prison = prison
        self.subject = subject
        self.description = description

base_url = "https://desencarcera.com/denuncias/"
pages = range(1,129)

default_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }

complaints = list()
for p in pages:
    print("Crawling page {}...".format(p))
    r = requests.post(base_url, data = { 'pagina': p }, headers = default_headers)

    print("Processing contents of page {}...".format(p))

    soup = BeautifulSoup(r.text, features="lxml")
    denuncias = soup.find_all(name = "div", class_="info_denuncias")
    for d in denuncias:
        id = str(d.find(name="h3", class_="title_denuncia").string).replace("Denúncia n°","").strip()
        details = d.find_all("p")
        prison = details[0].contents[1].strip()
        subject = details[1].contents[1].strip()
        description = "\\n".join(details[2].contents).strip()
        complaints.append(Complaint(id,prison,subject,description))

print("Exporting data as CSV...")
with open("denuncias.csv", "w") as csvfile:
    dwriter = csv.writer(csvfile, delimiter=",")
    for c in complaints:
        dwriter.writerow([c.id,c.prison,c.subject,c.description])

print("Done!")
