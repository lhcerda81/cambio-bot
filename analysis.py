import pandas as pd
from prophet import Prophet

def prever(df):
    if len(df) < 20:
        return None

    df = df.copy()
    df = df.rename(columns={"data": "ds", "valor": "y"})
    df["ds"] = pd.to_datetime(df["ds"])

    model = Prophet(daily_seasonality=True)
    model.fit(df)

    future = model.make_future_dataframe(periods=2)
    forecast = model.predict(future)

    previsoes = forecast.tail(2)["yhat"].values

    return previsoes.tolist()
