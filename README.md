# Discord QR Token Logger

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)

![GitHub](https://img.shields.io/github/license/9P9/Discord-QR-Token-Logger)
![GitHub contributors](https://img.shields.io/github/contributors/9P9/Discord-QR-Token-Logger)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=shields)](http://makeapullrequest.com)
![GitHub repo size](https://img.shields.io/github/repo-size/9P9/Discord-QR-Token-Logger)
![GitHub issues](https://img.shields.io/github/issues/9P9/Discord-QR-Token-Logger)
![GitHub pull requests](https://img.shields.io/github/issues-pr/9P9/Discord-QR-Token-Logger)

A python script that generates a scam nitro QR code which can grab a victim's authentication token if scanned. Developed to show how social engineering is performed. **For Educational Purposes Only**.

![Capture d’écran 2022-08-27 172232](https://user-images.githubusercontent.com/38190847/187040712-92f4c796-c655-47a2-abb2-7f4519d1dab7.png)

*If you're interested in knowing the powerlevel configuration to get this prompt, have a look at [this repo](https://github.com/billythegoat356/pystyle).*

# Table of contents

- [Usage](#usage)
  - [Without Discord features](#without-discord-features)
  - [With Discord features](#with-discord-features)
- [Installation](#installation)
  - [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

# 📈Usage

To use the script, you just need to launch it normally without updating any code line ! However there is **2 way** to use the script :

- [Without Discord features](#with)
- [With Discord features](#with-Discord-webhook-url)

## Without Discord features

Without discord features, you can only get target token, you must proceed as follows:

![image](https://user-images.githubusercontent.com/38190847/187048296-dd4b9c75-7c4d-476c-8cba-9c53a809d610.png)

## With Discord features

To use Discord features you will need to provide **webhook url** to prompt when requested:

![image](https://user-images.githubusercontent.com/38190847/187048386-1abda0d0-afa9-4a0a-a351-4e55b34398e7.png)

With this method you are able to get much more target information like:

- User token informations :
  - 👑 Username
  - 📧 Mail 
  - 📞 Phone 
  - 🤑 Nitro 
- Payment info :
  - 💳 Brand (Visa/Mastecard/paypal)
  - ℹ/📩 Last 4 or paypal mail
  - 📅 Expiration
- Billing adress :
  - 📛 Name
  - ⚡ Line 1
  - ❄ Line 2
  - 🏳 Country
  - 🚩 State
  - 🏙 City
  - 📮 Postal code

# 🛠Installation

For installation, you may need some dependencies,
You may need to follow these steps to avoid all python interpreter errors.

## Dependencies

- Chrome, **be sure to have the lattest version**.
- Python 9 or above
- Python module (launch **install_requirements.bat**)

After following all instructions, you can start the script 🥳.

# 💡Contributing

Your contributions are always welcome! if you contribute we will show your account in the README file ! Please have a look at the [contribution guidelines](CONTRIBUTING.md) first. 🎉

## Contributors ❤

<a href="https://github.com/9P9/Discord-QR-Token-Logger/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=9P9/Discord-QR-Token-Logger" />
</a>
<br>
<br>

> **Working on your first Pull Request?** You can learn how from this *free* series [How to Contribute to an Open Source Project on GitHub](https://kcd.im/pull-request)

# 📝License

The GNU General Public License v3.0 (GPL-3.0) 2022 - [mouadessalim](https://github.com/mouadessalim) & [9P9](https://github.com/9P9). Please have a look at the [LICENSE](LICENSE) for more details.
