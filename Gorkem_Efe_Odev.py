import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


## Bu datalardan belirlediğimiz eşikten küçük ve önemsiz miktarda olanları filtreler.
def filter_data(df, column, threshold=0.001):
    df = df[df[column].astype(float) >= threshold]
    return df

## Datamızın içinden istatiksel analimiz sonrası aldığımız verileri bir DICT'e yazdırır.
def analyze_df(df, price_column, volume_column):
    global analysis
    analysis = {
        "min_price": df[price_column].astype(float).min(),
        "max_price": df[price_column].astype(float).max(),
        "avg_price": df[price_column].astype(float).mean(),
        "total_volume": df[volume_column].astype(float).sum()
    }
    return analysis


## Verdiğimiz Parametreye göre Order Book verilerini json formatında internetten çeker.
def fetch_data(Parameter):
    url = f"https://www.bitexen.com/api/v1/order_book/{Parameter}/"
    response = requests.get(url)
    return response.json()

## Yukarda tanımladığımız filter_data ve analyze_df fonksiyonlarını kullanarak Order Book analiz eder ve bunları bir DICT'e kaydeder
def analyze_order_book(data):
    global df_buyers

    df_buyers = pd.DataFrame(data['data']['buyers'])
    df_sellers = pd.DataFrame(data['data']['sellers'])
    df_transactions = pd.DataFrame(data['data']['last_transactions'])

    df_buyers = filter_data(df_buyers, 'orders_total_amount')
    df_sellers = filter_data(df_sellers, 'orders_total_amount')
    df_transactions = filter_data(df_transactions, 'amount')

    Buyers = analyze_df(df_buyers, 'orders_price', 'orders_total_amount')
    Sellers = analyze_df(df_sellers, 'orders_price', 'orders_total_amount')
    Transactions = analyze_df(df_transactions, 'price', 'amount')

    return {
        "buyers": Buyers,
        "sellers": Sellers,
        "transactions": Transactions
    }

## Elde ettiğimiz analiz sonuçlarını bir excel dosyasına çıktı olarak kaydeder.
def save_to_excel(btctry_analysis, btcusdt_analysis, filename="Excel_Gorkem_Efe_Odev.xlsx"):
    with pd.ExcelWriter(filename) as writer:
        btctry_df = pd.DataFrame(btctry_analysis)
        btcusdt_df = pd.DataFrame(btcusdt_analysis)

        btctry_df.to_excel(writer, sheet_name="TRY - BTCTRY")
        btcusdt_df.to_excel(writer, sheet_name="USDT - BTCUSDT")

## Programın ana fonksiyonudur.
def main():
    logging.info("Fetching BTCTRY data")
    btctry_data = fetch_data("BTCTRY")

    logging.info("Fetching BTCUSDT data")
    btcusdt_data = fetch_data("BTCUSDT")

    if btctry_data and btcusdt_data:
        logging.info("Analyzing BTCTRY data")
        btctry_analysis = analyze_order_book(btctry_data)

        logging.info("Analyzing BTCUSDT data")
        btcusdt_analysis = analyze_order_book(btcusdt_data)

        logging.info("Saving analysis to Excel")
        save_to_excel(btctry_analysis, btcusdt_analysis)

        logging.info("Analysis saved successfully.")

## Programı çalıştırır.
if __name__ == "__main__":
    main()