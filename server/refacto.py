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
    "Odesa Oblast": "Одеська Область",
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

def renameIcon(dat,path):
    try:
        pth = '.\\public\\img\\' + dat + path[len(path)-4:len(path)]
        os.rename(path,pth)
        return pth
    except:
        return 

def formating(dat):
    n = ''
    
    for i in range(len(dat)):
        try:
            if type(int(dat[i])) is int:
                n += dat[i]
            if len(n) == 2:
                n += '.'
        except:
            continue
    try:
        return float(n)
    except:
        return ''


def generate_arr_voc(vocabulary):
    data = []
    i = 0
    for key in vocabulary:
        n = []
        n.append(i)
        n.append(key)
        n.append(vocabulary[key])
        data.append(n)
        i += 1
    return data


def read_JSON():
    with open('server\data.json') as json_file:
        res1 = []
        res2 = []
        data = json.load(json_file)
        for p in data['citiesList']:
            n = []
            n.append(p['areasID'])
            n.append(p['nameUA'])
            n.append(p['nameEN'])
            n.append(p['latitude'])
            n.append(p['longitude'])
            n.append(p['icon'])
            res1.append(n)

        for j in data['areasList']:
            t = []
            t.append(j['nameEN'])
            res2.append(t)

        return [res1[i] + res2[i] for i in range(len(res1))]


def find_area_id(dat, voc):
    for i in range(len(voc)):
        if dat.lower() == voc[i][1].lower():
            return voc[i][0]


def create_Json(dat, voc, area_func,formate,rename):
    
    data = {}
    data['citiesList'] = []
    data['areasList'] = []

    for i in range(len(voc)):
        data['areasList'].append({
            'nameUA': voc[i][2],
            'nameEN': voc[i][1],
            'id': voc[i][0]
        })

    for j in range(len(dat)):
        data['citiesList'].append({
            'areasID': area_func(dat[j][6], voc),
            'nameUA': dat[j][1],
            'nameEN': dat[j][2],
            'latitude': formate(dat[j][3]),
            'longitude':formate(dat[j][4]),
            'icon': rename(dat[j][2],dat[j][5])
        })

    with open('server\data2.json','w') as json_file:
        json.dump(data, json_file)


if __name__ == "__main__":
    create_Json(read_JSON(),generate_arr_voc(vocabulary),find_area_id,formating,renameIcon)
