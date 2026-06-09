import yfinance as yf
import pandas as pd

ticker = yf.Ticker("QQQ")

all_data = []

for exp in ticker.options:
    chain = ticker.option_chain(exp)
    calls = chain.calls
    puts = chain.puts

    for strike in range(650, 851, 5):

        call_row = calls[calls["strike"] == strike]
        put_row = puts[puts["strike"] == strike]

        call_mid = None
        put_mid = None

        if not call_row.empty:
            bid = call_row.iloc[0]["bid"]
            ask = call_row.iloc[0]["ask"]
            if bid > 0 and ask > 0:
                call_mid = (bid + ask) / 2

        if not put_row.empty:
            bid = put_row.iloc[0]["bid"]
            ask = put_row.iloc[0]["ask"]
            if bid > 0 and ask > 0:
                put_mid = (bid + ask) / 2

        all_data.append({
            "Expiration": exp,
            "Strike": strike,
            "Call_Mid": call_mid,
            "Put_Mid": put_mid
        })

df = pd.DataFrame(all_data)
df.to_excel("QQQ_All_Expirations_MID.xlsx", index=False)

print("Saved!")
