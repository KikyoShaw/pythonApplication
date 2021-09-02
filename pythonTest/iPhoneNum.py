# _*_ encoding:utf-8 _*_
# a tool to generate  vcard and parse vcard
#

import vobject
import requests
from bs4 import BeautifulSoup
import re


# create a vcard ---test
def create_vcard(phones):
    for phone in phones:
        j = vobject.vCard()
        j.add('fn')
        j.fn.value = phone
        j.add('tel')
        j.tel.type_param = 'CELL'
        j.tel.value = phones[phone]
        j.prettyPrint()
        with open('test.vcf', 'a') as f:
            f.write(j.serialize())


def search_zone():
    phones = []
    url = 'http://www.jihaoba.com/haoduan/184/beijing.htm'
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'lxml')
    phone_list = soup.find_all('li', 'hd-city01')
    pattern = re.compile('\d{7}')
    for phone in phone_list:
        if re.search(pattern, phone.string):
            phones.append(phone.string)

    print('find zone : %d' % len(phones))
    return phones


def genrate_phone():
    final_phones = {}
    phones = search_zone()
    for zone in phones:
        for i in range(1, 10):
            final_phone = zone + str(i) + "322"
            final_phones[str(zone) + str(i)] = final_phone
    return final_phones


if __name__ == "__main__":
    print('hello world !!')
    phones = genrate_phone()
    create_vcard(phones)
    print('length%d\t' % len(phones))