# QR Discord Token Grabber
A python script that generates a scam nitro QR code which can grab a victim's authentication token if scanned. Developed to show how social engineering is performed; use for educational purposes only.

![img1](https://i.ibb.co/BL2Q0jz/Screenshot-527.png)

## Demonstration

![qr-code](https://user-images.githubusercontent.com/75003671/117522092-fd79ff80-afe3-11eb-938c-23dd68d5927c.gif)

## Usage
1. This project requires [Python >= 3.7.6](https://python.org). When installing Python, make sure to check the *ADD TO PATH* checkbox.

2. Run the `[1] install_requirements.bat` file.

3. Unzip the `browser.7z` file so that the browser folder is in the same directory as the `[2] run.bat` file.

4. Run the `[2] run.bat` file.

5. Input your discord webhook link (this link is used to post the authentication token to a channel). Note that, even if you do not input a webhook link, you will still receive the token when it is printed to the console, but note that you will lose this token once the program is closed!

6. Wait for `discord_gift.png` to be generated. Then, send the image to a victim for them to scan it. Note that the QR code is only valid for approximately two minutes after creation.

7. When the QR code is scanned, you will be logged onto their account and receive their discord authentication token.

## Need extra help?

[Join the discord server for support!](https://discord.gg/a24Sp9bEXu)
