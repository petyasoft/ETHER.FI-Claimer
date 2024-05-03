from fake_useragent import UserAgent
import asyncio
import aiohttp
import random
from time import perf_counter


SLEEP = [0,60]  # задержка в секундах берется рандомно от левой границы, до правой

async def claim(wallet = "",proxies = None):
    async with aiohttp.ClientSession() as session:
        session.proxies = proxies 
        headers = {
            'accept': '*/*',
            'content-type': 'text/plain;charset=UTF-8',
            'origin': 'https://app.ether.fi',
            'priority': 'u=1, i',
            'referer': 'https://app.ether.fi/portfolio',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': UserAgent().random,
        }

        data = '{'+f'"account":"{wallet}"'+'}'
        await asyncio.sleep(random.randint(SLEEP[0],SLEEP[1]))
        async with session.post("https://app.ether.fi/api/dailyStreak/updateStreak",headers=headers, data=data) as response:
            text = await response.text()
            print(wallet,text)
            
async def main():
    while True:
        start = perf_counter()
        tasks = []
        with open('wallets.txt') as file:
            wallets = [wallet.strip() for wallet in file.readlines()]
            for wallet in wallets:
                if ';' in wallet:
                    wallet, proxy = wallet.split(";")
                else:
                    wallet = wallet
                    proxy = None
                    
                proxies = {
                        'http': None,
                        'https': None,
                    }
                
                if proxy:
                    proxies['http'] = f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
                    proxies['https'] = f"http://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
                tasks.append(claim(wallet=wallet, proxies=proxies))

        await asyncio.gather(*tasks)
        end = perf_counter()
        await asyncio.sleep(60*60*24-(end-start))

asyncio.run(main())
