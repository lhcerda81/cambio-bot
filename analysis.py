def prever(df):
    if len(df) < 2:
        return None

    ultimo = df["valor"].iloc[-1]
    return [ultimo, ultimo]
