import requests
from bs4 import BeautifulSoup
from telegram import Bot
from decouple import config
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Configurações do Telegram
telegram_token = config('TELEGRAM_TOKEN')
chat_id = config('CHAT_ID', cast=int)

# Função para verificar o preço de um site específico


def check_price_site1():
    url = "https://www.panvel.com/panvel/fralda-pampers-pants-bag-ajuste-total-xxg-com-60-unidades/p-115484"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_tag = soup.find("span", {"class": "deal-price ng-star-inserted"})
    if price_tag:
        price = float(price_tag.text.replace('R$', '').replace(
            '.', '').replace(',', '.').strip())
        return price, url
    return None, None


def check_price_site2():
    url = "https://www.paguemenos.com.br/fralda-pampers-pants-ajuste-total-xxg-60-unidades/p?idsku=54401"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_tag = soup.find(
        "span", {"class": "vtex-store-components-3-x-currencyInteger"})
    if price_tag:
        price = float(price_tag.text.replace('R$', '').replace(
            '.', '').replace(',', '.').strip())
        return price, url
    return None, None


def check_price_site3():
    url = "https://www.bistek.com.br/fralda-pampers-pants-xxg-c60-2122383/p"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_tag = soup.find("span", {
                          "class": "vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--pdp"})
    if price_tag:
        price = float(price_tag.text.replace('R$', '').replace(
            '.', '').replace(',', '.').strip())
        return price, url
    return None, None


def check_price_site4():
    url = "https://www.saojoaofarmacias.com.br/fralda-pampers-pants-ajuste-total-xxg-60-unidades-10001069/p?idsku=9437&gclid=CjwKCAjw3P-2BhAEEiwA3yPhwKaBsU8DQcbiw8LaxkIAdux1xp4loQz6imvDxC0hjKYoqi9D4fXAJxoCcG4QAvD_BwE"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_tag = soup.find(
        "span", {"class": "sjdigital-custom-apps-5-x-currencyInteger"})
    if price_tag:
        price = float(price_tag.text.replace('R$', '').replace(
            '.', '').replace(',', '.').strip())
        return price, url
    return None, None

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

    price1, url1 = check_price_site1()
    if price1:
        prices.append((price1, url1))

    price2, url2 = check_price_site2()
    if price2:
        prices.append((price2, url2))

    price3, url3 = check_price_site3()
    if price3:
        prices.append((price3, url3))

    price4, url4 = check_price_site4()
    if price4:
        prices.append((price4, url4))

    if prices:
        best_price, best_url = min(prices, key=lambda x: x[0])
        print(f"Melhor preço atual: R${best_price:.2f}")
        print(f"URL do melhor preço: {best_url}")

        preco_alvo = 129.00  # Defina seu preço alvo
        if best_price < preco_alvo:
            mensagem = f"""O preço caiu! Melhor preço atual: R${best_price:.2f}
Compre aqui: {best_url}"""
            await send_telegram_message(mensagem, chat_id, telegram_token)

# Configuração do agendador assíncrono


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(monitorar_preco, 'interval', hours=8)
    scheduler.start()
    while True:
        await asyncio.sleep(28800)  # Manter o loop do evento rodando

if __name__ == "__main__":
    asyncio.run(main())
