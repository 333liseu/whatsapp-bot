from fastapi import FastAPI, Form
from twilio.twiml.messaging_response import MessagingResponse
import uvicorn
import requests
import unicodedata

# Inicializa o app FastAPI
app = FastAPI()

# Função para normalizar o texto (remove acentos e transforma em minúsculas)
def normalizar_texto(texto: str) -> str:
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto.lower().strip()

# Função para buscar o preço atual do BTC
def get_btc_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd,brl')
        data = response.json()
        price_usd = f"${data['bitcoin']['usd']:,.2f}"
        price_brl = f"R${data['bitcoin']['brl']:,.2f}"
        return price_usd, price_brl
    except Exception as e:
        print(f"❌ Erro ao buscar o preço do BTC: {e}")
        return "⚠️ Erro ao obter o preço do BTC.", None

# Rota de teste para confirmar que o servidor está rodando
@app.get("/")
async def root():
    return {"message": "✅ Bot WhatsApp rodando na Render.com!"}

# Endpoint do webhook do WhatsApp
@app.post("/whatsapp")
async def whatsapp_webhook(Body: str = Form(...)):
    msg = normalizar_texto(Body)
    print(f"📩 Mensagem recebida (normalizada): {msg}")
    response = MessagingResponse()
    message = response.message()

    # Responde aos comandos "preço BTC" e "dca carteira"
    if msg in ["preco btc", "preço btc"]:  # Aceita ambas as formas com e sem acento
        price_usd, price_brl = get_btc_price()
        if price_brl:
            message.body(f"📈 O preço **atual** do BTC é:\n💵 USD: {price_usd}\n🇧🇷 BRL: {price_brl}")
        else:
            message.body("⚠️ Erro ao obter o preço do BTC.")
    elif msg == "dca carteira":
        message.body("💰 Sugiro comprar 10% em BTC com base nas análises atuais.")
    else:
        message.body("🤖 Comando não reconhecido. Tente: 'preço BTC' ou 'DCA carteira'.")

    return str(response)

# Inicia o servidor quando rodado diretamente
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
