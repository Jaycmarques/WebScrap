import requests
from bs4 import BeautifulSoup
from telegram import Bot
from decouple import config
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Configurações do Telegram
telegram_token = config('TELEGRAM_TOKEN')
chat_id = config('CHAT_ID', cast=int)

# Função para verificar o preço


def check_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança um erro para códigos de status HTTP 4xx/5xx

        soup = BeautifulSoup(response.content, 'html.parser')

        # Verifique o conteúdo da página para entender o motivo do erro
        # Exibe os primeiros 500 caracteres para depuração
        print("Conteúdo da página:", soup.prettify()[:500])

        # Encontrar o preço usando a classe CSS fornecida
        price_tag = soup.find(
            "span", class_="vtex-store-components-3-x-currencyInteger")
        if price_tag:
            price_text = price_tag.text.strip()
            # Processar o texto do preço
            # Remove "R$" e espaços extras, e substitui vírgula por ponto para conversão
            price = price_text.replace('R$', '').replace(
                '.', '').replace(',', '.').strip()
            try:
                return float(price)
            except ValueError:
                print("Erro ao converter o preço para float.")
                return None
        else:
            print("Tag de preço não encontrada.")
            return None
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
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
    target_url = "https://www.paguemenos.com.br/fralda-pampers-pants-ajuste-total-xxg-60-unidades/p?idsku=54401"
    price_target = 140.00  # Defina seu preço alvo

    price = check_price(target_url)
    if price is not None:
        print(f"Preço encontrado: R${price:.2f}")

        if price < price_target:
            mensagem = f"""O preço caiu! Melhor preço atual: R${price:.2f}
Compre aqui: {target_url}"""
            await send_telegram_message(mensagem, chat_id, telegram_token)
        else:
            print(f"O preço não atingiu o alvo. Preço atual: R${price:.2f}")
    else:
        print("Não foi possível encontrar o preço.")

# Configuração do agendador assíncrono


async def main():
    scheduler = AsyncIOScheduler()
    # Ajuste o intervalo conforme necessário
    scheduler.add_job(monitorar_preco, 'interval', seconds=30)
    scheduler.start()
    while True:
        await asyncio.sleep(30)  # Manter o loop do evento rodando

if __name__ == "__main__":
    asyncio.run(main())
