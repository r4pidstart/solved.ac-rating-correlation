import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import html
import asyncio
import csv

def get_codeforces_rating(handle: tuple[str, str, str], writer: csv.DictWriter):
    url = f"https://codeforces.com/profile/{handle[2]}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rating_div = soup.select_one('#pageContent > div:nth-child(3) > div > div.info > ul > li:nth-child(1) > span')
        if rating_div:
            rating = rating_div.text
            if rating.isdigit():
                writer.writerow({'boj': handle[0], 'rating1': handle[1], 'cp':handle[2], 'rating2':rating})
                print(f'cf - {handle[1]}, {rating}')
            return
        else:
            return
    else:
        return
    
def get_atcoder_rating(handle: tuple[str, str, str], writer: csv.DictWriter):
    url = f"https://atcoder.jp/users/{handle[2]}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rating_span = soup.select('td')
        if rating_span:
            try:
                rating = rating_span[-4].text.split()[0]
                if rating.isdigit():
                    writer.writerow({'boj': handle[0], 'rating1': handle[1], 'cp':handle[2], 'rating2':rating})
                    print(f'at - {handle[1]}, {rating}')
            except:
                pass
            return
        else:
            return
    else:
        return
    
user_list=[]
def get_users():
    for i in range(600):
        url = f"https://solved.ac/ranking/tier?page={i+1}"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        rows = soup.select('table tbody tr')
        for row in rows:
            columns = row.find_all('td')
            try:
                user_list.append(
                    (
                        columns[1].select_one('a b').text,  # name
                        columns[2].select_one('b div span').text,  # rating
                    )
                )
            except:
                pass

def get_cf_handle(writer_cf: csv.DictWriter, writer_at: csv.DictWriter):
    for it in user_list:
        url = f"https://www.acmicpc.net/user/{it[0]}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.select('#statics tbody tr')

        print(f'current: {it[0]}')
        for row in rows:
            try:
                if row.text[:10] == "Codeforces":
                    get_codeforces_rating((it[0], it[1], row.select_one('td a span').text), writer_cf)
                elif row.text[:7] == "Atcoder":
                    get_atcoder_rating((it[0], it[1], row.select_one('td a span').text), writer_at)
            except:
                pass


f_path = './'
global writer_cf, writer_at
async def main():
    csvfile1=open(os.path.join(f_path, 'output_cf.csv'), 'w', newline='')
    fieldnames = ['boj', 'rating1', 'cp', 'rating2']
    writer_cf = csv.DictWriter(csvfile1, fieldnames=fieldnames)

    csvfile2=open(os.path.join(f_path, 'output_at.csv'), 'w', newline='')
    fieldnames = ['boj', 'rating1', 'cp', 'rating2']
    writer_at = csv.DictWriter(csvfile2, fieldnames=fieldnames)

    writer_cf.writeheader()
    writer_at.writeheader()

    get_users()
    pd.DataFrame(user_list).to_csv(os.path.join(f_path, "solved"), index=False)

    get_cf_handle(writer_cf, writer_at)

    csvfile1.close()
    csvfile2.close()

if __name__ == '__main__':
    asyncio.run(main())
    