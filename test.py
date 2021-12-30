from firebase_admin.firestore import client
import pandas as pd

from pandas import DataFrame

from src.environment.simulation import SimulationEnvironment
from src.strategy.grid_trading import GridTrading

from time import sleep


def bitstamp_loader(datapath: str) -> DataFrame:
    dataframe = pd.read_csv(datapath, skiprows=1)
    dataframe = dataframe.rename(
        columns={"unix": "timestamp", "symbol": "security"})
    dataframe = dataframe.drop(columns=["date", "Volume ETH", "Volume USD"])
    dataframe = dataframe.set_index("timestamp")
    dataframe = dataframe.sort_index()

    return dataframe


if __name__ == '__main__':
    df = bitstamp_loader("data/Bitstamp_ETHUSD_1h.csv")
    env = SimulationEnvironment("SOL", df, 1000, 50, 0.005)

    # print(env.get_positions())

    # import cbpro

    # auth_client = cbpro.AuthenticatedClient('2ff05c91df31d1c63ca61ae0e875c6e7',
    #                                         'XXa2zKyj+AgW8hRYYBOdFzs9wZaH+Pu+tARbGOo4fHLcJiTwdCz6jvF4EOXJGn2B1phVOBjxQY0TT36RQ0+KOg==',
    #                                         'gb7cw21mo9h')

    # fills_gen = auth_client.get_fills('SOL-USDT')
    # # Get all fills (will possibly make multiple HTTP requests)
    # all_fills = list(fills_gen)
    # print(all_fills)
