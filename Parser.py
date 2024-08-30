import requests

class WbParser:
    def __init__(self, art:str):
        self.art = art
        self.part = art[:6]
        self.vol = art[:4]
        self.BascetNum = self.FindBascet()

    @property
    def TestArticle(self):
        headers = {
            'accept': '*/*',
            'origin': 'https://www.wildberries.ru',
            'priority': 'u=1, i',
            'referer': f'https://www.wildberries.ru/catalog/{self.art}/detail.aspx',
            'sec-ch-ua': '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0 (Edition Yx GX)',
        }

        try:
            req = requests.get(
                f'https://basket-{self.BascetNum}.wbbasket.ru/vol{self.vol}/part{self.part}/{self.art}/info/ru/card.json',
                headers=headers)
            return True
        except:
            return False

    def FindBascet(self):

        for j in range(7,20):
            try:
                response = requests.get( f'https://basket-{j}.wbbasket.ru/vol{self.vol}/part{self.part}/{self.art}/images/c246x328/1.webp')
                if response.ok :
                    return j
            except:
                continue
        return
    
    def ChangeImage(self):
        headers = {
            'sec-ch-ua': '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
            'Referer': f'https://www.wildberries.ru/catalog/{self.art}/detail.aspx',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0 (Edition Yx GX)',
            'sec-ch-ua-platform': '"Windows"',
        }

        arr = []

        for i in range(1,self.imageCount+1):

            try:
                response = requests.get(f'https://basket-{self.BascetNum}.wbbasket.ru/vol{self.vol}/part{self.part}/{self.art}/images/c246x328/{i}.webp',
                                        headers=headers)
            except:
                return 'not real article'

            arr.append(response.url)

        return arr

    def ChangeCard(self):

        headers = {
            'accept': '*/*',
            'origin': 'https://www.wildberries.ru',
            'priority': 'u=1, i',
            'referer': f'https://www.wildberries.ru/catalog/{self.art}/detail.aspx',
            'sec-ch-ua': '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0 (Edition Yx GX)',
        }

        try:
            req = requests.get(f'https://basket-{self.BascetNum}.wbbasket.ru/vol{self.vol}/part{self.part}/{self.art}/info/ru/card.json',
                               headers=headers)
        except:
            return 'not real article'

        src = req.json()

        self.imageCount = src['media']['photo_count']

        return src

    def ChangeDetail(self):
        headers = {
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Origin': 'https://www.wildberries.ru',
            'Referer': f'https://www.wildberries.ru/catalog/{self.art}/detail.aspx',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 OPR/111.0.0.0 (Edition Yx GX)',
            'sec-ch-ua': '"Opera GX";v="111", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'appType': '1',
            'curr': 'rub',
            'dest': '-366541',
            'spp': '30',
            'ab_testing': 'false',
            'nm': f'{self.art}',
        }

        try:
            req = requests.get('https://card.wb.ru/cards/v2/detail',
                               params=params,
                               headers=headers)
        except:
            return 'not real article'

        src = req.json()

        return src
#
# parser = WbParser('111111111')
# parser.ChangeCard()
# parser.ChangeImage()
# parser.ChangeDetail()
