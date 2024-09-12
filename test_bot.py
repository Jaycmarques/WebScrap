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
            "span", class_="a-offscreen")
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
    target_url = "https://www.amazon.com.br/Fralda-Pants-Premium-Pampers-Pacote/dp/B07X83FF8X/ref=sr_1_6?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2LUM3OSBHFJKW&dib=eyJ2IjoiMSJ9.HI0AJEPt4zL6Z1u120QdrepTnqaKIF__Vu2wj0y2OIbIcuV4o_Ce8Cv85b6gKF3ekDFg921vyEpLGoOqvsAmzRFmOWRT8Q3OH-CoxjKsH19Ymts1ulmckEFxFC5x4lJjPWl-6TM5RFMcx1IFl8VRDosP43DT7-Y2mMeK5VfwntZoKwNRJRqVubYxTU3U7ts85lN_2lu2IrIz20wgIi7XwSDoDBbSnfJnDgDGfvFFs05cYoBgTPctmkQdbOodUSGF1YPE5Yd7Kwa6gdgyP9U_tdWvqwg-9k6J3AEBtnE8GTo.hoTUsO6BCsmfKTjVkbjptTaRQiGEnYGRa0LdZURRnm0&dib_tag=se&keywords=xxg+60+pampers&qid=1726089642&s=hpc&sprefix=xxg+60+pampers%2Chpc%2C172&sr=1-6&ufe=app_do%3Aamzn1.fos.a492fd4a-f54d-4e8d-8c31-35e0a04ce61e"
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
