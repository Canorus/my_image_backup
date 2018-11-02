 #!/usr/local/bin/python3.6
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import urllib.request
#from urllib.request import urlopen
import requests
import re
import os
import datetime

userid = input('Please input your user id: ')
pw = input('Please input your password: ')
base = os.getcwd()+'/'
d = datetime.datetime.today()
# setting chrome driver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(base+'chromedriver', options=options)
driver.implicitly_wait(3)

# login credential
driver.get('https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&ru=')
driver.find_element_by_name('userid').send_keys(userid)
driver.find_element_by_name('pass').send_keys(pw)
driver.find_element_by_id('sgnBt').click()
 
# myPurchsesHistory
driver.get('https://www.ebay.com/myb/PurchaseHistory')
html = driver.page_source
f = open(base+'purchase_history.html','w')
f.write(html)
f.close()

# now let's drill urls
# before that let's define download function

def getimage(url, name):
    urllib.request.urlretrieve(url, name)
    print('saving: '+name)

purchase_dic = dict()

# parsing data from purchase history

soup = bs(html,'html.parser')
li = soup.find_all(attrs={"class":"result-set-r"})
li1 = bs(str(li[1]),'html.parser')
for i in li1.find_all('a',attrs={"class":"item-title"}):
    purchase_dic[i.get_text()] = i['href']

# retrieving each url

for i in purchase_dic:
    istr = str(i).replace('/','')
    if os.path.exists(base+istr):
        pass
    else:
        os.mkdir(base+istr)
        fw = open(base+istr+'/'+str(d.year)+'-'+str(d.month)+'-'+str(d.day)+'-'+istr+'.html','w')
        req = purchase_dic[i]
        driver.get(req)
        page_source = driver.page_source
        try:
            req = bs(page_source, 'html.parser').find_all('a',text='See original listing')[0]['href'] # point req to Original listing url
            print(i+': See original listing detected')
            driver.get(req)
            page_source = driver.page_source
        except:
            print(i+': error occured while re-routing req url')
        driver.implicitly_wait(3)
        page_source = bs(driver.page_source,'html.parser') # original listing page source
        fw.write(str(page_source))
        fw.close()
        imgre = re.compile('s-l(64|500).jpg')
        imgsrc = page_source.find_all('img',attrs={'src':imgre})
        for v,k in enumerate(imgsrc):
            print(str(v)+': '+imgre.sub('s-l1600.jpg',str(k['src'])))
            getimage(imgre.sub('s-l1600.jpg',str(k['src'])),base+istr+'/'+istr+str(v)+'.jpg')
driver.close()
