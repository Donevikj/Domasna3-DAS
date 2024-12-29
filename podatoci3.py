import pandas as pd
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, EMAIndicator


def clean_data(data):
    data.loc[:, 'Price'] = data['Price'].str.replace('.', '').str.replace(',', '.').astype(float)
    data.loc[:, 'Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by='Date')
    return data


def calculate_indicators(data):
    data['SMA_10'] = SMAIndicator(data['Price'], window=10).sma_indicator()
    data['EMA_10'] = EMAIndicator(data['Price'], window=10).ema_indicator()

    # RSI
    data['RSI'] = RSIIndicator(data['Price'], window=14).rsi()
    return data


def generate_signals(data):
    data['Signal'] = 'Hold'
    data.loc[data['RSI'] < 30, 'Signal'] = 'Buy'
    data.loc[data['RSI'] > 70, 'Signal'] = 'Sell'
    return data


def plot_indicators(data, issuer_code):
    plt.figure(figsize=(14, 8))

    plt.subplot(2, 1, 1)
    plt.plot(data['Date'], data['Price'], label='Price', color='blue')
    plt.plot(data['Date'], data['SMA_10'], label='SMA 10', color='orange')
    plt.plot(data['Date'], data['EMA_10'], label='EMA 10', color='green')
    plt.title(f'{issuer_code} Price with Indicators')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(data['Date'], data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', color='red', alpha=0.7, label='Overbought (70)')
    plt.axhline(30, linestyle='--', color='green', alpha=0.7, label='Oversold (30)')
    plt.title('RSI Indicator')
    plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    issuer_codes_path = "C:/Users/38978/PycharmProjects/Domasna1DAS/issuer_codes.csv"
    historical_data_path = "C:/Users/38978/PycharmProjects/Domasna1DAS/10years_data.csv"

    try:
        issuer_codes = pd.read_csv(issuer_codes_path)
        issuer_code = 'ALK' #load an issuer code
        print(f"Using issuer code: {issuer_code}")

        historical_data = pd.read_csv(historical_data_path)
        data = historical_data[historical_data['Issuer Code'] == issuer_code]
        data = clean_data(data)

        data = calculate_indicators(data)

        data = generate_signals(data)

        output_path = f"{issuer_code}_technical_analysis.csv"
        data.to_csv(output_path, index=False)
        print(f"Technical analysis saved to {output_path}.")

        plot_indicators(data, issuer_code)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Missing column in the data - {e}")


if __name__ == "__main__":
    main()
