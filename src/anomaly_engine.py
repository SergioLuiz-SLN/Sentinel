import yfinance as yf
import time
from datetime import datetime
import os
import json


def carregar_config():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(src_dir)
    config_path = os.path.join(root_dir, "config", "config_motor.json")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def processar_ativos():

    config = carregar_config()
    tickers = config["parametros"]["ativos"]

    src_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(src_dir)

    caminho_log = os.path.join(root_dir, "data", "log_sistema.txt")

    os.makedirs(os.path.dirname(caminho_log), exist_ok=True)

    horario_motor = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open(caminho_log, "w", encoding="utf-8") as f:

        f.write(f"MOTOR:{horario_motor}\n")

        for ticker in tickers:

            try:

                stock = yf.Ticker(ticker)

                hist = stock.history(period="2mo")

                hist = hist.tail(20)

                mediana = int(hist["Volume"].median())

                if hist.empty:
                    continue

                ultimo_candle = hist.iloc[-1]

                data_yahoo = hist.index[-1].strftime("%d/%m/%Y")

                volume_atual = int(ultimo_candle["Volume"])

                mediana = int(hist["Volume"].median())

                limite = int(mediana * 1.5)

                preco = round(float(ultimo_candle["Close"]), 2)

                status = "🚨 ANOMALIA" if volume_atual > limite else "✅ NORMAL"

                linha = (
                    f"{status}"
                    f" | Serviço: {ticker}"
                    f" | Data: {data_yahoo}"
                    f" | Preço: {preco}"
                    f" | Atual: {volume_atual}"
                    f" | Mediana: {mediana}"
                    f" | Limite: {limite}\n"
                )

                f.write(linha)

            except Exception as erro:

                print(f"Erro em {ticker}: {erro}")

    print(f"[{datetime.now().strftime('%H:%M:%S')}] Log atualizado.")


if __name__ == "__main__":

    while True:

        processar_ativos()

        time.sleep(10)