import requests
import bs4
import os
import sh
import tqdm
import sys
import argparse

URL = "wallhaven.cc"
N_IMAGE_PAGES = 24

def main(query, path):
    q = f"https://{URL}/search?q={query}&categories=111&purity=100&sorting=relevance&order=desc"
    urlreq = requests.get(q)
    soup = bs4.BeautifulSoup(urlreq.text, 'lxml') # Complete html
    soupid = soup.findAll('h1') # picking up all the 'preview' classes
    results = int(soupid[0].text.split(" ")[0].replace(",","").replace(".","")) #how many results are
    pages = round(results/N_IMAGE_PAGES) 
    r_pages = results/N_IMAGE_PAGES

    if (pages - r_pages) < 0:
        pages = pages - 1 #how many pages are

    print(f"There are {results} wallpapers for '{query}' divided in {pages} pages (24 images each)")
    pas = True
    while pas:
        try:
            user_nro_pages = input(f"How many pages you want to download? (default = 1, max = {pages}) ")
            user_nro_pages = int(user_nro_pages)
            print(user_nro_pages)
            if user_nro_pages == 0 or user_nro_pages > pages:
                if user_nro_pages == 1:
                    print(f"Unfortunately you can only download 1 page")
                else:
                    print(f"Unfortunately you can only download from 1 up to {pages} pages")
            else:
                pas = False
        except ValueError:
            if not user_nro_pages:
                user_nro_pages = 1
                pas = False
            else:
                print("Please insert a valid number")
            pass

    sh.mkdir("-p", path)

    for nro_page in range(1, user_nro_pages + 1):
        print(f"Downloading: ({nro_page}/{user_nro_pages})")
        q = f"https://{URL}/search?q={query}&categories=111&purity=100&sorting=relevance&order=desc&page={nro_page}"
        urlreq = requests.get(q)
        soup = bs4.BeautifulSoup(urlreq.text, 'lxml') # Complete html
        soupid = soup.findAll('a', {'class': 'preview'}) # picking up all the 'preview' classes
        ids = list(map(lambda s: s["href"].split("/")[-1], soupid))
        for i in tqdm.tqdm(ids):
            urlimage = requests.get(f"https://wallhaven.cc/w/{i}")
            soup = bs4.BeautifulSoup(urlimage.text, 'lxml') # Complete html
            soupid = soup.findAll('img', {'id': 'wallpaper'}) # picking up all the 'preview' classes
            final_url = soupid[0]["src"]
            imgreq = requests.get(final_url) #image response
            if imgreq.status_code == 200:
                with open(path+"/"+os.path.basename(final_url), 'ab') as imageFile:
                    for chunk in imgreq.iter_content(1024):
                        imageFile.write(chunk)
    print("Download Complete! :D")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--query", help="what images should be about")
    parser.add_argument("-p", "--path", help="folder to save downloaded images")
    args = parser.parse_args()

    if args.query and args.path:
        query = args.query
        path = args.path
        if path[-1] == "/":
            main(query, path[0: -1])
        else:
            main(query, path)
    else:
        parser.print_help()