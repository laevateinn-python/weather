import os
import requests
from bs4 import BeautifulSoup
import json

vocabulary = {
    "Cherkasy Oblast": "Черкаська Область",
    "Chernihiv Oblast": "Чернігівська Область",
    "Chernivtsi Oblast": "Чернівеська Область",
    "Dnipropetrovsk Oblast": "Дніпропетровська Область",
    "Donetsk Oblast": "Донецька Область",
    "Ivano-Frankivsk Oblast": "Івано-Франківська Область",
    "Kharkiv Oblast": "Харківська Область",
    "Kherson Oblast": "Херсонська Область",
    "Khmelnytskyi Oblast": "Хмельницька Область",
    "Kiev Oblast": "Київська Область",
    "Kirovohrad Oblast": "Кіровоградська Область",
    "Luhansk Oblast": "Луганська Область",
    "Lviv Oblast": "Львівська Область",
    "Mykolaiv Oblast": "Миколаївська Область",
    "Odessa Oblast": "Одеська Область",
    "Poltava Oblast": "Полтавська Область",
    "Rivne Oblast": "Рівненська Область",
    "Sumy Oblast": "Сумська Область",
    "Ternopil Oblast": "Тернопільська Область",
    "Vinnytsia Oblast": "Вінницька Область",
    "Volyn Oblast": "Волинська Область",
    "Zakarpattia Oblast": "Закарпатська Область",
    "Zaporizhia Oblast": "Запорізька Область",
    "Zhytomyr Oblast": "Житомирська Область",
    "Kyiv": "Київ",
    "Sevastopol": "Севастополь",
    "Crimea": "Крим",
}


def generate_icon_path(data):
    arr = os.listdir('public\\img')
    for i in range(len(arr)):
        if data.lower() in arr[i][0:len(arr)-4].lower():
            return 'public\\img\\' + arr[i]


def generateJson(CITYDATE, COORDINATES):
    print('generating JSON')
    data = {}
    data['citiesList'] = []
    data['areasList'] = []
    for i in range(len(CITYDATE)-1):
        data['citiesList'].append({
            'areasID': i,
            'nameUA': str(CITYDATE[i][1]),
            'nameEN': str(CITYDATE[i][0]),
            'latitude': str(COORDINATES[i][0]),
            'longitude': str(COORDINATES[i][1]),
            'icon': generate_icon_path(CITYDATE[i][1])
        })
        data['areasList'].append({
            'nameUA': str(CITYDATE[i][4]),
            'nameEN': str(CITYDATE[i][2]),
            'id': i
        })
    with open('server\\data.json', 'w') as File:
        json.dump(data, File)
    print('generated sucsesfull')


class ParserCity:
    def __init__(self, voc):
        self.Headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
        self.vocabulary = voc

    def request(self, url):
        req = requests.get(url, headers=self.Headers).text
        soup = BeautifulSoup(req, 'lxml')
        return soup

    def translate(self, data):
        res = data[1:len(data)]
        for i in range(len(res)):
            for key in self.vocabulary:
                if res[i][2] == key:
                    res[i].append(self.vocabulary[key])
            if len(res[i]) < 5:
                res[i].append('')
        return res

    def parsingCity(self, url):
        print('generating citydate')
        data = []
        soup = self.request(url)
        table = soup.find("table", attrs={"class": "wikitable sortable"})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            link = ["https://en.m.wikipedia.org" +
                    ele.find('a').get('href') for ele in cols[0:1]]
            cols = [ele.text.strip() for ele in cols[0:3]]
            data.append(cols + link)
        data = self.translate(data)
        print('generated sucsesfull')
        return(data)


class ParserCoordinates:
    def __init__(self, parserReq):
        self.parserReq = parserReq

    def parse(self, data):
        print('generating coordinates')
        res = []
        dat = data
        for i in dat:
            try:
                soup = self.parserReq(i[3])
                table = soup.find("table", attrs={"class": "infobox geography vcard"})
                table = table.find('span', attrs={"class": "geo-dms"})
                table = [ele.text for ele in table.find_all('span')]
                res.append(table)
            except:
                res.append(['', ''])
                continue
        print('generated sucsesfull')
        return res


class downloadIcon:
    def __init__(self, parserReq):
        self.parserReq = parserReq

    def parse(self):
        data = []
        soup = self.parserReq(
            "https://uk.wikipedia.org/wiki/Міста_України_(за_алфавітом)")
        table = soup.find("table")
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            lnk = ["https:" + ele.find('img').get("src") for ele in cols[0:1]]
            cols = [ele.text.strip() for ele in cols[1:2]]
            data.append(lnk + cols)
        return data[1:len(data)]

    def download(self, path):
        data = self.parse()
        res = []
        for i in data:
            link = i[0]
            if "[" in i[1]:
                p = i[1].index('[')
                fileName = i[1][0:p]
            else:
                fileName = i[1]

            pth = path + fileName + link[len(link)-4:len(link)]
            res.append(pth)
            # else:
            #r = requests.get(link, stream=True)
            # if r.status_code == 200:
            # with open(pth, 'wb') as f:
            # for chunk in r:
            # f.write(chunk)

        return res


if __name__ == "__main__":
    obj = ParserCity(vocabulary)
    reqInstance = obj.request
    CITYDATE = obj.parsingCity(
        "https://en.m.wikipedia.org/wiki/List_of_cities_in_Ukraine")
    COORDINATES = ParserCoordinates(reqInstance).parse(CITYDATE)
    generateJson(CITYDATE, COORDINATES)

    input()
