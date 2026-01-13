import time

# ... (todo tu código anterior) ...

if __name__ == "__main__":
    print("Esperando 10 segundos para evitar Error 409...")
    time.sleep(10) # Este retraso permite que Telegram cierre la sesión vieja
    while True:
        try:
            print("Bot conectado y listo para el Mapa 4")
            bot.polling(non_stop=True, interval=2, timeout=20)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)
