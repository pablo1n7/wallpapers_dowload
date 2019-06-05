# Wallpapers Downloader

How to use:

1 - Install the dependencies:

    pip install -r requirements.txt

2 - Run the following command:

    python downloader.py -q QUERY -p DOWNLOAD_PATH

For example:
    
    python downloader.py -q sci -p images/

3 - It has a help argument too:

    python downloader.py -h

    usage: downloader.py [-h] [-q QUERY] [-p PATH]

    optional arguments:
      -h, --help            show this help message and exit
      -q QUERY, --query QUERY
                            what images should be about
      -p PATH, --path PATH  folder to save downloaded images

Based on: https://github.com/Princeyadav05/WallsCrawler.git