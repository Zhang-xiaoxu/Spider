import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool

#?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=3&from=gallery
def gar_page(offset):
    '''
    请求参数
    '''
    params = {
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'3',
        'from':'gallery',
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(type(response))
            print(response.text)
            return response.json()

    except requests.ConnectionError:
        return None

def get_images(json):
    if json.get('data'):
        for item in json.get('data'): #将json文件中key值为data的值取出来，并进行遍历
            title = item.get('title') #将遍历的每个对象中的key为title的值赋给title
            images = item.get('image_list') #image_list的值付给images
            if images:
                for image in images: #images进行遍历
                    yield {
                        'image':image.get('url'), #取出每张图片地址
                        'title':title
                    }




def save_image(item):
    '''
    下载图片并保存
    '''
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        local_image_url = item.get('image')
        new_image_url = local_image_url.replace('list', 'large')
        response = requests.get('http:' + new_image_url)
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded',file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')






def main(offset):
    json = gar_page(offset)

    for item in get_images(json):
        print(item)
        save_image(item)


GROUP_START = 1
GROUP_END = 5
if __name__ == '__main__':

    pool = Pool()
    groups = ([x*20 for x in range(GROUP_START,GROUP_END+1)])
    pool.map(main,groups)
    pool.close()
    pool.join()
