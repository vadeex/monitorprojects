import datetime
import threading

webhookUrl = 'https://discordapp.com/api/webhooks/667721465055150080/5fkJheldTQfscOMUyLkNVymTvMpIi5AitqXKrsY1biMCEELEGSY0tO3am0g--XY4WjWv'
bstnWebhook = 'https://discordapp.com/api/webhooks/668809787630419969/iSCxr-BCYIcge3-LzXHsnTeFymGqygOiaeGsmMYocFjVTvReE1O2Wn-yyYg8HpN_dlT1'


def getTimestamp():
    return '[' + str(datetime.datetime.now()) + '] '


if __name__ == '__main__':
    from bstn_product import bstnurltask

    try:
        proxies = open('rotating.txt').read().splitlines()
        print(getTimestamp() + 'Successfully loaded ' + str(proxies.__len__()) + ' proxies')
        # taskNew = monitorTask(proxies, bstnWebhook, 2)
        # threading.Thread(target=taskNew.task).start()
        taskBstnUrl = bstnurltask(proxies, bstnWebhook, 2,
                                  'https://www.bstn.com/en/p/nike-react-element-55-se-cd2153-100-167370')
        threading.Thread(target=taskBstnUrl.task).start()
    except Exception as e:
        print(e)
