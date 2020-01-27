import datetime
import random
import time

import cloudscraper
from bs4 import BeautifulSoup

from discord_hooks import Webhook


def getTimestamp(module):
    return '[' + str(datetime.datetime.now()) + '] ' + module + ': '


class monitorTask():
    def __init__(self, prox, hook, delay):
        self.hook = hook
        self.delay = delay
        self.proxies = prox
        print(getTimestamp('BSTN') + 'Starting task...')

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
                newUrls = []
                changed = False
                soup = BeautifulSoup(text, 'html.parser')
                links = open('bstn_new.txt').read().splitlines()
                products = soup.find_all('li', {'class': 'item'})
                for i in products:
                    picUrl = 'https://images1-focus-opensocial.googleusercontent.com/gadgets/proxy?container=focus&url=' + \
                             i.find('img')['src'] + '&container=focus'
                    elmt = i.find('div', {'class': 'pText'})
                    productName = elmt.find('a')['title']
                    productUrl = 'https://www.bstn.com' + elmt.find('a')['href']
                    if productUrl not in links:
                        newUrls.append(productUrl)
                        changed = True
                        productPrice = elmt.find('span', {'class': 'price'}).text
                        # if 'newprice' in str(elmt):
                        # productPrice = elmt2.find('span', {'class': 'newprice'}).text.replace(' ', '')
                        # else:
                        # productPrice = elmt2.find('span', {'class': 'price'}).text.replace(' ', '')
                        print(getTimestamp('BSTN') + 'New Product loaded -> ' + productUrl)
                        sizes = ''
                        if 'Variants' in str(elmt):
                            elmt3 = elmt.find('ul', {'class': 'availableVariants'})
                            if 'li' in str(elmt3):
                                sizeBlocks = elmt3.find_all('li')
                                for s in sizeBlocks:
                                    if 'soldout' not in str(s):
                                        atcLink = 'https://www.bstn.com' + s.find('a')['href']
                                        size = str(s.find('a').text).replace(",", ".")
                                        if not sizes:
                                            sizes = size + ': [**[ATC]**](' + atcLink + ')'
                                        else:
                                            sizes += ',' + size + ': [**[ATC]**](' + atcLink + ')'
                        embed = Webhook(self.hook, color=0xff003a)
                        embed.set_title(title='**BSTN**')
                        embed.set_desc('**[NEW: ' + productName + '](' + productUrl + ')**')
                        embed.add_field(name='Price', value='**' + str(productPrice).replace('\n', '') + '**',
                                        inline=False)
                        embed.set_thumbnail(url=picUrl)
                        embed.set_footer(text='brought to you by @EscapeNotify',
                                         icon='https://cdn.discordapp.com/attachments/632664568400838699/636226829660717076/testtest.png',
                                         ts=True)
                        split = sizes.split(',')
                        count = 0
                        run = 0
                        sis = ''
                        for i in split:
                            if count <= 4:
                                sis += str(i) + '\n'
                            if count == 4 or run == len(split) - 1:
                                embed.add_field(name='Sizes', value=sis, inline=False)
                                sis = ''
                                count = 0
                            count += 1
                            run += 1
                        embed.post()
                    else:
                        newUrls.append(productUrl)
                if changed:
                    print(getTimestamp('BSTN-HANDLER') + 'Found database changes. Updating database...')
                    saveUrl(newUrls)
                    changed = False
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
                resp = scraper.get(
                    'https://www.bstn.com/en/footwear/filter/__brand_adidas.jordan.nike/page/1/sort/date_new')
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
