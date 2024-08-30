import sqlite3
import random

def Adult(detail):
    try:
        if detail["data"]["products"][0]["isAdult"] == True:
            return 'TRUE'
    finally:
        return 'FALSE'

def CrateId():
    con = sqlite3.connect("anime.db")
    cur = con.cursor()

    arr = cur.execute('''SELECT id from goods  ''').fetchall()

    con.close()

    id = str(int(arr[-1][0])+1)[::-1]

    while len(id) <7:
        id += '0'

    return id[::-1]

def WBTable():
    con = sqlite3.connect("anime.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE  IF NOT EXISTS WBart( article TEXT  ) ;''')

    con.commit()
    con.close()

def CheckingArticle (art):
    con = sqlite3.connect("anime.db")
    cur = con.cursor()

    if len(cur.execute('''SELECT * from WBart where article = ? ''',[art,]).fetchall())  == 0 :
        con.close()
        return True

    con.close()
    return False

def Characteristics(card):
    arr = []

    for i in card["grouped_options"]:
        arr.append([i["group_name"]])

        for j in i["options"]:
            arr.append([j["name"], j["value"]])

    return arr

def NewArticle(art):
    con = sqlite3.connect("anime.db")
    cur = con.cursor()

    cur.execute('''insert into WBart(article) values(?) ''', [art, ])

    con.commit()
    con.close()

def FillInfo(message,parser,):
    category = message.text

    card = parser.ChangeCard()
    detail = parser.ChangeDetail()
    images = parser.ChangeImage()

    con = sqlite3.connect("anime.db")
    cur = con.cursor()

    cur.execute('''INSERT INTO goods (id, name, img, price ,discount,value, age_limit, Rating, Reviews, characteristics, Category, Reviews_user) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ''',
                [CrateId(),
                 card["imt_name"],
                 str(images),
                 detail["data"]["products"][0]["sizes"][0]["price"]["total"]//100,
                 random.randrange(0, 100, 5),
                 card["description"],
                 Adult(detail),
                 detail["data"]["products"][0]["reviewRating"],
                 detail["data"]["products"][0]["feedbacks"],
                 str(Characteristics(card)),
                 category,
                 '[]' ])

    con.commit()
    con.close()
    return

