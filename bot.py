import requests
import time
from datetime import datetime

import os

TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

NIVEIS = [1, 2, 3]  # percentuais para alerta

def get_cotacao():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL"
    r = requests.get(url)
    data = r.json()
    usd = float(data["USDBRL"]["bid"])
    eur = float(data["EURBRL"]["bid"])
    return usd, eur

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

usd_inicio = None
eur_inicio = None

alertas_usd_enviados = set()
alertas_eur_enviados = set()

dia_atual = datetime.now().day

print("🚀 Agente PRO de câmbio iniciado...")

while True:
    try:
        agora = datetime.now()

        # 🔄 Novo dia → reset
        if agora.day != dia_atual:
            usd_inicio = None
            eur_inicio = None
            alertas_usd_enviados.clear()
            alertas_eur_enviados.clear()
            dia_atual = agora.day
            print("🔄 Novo dia iniciado.")

        usd, eur = get_cotacao()

        if usd_inicio is None:
            usd_inicio = usd
            eur_inicio = eur
            print(f"📌 Início do dia - USD: {usd_inicio} | EUR: {eur_inicio}")

        variacao_usd = ((usd - usd_inicio) / usd_inicio) * 100
        variacao_eur = ((eur - eur_inicio) / eur_inicio) * 100

        print(f"{agora} | USD: {usd} ({variacao_usd:.2f}%) | EUR: {eur} ({variacao_eur:.2f}%)")

        # 📈📉 Verifica níveis
        for nivel in NIVEIS:
            # Alta USD
            if variacao_usd >= nivel and f"+{nivel}" not in alertas_usd_enviados:
                enviar(f"📈 Dólar subiu +{nivel}% hoje!\nAtual: R$ {usd}\nVariação: {variacao_usd:.2f}%")
                alertas_usd_enviados.add(f"+{nivel}")

            # Queda USD
            if variacao_usd <= -nivel and f"-{nivel}" not in alertas_usd_enviados:
                enviar(f"📉 Dólar caiu -{nivel}% hoje!\nAtual: R$ {usd}\nVariação: {variacao_usd:.2f}%")
                alertas_usd_enviados.add(f"-{nivel}")

            # Alta EUR
            if variacao_eur >= nivel and f"+{nivel}" not in alertas_eur_enviados:
                enviar(f"📈 Euro subiu +{nivel}% hoje!\nAtual: R$ {eur}\nVariação: {variacao_eur:.2f}%")
                alertas_eur_enviados.add(f"+{nivel}")

            # Queda EUR
            if variacao_eur <= -nivel and f"-{nivel}" not in alertas_eur_enviados:
                enviar(f"📉 Euro caiu -{nivel}% hoje!\nAtual: R$ {eur}\nVariação: {variacao_eur:.2f}%")
                alertas_eur_enviados.add(f"-{nivel}")

        time.sleep(60)

    except Exception as e:
        print("Erro:", e)
        time.sleep(30)
