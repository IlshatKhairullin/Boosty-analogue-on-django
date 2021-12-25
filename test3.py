import requests
from bs4 import BeautifulSoup

class Exchange_Rates:

    def Dollar():
        DOLLAR_RUB = 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%B0%D1%80+&aqs=chrome.1.69i57j0i67i433j0i10i433j0i67i131i433i457j0i67j0i67i433j0i10i433l3j0i512.1779j1j15&sourceid=chrome&ie=UTF-8'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'} # описание пользователя, если не передать будет считаться, что заходит бот. My user agent

        full_page = requests.get(DOLLAR_RUB, headers=headers)  # попытка извлечения данных из ресурса

        soup = BeautifulSoup(full_page.content, 'html.parser')  # content - нахождение кодировки страницы

        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert[0].text

    def Eur():
        Eur_RUB = 'https://www.google.com/search?q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%B2+%D1%80%D1%83%D0%B1&sxsrf=AOaemvK4n_37kOrsRXbVjxYKyytVi0GIWQ%3A1639208012513&ei=TFS0YfLeHpDbrgSUxoDYAg&oq=%D0%B5%D0%B2%D1%80%D0%BE+&gs_lcp=Cgdnd3Mtd2l6EAMYADIMCAAQsQMQQxBGEIICMggIABCABBCxAzIECAAQQzIICAAQgAQQsQMyDQgAEIAEEIcCELEDEBQyBQgAEIAEMgQIABBDMgUIABCxAzIFCAAQgAQyBQgAEIAEOgoIABCABBCHAhAUOgsIABCABBCxAxCDAToLCC4QgAQQxwEQ0QM6CwguEIAEEMcBEKMCOgsILhCABBCxAxCDAToJCAAQQxBGEIICSgQIQRgASgQIRhgAUABY_w1g3xVoAXACeACAAWuIAbMEkgEDNS4xmAEAoAEBwAEB&sclient=gws-wiz'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

        full_page = requests.get(Eur_RUB, headers=headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
        return convert[0].text

class Banks:

    def Dollar2(num):
        DOLLAR_RUB = 'https://www.banki.ru/products/currency/cash/usd/kazan~/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

        full_page = requests.get(DOLLAR_RUB, headers=headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll('div', {'class': 'currency-table__large-text'})

        if num == 0:
            return convert[0].text  # 0 - ЦБ 1 - покупка 2 - продажа
        elif num == 1:
            return convert[1].text
        else:
            return convert[2].text

    def Euro2(num):
        EURO_RUB = 'https://www.banki.ru/products/currency/cash/eur/kazan~/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

        full_page = requests.get(EURO_RUB, headers=headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll('div', {'class': 'currency-table__large-text'})

        if num == 0:
            return convert[0].text  # 0 - ЦБ 1 - покупка 2 - продажа
        elif num == 1:
            return convert[1].text
        else:
            return convert[2].text

    def Dollar_bank(num):
        DOLLAR_RUB = 'https://www.banki.ru/products/currency/cash/usd/kazan~/'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

        full_page = requests.get(DOLLAR_RUB, headers=headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll('div', {'class': 'currency-table__rate__text'})

        if num == 1:
            return convert[1].text
        else:
            return convert[2].text

    def Euro_bank(num):
        EURO_RUB = 'https://www.banki.ru/products/currency/cash/eur/kazan~/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

        full_page = requests.get(EURO_RUB, headers=headers)

        soup = BeautifulSoup(full_page.content, 'html.parser')

        convert = soup.findAll('div', {'class': 'currency-table__rate__text'})

        if num == 1:
            return convert[1].text
        else:
            return convert[2].text
