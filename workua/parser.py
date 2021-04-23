import requests
from bs4 import BeautifulSoup
from time import time, sleep
import random
import csv
import json
import sqlite3


def random_sleep():
    sleep(random.randint(1, 3))


BASE_URL = f'https://www.work.ua/jobs/'


def parser_url_job(n_pages=False):
    page = 0
    list_with_jobs_url = []
    if not n_pages:
        n_pages = 3
    while page <= n_pages-1:

        page += 1
        print(f'Scan page: {page}')

        params = {
            'ss': 1,
            'page': page,
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:87.0) Gecko/20100101 Firefox/87.0',  # user-agent == 'python-3.9'
        }
        response = requests.get(BASE_URL, params=params, headers=headers)

        random_sleep()

        response.raise_for_status()  # stop program if status_code != 2xx

        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        jobs_list = soup.find(id="pjax-job-list")

        if jobs_list is None:
            break

        cards = jobs_list.find_all("div", {"class": "job-link"})

        for card in cards:

            tag_a = card.find("h2").find("a")
            job_id = tag_a['href']

            result = f'https://www.work.ua{job_id}'
            list_with_jobs_url.append(result)
    print(f'find works: {len(list_with_jobs_url)}')
    return list_with_jobs_url

url_for_pars_info = parser_url_job(1)

def parser_info_job():
    result = []
    for url in url_for_pars_info:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:87.0) Gecko/20100101 Firefox/87.0',
            # user-agent == 'python-3.9'
        }
        response = requests.get(url, headers=headers)
        random_sleep()
        response.raise_for_status()  # stop program if status_code != 2xx
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        job_url = url
        job_title = soup.find(id="h1-name").text

        job_description = soup.find(id="job-description").find('p').text

        result.append({
            'job_url': f'{job_url}',
            'job_title': f'{job_title}',
            'job_description': f'{job_description}'
        })
    return result

data_to_write = parser_info_job()


#CSV
def write_date_to_csv():
    with open(f'./jobs_{time()}.csv', 'w') as file:
        start_time = time()
        fieldnames = ['url', 'title', 'description']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for work in data_to_write:
            csv_writer.writerow({
                'url': work['job_url'],
                'title': work['job_title'],
                'description': work['job_description']
            })
        end_time = time()
        all_time = end_time - start_time
        print("file recording 'CSV' completed!\n", f"for: {all_time}'s")


#JSON
def write_date_to_json():
    start_time = time()
    with open(f'./jobs_{time()}.json', 'w') as file:
        all_data = []
        for work in data_to_write:
            data = {f"id-{(work['job_url']).split('/')[-2]}": {
                'url': work['job_url'],
                'title': work['job_title'],
                'description': work['job_description']
                }
            }
            all_data.append(data)
        json.dump(all_data, file, indent=3, ensure_ascii=False)
        end_time = time()
        all_time = end_time - start_time
        print("file recording 'JSON' completed!\n", f"for: {all_time}'s")

#DB
def write_date_to_db():
    start_time = time()
    db_name = f'./jobs_{time()}.db'
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute('''CREATE TABLE jobs_base
                   (url VARCHAR, title VARCHAR, description VARCHAR)''')
    for work in data_to_write:
        cur.execute(f"INSERT INTO jobs_base VALUES (?,?,?)", (f"{work['job_url']}", f"{work['job_title']}", f"{work['job_description']}"))

    con.commit()

    con.close()
    end_time = time()
    all_time = end_time - start_time
    print("file recording 'DB' completed!\n", f"for: {all_time}'s")

write_date_to_csv()
print('=========')
write_date_to_json()
print('=========')
write_date_to_db()
print('=========')
print('Have a nice DAy!')



