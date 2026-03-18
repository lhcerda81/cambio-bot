import requests
import time
from datetime import datetime
import pandas as pd

from db import init_db, salvar, conn
from analysis import variacao, prever

# CONFIG
TOKEN = "SEU_TOKEN"
CHAT_ID = "SEU_CHAT_ID"

def enviar(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_cotacao():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL"
    r = requests.get(url)
    data = r.json()

    usd = float(data["USDBRL"]["bid"])
    eur = float(data["EURBRL"]["bid"])

    return usd, eur

init_db()

usd_inicio = None
eur_inicio = None
dia = datetime.now().day

print("🚀 Sistema de câmbio iniciado...")

while True:
    try:
        now = datetime.now()

        # reset diário
        if now.day != dia:
            usd_inicio = None
            eur_inicio = None
            dia = now.day

        usd, eur = get_cotacao()

        salvar("USD", usd)
        salvar("EUR", eur)

        # define início do dia
        if usd_inicio is None:
            usd_inicio = usd
            eur_inicio = eur

        var_usd = variacao(usd_inicio, usd)
        var_eur = variacao(eur_inicio, eur)

        print(f"{now} | USD: {usd} ({var_usd:.2f}%) | EUR: {eur} ({var_eur:.2f}%)")

        # ALERTA ±3%
        if abs(var_usd) >= 3:
            enviar(f"🚨 USD variou {var_usd:.2f}% hoje\nValor: R$ {usd}")

        if abs(var_eur) >= 3:
            enviar(f"🚨 EUR variou {var_eur:.2f}% hoje\nValor: R$ {eur}")

        # PROJEÇÃO
        df = pd.read_sql("SELECT * FROM cotacoes WHERE moeda='USD'", conn)
        prev = prever(df)

        if prev:
            enviar(f"📊 Projeção USD:\nDia1: {prev[0]:.2f}\nDia2: {prev[1]:.2f}")

        time.sleep(300)

    except Exception as e:
        print("Erro:", e)
        time.sleep(60)
