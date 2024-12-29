import pandas as pd
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.volatility import BollingerBands
from ta.trend import CCIIndicator
from ta.volume import VolumeWeightedAveragePrice

def clean_data(data):
    data.loc[:, 'Price'] = data['Price'].str.replace('.', '').str.replace(',', '.').astype(float)
    data.loc[:, 'Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by='Date')
    return data

def calculate_indicators(data):
    # Moving Averages
    data['SMA_10'] = SMAIndicator(data['Price'], window=10).sma_indicator()
    data['EMA_10'] = EMAIndicator(data['Price'], window=10).ema_indicator()
    data['MACD'] = MACD(data['Price']).macd()

    # Adding Hull Moving Average (HMA)
    data['HMA_20'] = data['Price'].rolling(window=20).apply(lambda x: (2 * x[:int(len(x)/2)].mean() - x[int(len(x)/2):].mean()))

    # Adding Weighted Moving Average (WMA)
    data['WMA_10'] = data['Price'].rolling(window=10).apply(lambda x: sum((i+1) * val for i, val in enumerate(x)) / sum(range(1, 11)))

    # Oscillators
    data['RSI'] = RSIIndicator(data['Price'], window=14).rsi()
    data['Stochastic'] = StochasticOscillator(data['Price'], data['Price'], data['Price'], window=14).stoch()
    data['CCI'] = CCIIndicator(data['Price'], data['Price'], data['Price'], window=20).cci()

    # Adding Williams %R
    data['Williams_%R'] = StochasticOscillator(data['Price'], data['Price'], data['Price'], window=14).stoch_signal() - 100

    return data

def generate_signals(data):
    data['Signal'] = 'Hold'
    data.loc[data['RSI'] < 30, 'Signal'] = 'Buy'
    data.loc[data['RSI'] > 70, 'Signal'] = 'Sell'
    data.loc[(data['Price'] < data['SMA_10']) & (data['RSI'] < 30), 'Signal'] = 'Strong Buy'
    data.loc[(data['Price'] > data['EMA_10']) & (data['RSI'] > 70), 'Signal'] = 'Strong Sell'
    return data

def plot_indicators(data, issuer_code):
    plt.figure(figsize=(16, 14))

    # Price with SMA, EMA, MACD
    plt.subplot(4, 1, 1)
    plt.plot(data['Date'], data['Price'], label='Price', color='blue')
    plt.plot(data['Date'], data['SMA_10'], label='SMA 10', color='orange')
    plt.plot(data['Date'], data['EMA_10'], label='EMA 10', color='green')
    plt.plot(data['Date'], data['HMA_20'], label='HMA 20', color='red', linestyle='--')
    plt.plot(data['Date'], data['WMA_10'], label='WMA 10', color='purple', linestyle='--')
    plt.title(f'{issuer_code} Price with Moving Averages')
    plt.legend()

    # RSI and Stochastic Oscillator
    plt.subplot(4, 1, 2)
    plt.plot(data['Date'], data['RSI'], label='RSI', color='purple')
    plt.axhline(70, linestyle='--', color='red', alpha=0.7, label='Overbought (70)')
    plt.axhline(30, linestyle='--', color='green', alpha=0.7, label='Oversold (30)')
    plt.plot(data['Date'], data['Stochastic'], label='Stochastic Oscillator', color='brown', linestyle='--')
    plt.title('Momentum Indicators')
    plt.legend()

    # MACD
    plt.subplot(4, 1, 3)
    plt.plot(data['Date'], data['MACD'], label='MACD', color='cyan')
    plt.title('MACD Indicator')
    plt.legend()

    # CCI and Williams %R
    plt.subplot(4, 1, 4)
    plt.plot(data['Date'], data['CCI'], label='CCI', color='magenta')
    plt.plot(data['Date'], data['Williams_%R'], label="Williams %R", color='darkgreen', linestyle='--')
    plt.title('Cyclical Indicators')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():
    try:
        # Replace these paths with your local file paths
        issuer_codes_path = 'C:/Users/38978/PycharmProjects/Domasna1DAS/issuer_codes.csv'
        historical_data_path = 'C:/Users/38978/PycharmProjects/Domasna1DAS/10years_data.csv'

        issuer_codes = pd.read_csv(issuer_codes_path)
        issuer_code = 'ALK'  # Load an issuer code
        print(f"Using issuer code: {issuer_code}")

        historical_data = pd.read_csv(historical_data_path)
        data = historical_data[historical_data['Issuer Code'] == issuer_code]
        data = clean_data(data)

        data = calculate_indicators(data)
        data = generate_signals(data)

        output_path = f"C:/Users/38978/PycharmProjects/Domasna1DAS/{issuer_code}_technical_analysis.csv"
        data.to_csv(output_path, index=False)
        print(f"Technical analysis saved to {output_path}.")

        plot_indicators(data, issuer_code)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except KeyError as e:
        print(f"Error: Missing column in the data - {e}")

if __name__ == "__main__":
    main()
