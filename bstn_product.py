import datetime
import random
import time

import cloudscraper
from bs4 import BeautifulSoup


def getTimestamp(module):
    return '[' + str(datetime.datetime.now()) + '] ' + module + ': '


class bstnurltask():
    def __init__(self, prox, hook, delay, url):
        self.hook = hook
        self.delay = delay
        self.proxies = prox
        self.url = url
        print(getTimestamp('BSTN') + 'Starting URL task...')

    def get_random_ua(self):
        return random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        ])

    def task(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        }

        def getRandomProxy():
            proxy = random.choice(self.proxies)
            return proxy

        def validateProxy(proxy):
            proxyDict = {}
            proxySplit = proxy.split(':')
            if (len(proxySplit) != 4):
                proxyDict = {
                    'http': 'http://' + proxySplit[0] + ':' + proxySplit[1] + '/',
                    'https': 'https://' + proxySplit[0] + ':' + proxySplit[1] + '/'
                }
            else:
                proxyDict = {
                    'http': 'http://' + proxySplit[2] + ':' + proxySplit[3] + '@' + proxySplit[0] + ':' + proxySplit[
                        1] + '/',
                    'https': 'https://' + proxySplit[2] + ':' + proxySplit[3] + '@' + proxySplit[0] + ':' + proxySplit[
                        1] + '/'
                }
            return proxyDict

        def get2CapFormat(proxy):
            proxySplit = proxy.split(':')
            return proxySplit[2] + ':' + proxySplit[3] + '@' + proxySplit[0] + ':' + proxySplit[1]

        def saveUrl(list):
            with open('bstn_new.txt', 'w') as file_handler:
                for item in list:
                    file_handler.write("{}\n".format(item))
            print(getTimestamp('BSTN-HANDLER') + 'Succesfully updated database!')

        def checkResult(text):
            try:
                soup = BeautifulSoup(text, 'html.parser')
                picElmts = soup.find('ul', {'class': 'thumbnails'})
                picUrl = 'https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=' + \
                         picElmts.find('img')['src'] + '&container=focus'
                productName = str(soup.find('span', {'class': 'productname'}).text)
                productPrice = str(soup.find('span', {'class': 'price'}).text)
                sizeBlock = soup.select('div[class^=selectVariants]')
                sizeBl = sizeBlock.find_all('option', {'class': ''})
                for i in sizeBl:
                    if 'disabled' not in str(i):
                        size = str(i.text)
                        id = i['value']
                        print(size + ' # ' + id)
            except Exception as e:
                print(e)

        def productCheck():
            try:
                scraper = cloudscraper.create_scraper(interpreter='js2py', recaptcha={'provider': '2captcha',
                                                                                      'api_key': '140c4a7575cc2d22529359c728307d78',
                                                                                      'proxy': True})
                proxy = getRandomProxy()
                scraper.proxies = validateProxy(proxy)
                proxy2Cap = get2CapFormat(proxy)
                headers = {
                    'Referer': 'https://www.bstn.com',
                    'User-Agent': self.get_random_ua()
                }
                resp = scraper.get(self.url)
                html = resp.text
                if resp.status_code == 403:
                    if 'captcha' in html:
                        print(getTimestamp('BSTN') + 'Captcha detected!')
                        urlcap = 'http://2captcha.com/in.php?key=140c4a7575cc2d22529359c728307d78&method=userrecaptcha&googlekey=6LfBixYUAAAAABhdHynFUIMA_sa4s-XsJvnjtgB0&pageurl=https://www.bstn.com/'
                        resp = scraper.get(urlcap)

                        if resp.text[0:2] != 'OK':
                            quit('Service error. Error code:' + resp.text)

                        captcha_id = resp.text[3:]
                        fetch_url = 'http://2captcha.com/res.php?key=140c4a7575cc2d22529359c728307d78&action=get&id=' + captcha_id

                        for i in range(1, 10):
                            time.sleep(5)
                            resp = self.s.get(fetch_url)
                            if resp.text[0:2] == 'OK':
                                break
                        response = resp.text[3:]
                        print(getTimestamp('BSTN') + 'Captcha solved!')
                        parameters = {
                            'g-recaptcha-response': response
                        }
                        req = scraper.post('https://www.bstn.com/new-arrivals', data=parameters, headers=headers,
                                           proxies=proxy)
                        if req.status_code != 403:
                            print(getTimestamp('BSTN') + 'Captcha data posted with success!')
                            checkResult(req.text)
                        else:
                            print(getTimestamp('BSTN') + 'Captcha data denied')
                    if 'maximale Anzahl' in html:
                        print(getTimestamp('BSTN') + 'Too many users online!')
                else:
                    checkResult(html)
            except Exception as e:
                print(e)

        while (True):
            productCheck()
            time.sleep(self.delay)
