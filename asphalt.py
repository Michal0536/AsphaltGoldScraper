import requests
from bs4 import BeautifulSoup
import json5
import discord
import random


def get_proxy():
    x = open("proxy_compare.txt" , 'r')        
    proxy = {
        'https' : "",
        'http':""
    }
    proxy_lista =[]
    for line in x:
        proxy_lista.append(line[:-1])

    element = random.choice(proxy_lista)
    ip = element.split(":")[0]
    port = element.split(":")[1]
    login = element.split(":")[2]
    passwd = element.split(":")[3]

    https_proxy_format = "https://" +login+":"+passwd+"@"+ip+":"+port
    http_proxy_format = "http://" +login+":"+passwd+"@"+ip+":"+port
    proxy['https'] = https_proxy_format 
    proxy['http'] = http_proxy_format

    return proxy


def asphalt_gold_scrapper(url):
    headers_q = {
    'authority': 'www.asphaltgold.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="104", "Opera";v="90"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84',
    }
    asphalt_stock = []
    suma = 0
    r = requests.get(url = url, headers=headers_q,proxies=get_proxy())
    if r.status_code==200:
        soup = BeautifulSoup(r.content,'lxml')
        x = soup.select('script')
        for D in x:
            if r'window.ElevarGtmSuite.handlers.cartReconcile' in str(D):
                d=D
        JsonData = json5.loads(str(d).split("const product =")[1].split("if (config.event_config.product_view) {")[0].replace(';','').split('items:[')[0])
        for item in JsonData["items"]:
            img = "https:"+item.get('image')
            price = item.get('price') + "€"
            name = item.get('name')
            size = str(item.get("variant")).split('\\')[0][0:4]
            if size[-1]=="/" or size[-1]==" ":
                size=str(size[:-1]).replace(' ','')
            asphalt_stock.append(f"{size} [{str(item.get('inventory'))}]\n")
            suma = suma + int(item.get('inventory'))


        leng = len(asphalt_stock)
        middle_index = leng//2
        first_stock = asphalt_stock[:middle_index]
        second_stock = asphalt_stock[middle_index:]

        embed = discord.Embed(title=f'{name}', color=0x50d68d, url=url)
        embed.set_thumbnail(url=f'{img}')
        embed.add_field(name='Total Stock', value=f'{suma}' ,inline='false')
        embed.add_field(name='PRICE', value=f'{price}' ,inline='false')
        embed.add_field(name='SIZE [STOCK]' , value=f'{" ".join(first_stock)}', inline="true")
        embed.add_field(name='SIZE [STOCK]' , value=f'{" ".join(second_stock)}', inline="true")

        embed.set_footer(text='by Michał#0536')
    
        return embed  