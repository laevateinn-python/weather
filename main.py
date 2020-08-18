import os
import requests
from bs4 import BeautifulSoup

vocabulary = {
"Cherkasy Oblast":"Черкаська Область",
"Chernihiv Oblast":"Чернігівська Область",
"Chernivtsi Oblast":"Чернівеська Область",
"Dnipropetrovsk Oblast":"Дніпропетровська Область",
"Donetsk Oblast":"Донецька Область",
"Ivano-Frankivsk Oblast":"Івано-Франківська Область",
"Kharkiv Oblast":"Харківська Область",
"Kherson Oblast":"Херсонська Область",
"Khmelnytskyi Oblast":"Хмельницька Область",
"Kiev Oblast":"Київська Область",
"Kirovohrad Oblast":"Кіровоградська Область",
"Luhansk Oblast":"Луганська Область",
"Lviv Oblast":"Львівська Область",
"Mykolaiv Oblast":"Миколаївська Область",
"Odessa Oblast":"Одеська Область",
"Poltava Oblast":"Полтавська Область",
"Rivne Oblast":"Рівненська Область",
"Sumy Oblast":"Сумська Область",
"Ternopil Oblast":"Тернопільська Область",
"Vinnytsia Oblast":"Вінницька Область",
"Volyn Oblast":"Волинська Область",
"Zakarpattia Oblast":"Закарпатська Область",
"Zaporizhia Oblast":"Запорізька Область",
"Zhytomyr Oblast":"Житомирська Область",
"Kyiv":"Київ",
"Sevastopol":"Севастополь",
"Crimea":"Крим",
}
 
class ParserCity:
    def __init__(self, voc):
        self.Headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        self.vocabulary = voc

    def request(self,url):
        req = requests.get(url, headers=self.Headers).text
        soup = BeautifulSoup(req,'lxml')
        return soup

    def translate(self,data):
        res = data[1:len(data)]
        for i in range(len(res)):
            for key in self.vocabulary:
                if res[i][2] == key:
                    res[i].append(self.vocabulary[key])
        return res


    def parsingCity(self,url):
        data = []
        soup = self.request(url)
        table = soup.find("table", attrs={"class":"wikitable sortable"})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            link = ["https://en.m.wikipedia.org" + ele.find('a').get('href') for ele in cols[0:1]]
            cols = [ele.text.strip() for ele in cols[0:3]]
            data.append(cols + link)
        data = self.translate(data)
        return(data)

class ParserCoordinates:
    def __init__(self):
        pass

    def parse(self,parserReq,data):
        res = []
        for i in data:
            soup = parserReq(i[3])
            table = soup.find("table", attrs={"class":"infobox geography vcard"})
            table = table.find('span',attrs={"class":"geo-dms"})
            table = [ele.text for ele in table.find_all('span')]
            res.append(table)
        return res

class downloadIcon:
    def __init__(self,parserReq):
        self.parserReq = parserReq

    def parse(self):
        data = []
        soup = self.parserReq("https://uk.wikipedia.org/wiki/Міста_України_(за_алфавітом)")
        table = soup.find("table")
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            lnk = ["https:" + ele.find('img').get("src") for ele in cols[0:1]]
            cols = [ele.text.strip() for ele in cols[1:2]]
            data.append(lnk + cols)
        return data
    def download(self,path):
        data = self.parse()
        for i in data:
            link = i[0]
            pth = path + i[1] + link[len(link)-4:len(link)]
            r = requests.get(link, stream=True)
            if r.status_code == 200:
                with open(pth, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)





obj2 = ParserCity(vocabulary)
req = obj2.request
downloadIcon(req).download("public\img\emblem\r")