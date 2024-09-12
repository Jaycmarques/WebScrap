import requests
from bs4 import BeautifulSoup
from telegram import Bot
from decouple import config
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Configurações do Telegram
telegram_token = config('TELEGRAM_TOKEN')
chat_id = config('CHAT_ID', cast=int)

sites = [
    {
        'url': "https://www.amazon.com.br/Fralda-Pants-Premium-Pampers-Pacote/dp/B07X83FF8X/ref=sr_1_6?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2LUM3OSBHFJKW&dib=eyJ2IjoiMSJ9.HI0AJEPt4zL6Z1u120QdrepTnqaKIF__Vu2wj0y2OIbIcuV4o_Ce8Cv85b6gKF3ekDFg921vyEpLGoOqvsAmzRFmOWRT8Q3OH-CoxjKsH19Ymts1ulmckEFxFC5x4lJjPWl-6TM5RFMcx1IFl8VRDosP43DT7-Y2mMeK5VfwntZoKwNRJRqVubYxTU3U7ts85lN_2lu2IrIz20wgIi7XwSDoDBbSnfJnDgDGfvFFs05cYoBgTPctmkQdbOodUSGF1YPE5Yd7Kwa6gdgyP9U_tdWvqwg-9k6J3AEBtnE8GTo.hoTUsO6BCsmfKTjVkbjptTaRQiGEnYGRa0LdZURRnm0&dib_tag=se&keywords=xxg+60+pampers&qid=1726089642&s=hpc&sprefix=xxg+60+pampers%2Chpc%2C172&sr=1-6&ufe=app_do%3Aamzn1.fos.a492fd4a-f54d-4e8d-8c31-35e0a04ce61e",
        'price_class': "a-price-whole"
    },
    {
        'url': "https://www.paguemenos.com.br/fralda-pampers-pants-ajuste-total-xxg-60-unidades/p?idsku=54401",
        'price_class': "vtex-store-components-3-x-currencyInteger"
    },
    {
        'url': "https://www.bistek.com.br/fralda-pampers-pants-xxg-c60-2122383/p",
        'price_class': "vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--pdp"
    },
    {
        'url': "https://www.saojoaofarmacias.com.br/fralda-pampers-pants-ajuste-total-xxg-60-unidades-10001069/p?idsku=9437&gclid=CjwKCAjw3P-2BhAEEiwA3yPhwKaBsU8DQcbiw8LaxkIAdux1xp4loQz6imvDxC0hjKYoqi9D4fXAJxoCcG4QAvD_BwE",
        'price_class': "sjdigital-custom-apps-5-x-currencyInteger"
    }
]


def check_price(url, price_class):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_tag = soup.find("span", {"class": price_class})
    if price_tag:
        try:
            price = float(price_tag.text.replace('R$', '').replace(
                '.', '').replace(',', '.').strip())
            return price
        except ValueError:
            return None
    return None

# Função assíncrona para enviar mensagem pelo Telegram


async def send_telegram_message(message, chat_id, token):
    bot = Bot(token=token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print("Mensagem enviada com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar a mensagem: {e}")

# Função principal que verifica os preços e envia notificação


async def monitorar_preco():
    prices = []

    for site in sites:
        price = check_price(site['url'], site['price_class'])
        if price is not None:
            prices.append((price, site['url']))

    if prices:
        best_price, best_url = min(prices, key=lambda x: x[0])
        print(f"Melhor preço atual: R${best_price:.2f}")
        print(f"URL do melhor preço: {best_url}")

        price_target = 129.00  # Defina seu preço alvo
        if best_price < price_target:
            mensagem = f"""O preço caiu! Melhor preço atual: R${best_price:.2f}
Compre aqui: {best_url}"""
            await send_telegram_message(mensagem, chat_id, telegram_token)

# Configuração do agendador assíncrono


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(monitorar_preco, 'interval', minutes=30)
    scheduler.start()
    while True:
        await asyncio.sleep(1800)  # Manter o loop do evento rodando

if __name__ == "__main__":
    asyncio.run(main())
