from fastapi import FastAPI, Form
from twilio.twiml.messaging_response import MessagingResponse
import uvicorn
import requests

app = FastAPI()

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

@app.get("/")
async def root():
    return {"message": "Bot WhatsApp rodando na Render.com!"}

@app.post("/whatsapp")
async def whatsapp_webhook(Body: str = Form(...)):
    print(f"📩 Mensagem recebida do Twilio: {Body}")  # LOG DE DEBUG
    msg = Body.strip().lower()

    response = MessagingResponse()
    message = response.message()

    if msg == "preço btc":
        price_usd, price_brl = get_btc_price()
        if price_brl:
            print(f"✅ Resposta enviada: USD: {price_usd} | BRL: {price_brl}")  # LOG DE DEBUG
            message.body(f"📈 O preço **atual** do BTC é:\n💵 USD: {price_usd}\n🇧🇷 BRL: {price_brl}")
        else:
            message.body("⚠️ Erro ao obter o preço do BTC.")
    elif msg == "dca carteira":
        print("✅ Resposta enviada: DCA recomendada.")  # LOG DE DEBUG
        message.body("💰 Sugiro comprar 10% em BTC com base nas análises atuais.")
    else:
        print(f"⚠️ Comando não reconhecido: {msg}")  # LOG DE DEBUG
        message.body("🤖 Comando não reconhecido. Tente: 'preço BTC' ou 'DCA carteira'.")

    return str(response)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
        
