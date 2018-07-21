import requests
from lxml import etree
class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session() #request的session方法可以维持一个会话


    def token(self):
        '''
        session自动处理Cookies，
        提取页面代码中的隐藏表单token
        :return: token
        '''
        response = self.session.get(self.login_url,headers = self.headers)
        seletor = etree.HTML(response.text)
        token = seletor.xpath('//div//input[2]/@value')[0]
        return token

    def login(self, email, password):
        '''
        模拟登录
        :param email:
        :param password:
        :return:
        '''
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }

        response = self.session.post(self.post_url,data=post_data, headers = self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)

        response = self.session.get(self.logined_url,headers = self.headers)
        if response.status_code == 200:
            self.profile(response.text)

    def dynamics(self, html):
        '''获取动态信息'''
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class,"news")]//div[contains(@class,"alert")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
            print(dynamic)

    def profile(self, html):
        '''获取个人中心的用户名和邮箱'''
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value=""]/text()')
        print(name,email)

if __name__ == '__main__':
    login = Login()
    login.login(email='961512586@qq.com',password='zhangxiaoxu123')