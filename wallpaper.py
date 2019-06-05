import requests
import bs4
import os
import sh
import tqdm
import sys

URL = "wallhaven.cc"
#query = "sci"
#path = "Wallhaven"
N_IMAGE_PAGES = 24

def main(query, path):
    q = "https://{}/search?q={}&categories=111&purity=100&sorting=relevance&order=desc".format(URL, query)
    urlreq = requests.get(q)
    soup = bs4.BeautifulSoup(urlreq.text, 'lxml') # Complete html
    soupid = soup.findAll('h1') # picking up all the 'preview' classes
    nro = int(soupid[0].text.split(" ")[0].replace(",","").replace(".",""))
    pages = round(nro/N_IMAGE_PAGES) 
    r_pages = int(nro)/N_IMAGE_PAGES

    if (pages - r_pages) < 0:
        pages = pages - 1

    pas = True
    while pas:
        try:
            user_nro_pages = input("How many pages(max {}) you want to Download (There are 24 wallpapers on a single page):".format(pages))
            user_nro_pages = int(user_nro_pages)
            if user_nro_pages > 0 and user_nro_pages > pages:
                print("ERROR: only number between {} and {}".format(0, pages))
            else:
                pas = False
        except ValueError:
            print("ERROR: only number")
            pass

    sh.mkdir("-p", path)

    for nro_page in range(1, user_nro_pages + 1):
        print("------------- PAGE {}/{} -------------".format(nro_page, user_nro_pages))
        q = "https://{}/search?q={}&categories=111&purity=100&sorting=relevance&order=desc&page={}".format(URL, query, nro_page)
        urlreq = requests.get(q)
        soup = bs4.BeautifulSoup(urlreq.text, 'lxml') # Complete html
        soupid = soup.findAll('a', {'class': 'preview'}) # picking up all the 'preview' classes
        ids = list(map(lambda s: s["href"].split("/")[-1], soupid))
        for i in tqdm.tqdm(ids):
            urlimage = requests.get("https://wallhaven.cc/w/{}".format(i))
            soup = bs4.BeautifulSoup(urlimage.text, 'lxml') # Complete html
            soupid = soup.findAll('img', {'id': 'wallpaper'}) # picking up all the 'preview' classes
            final_url = soupid[0]["src"]
            imgreq = requests.get(final_url) #image response
            if imgreq.status_code == 200:
                with open(path+"/"+os.path.basename(final_url), 'ab') as imageFile:
                    for chunk in imgreq.iter_content(1024):
                        imageFile.write(chunk)

if __name__ == "__main__":    
    if(len(sys.argv) == 3):
        query = sys.argv[1]
        path = sys.argv[2]
        if path[-1] == "/":
            main(query, path[0: -1])
        else:
            main(query, path)
    else:
        print("help: python wallpaper.py QUERY PATH")