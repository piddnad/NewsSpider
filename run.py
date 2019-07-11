import os

print(os.system("scrapy crawl technews -o news.csv -t csv"))
