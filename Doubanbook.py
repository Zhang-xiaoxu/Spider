from bs4 import BeautifulSoup
import requests
url = 'https://book.douban.com/top250?icn=index-book250-all'
urls = ['https://book.douban.com/top250?start={}'.format(str(n)) for n in range(0,250,25)]

def get_book(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text,'lxml')
    titles = soup.select('div.pl2 > a')
    imgs = soup.select('a.nbg > img')
    cates = soup.select('p.quote > span')
    for title,img,cate in zip(titles,imgs,cates):
        data = {
            'title':title.get_text(),
            'img':img.get('src'),
            'cate':cate.get_text()
        }
        print(data)

for url_urls in urls:
    get_book(url_urls)