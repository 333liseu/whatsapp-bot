@app.post("/whatsapp")
async def whatsapp_webhook(Body: str = Form(...)):
    msg = normalizar_texto(Body)
    print(f"📩 Mensagem recebida (normalizada): {msg}")
    response = MessagingResponse()
    message = response.message()

    if msg in ["preco btc", "preço btc"]:  # Agora aceita ambas as formas
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
