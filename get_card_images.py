from bs4 import BeautifulSoup
import requests
import os
import shutil


if __name__ == "__main__":
    BASE_URL = 'https://goatcardsshop.crystalcommerce.com'
    EXT = '/catalog/naruto_ccg_singles/3837'
    images={}
    idx=0
    visited={}
    urls={}
    naruto_ccg=[]

    html_page = requests.get(BASE_URL+EXT)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    #print(soup.prettify())

    for divData in soup.findAll('div', {"id": 'page-container'}):
        #print(divData)
        for ul in divData.findAll('ul', {'class': 'parent-category'}):
            #print(ul)
            for a in ul.findAll('a', href=True):
                if '/catalog/naruto' in a['href']:
                    naruto_ccg.append(a['href'])


    for naruto_ext in naruto_ccg:
        print()
        print(naruto_ext)
        start = naruto_ext.rfind('-')
        end = naruto_ext.rfind('/')
        dir_name = naruto_ext[start+1:end]

        if dir_name not in os.listdir('./cards'):
            os.mkdir('./cards/%s'%dir_name)
        print(dir_name)
        for i in range(40):
            EXT = naruto_ext + '?page=%d' % i

            html_page = requests.get(BASE_URL+EXT)
            soup = BeautifulSoup(html_page.content, 'html.parser')


            for a in soup.find_all('a', href=True):
                if '/catalog/naruto' in a['href']:
                    if a['href'] not in urls:
                        urls[a['href']]=1


            while urls:

                ext = list(urls.keys())[0]
                urls.pop(ext)

                if ext not in visited:
                    visited[ext]=1

                    sub_url = BASE_URL+ext
                    card_page = requests.get(sub_url)
                    sub_soup = BeautifulSoup(card_page.content, 'html.parser')

                    for divdata in sub_soup.findAll('div', {"class": "image-meta"}):
                        for a in sub_soup.find_all('a', href=True):
                            if '/catalog/naruto' in a['href']:
                                if a['href'] not in urls and a['href'] not in visited:
                                    urls[a['href']]=1

                    for divdata in sub_soup.findAll('div', {"id": "main-image"}):
                        for getimgtag in divdata.findAll('img',src=True):
                            start_idx = getimgtag['src'].rfind('/') + 1
                            img_file = getimgtag['src'][start_idx:]

                            if img_file not in images:
                                idx += 1
                                images[img_file]=1
                                print(img_file)
                                r = requests.get(getimgtag['src'], stream=True) #Get request on full_url
                                if r.status_code == 200:                     #200 status code = OK
                                    with open("cards/%s/card%d.jpg"%(dir_name, idx), 'wb') as f: 
                                        r.raw.decode_content = True
                                        shutil.copyfileobj(r.raw, f)
                                #print()
