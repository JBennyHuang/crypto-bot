import pandas as pd

from pandas import DataFrame

from src.environment.simulation import SimulationEnvironment
from src.strategy.grid_trading import GridTrading


def bitstamp_loader(datapath: str) -> DataFrame:
    dataframe = pd.read_csv(datapath, skiprows=1)
    dataframe = dataframe.rename(
        columns={"unix": "timestamp", "symbol": "security"})
    dataframe = dataframe.drop(columns=["date", "Volume ETH", "Volume USD"])
    dataframe = dataframe.set_index("timestamp")
    dataframe = dataframe.sort_index()

    return dataframe


if __name__ == '__main__':
    df = bitstamp_loader("data/Bitstamp_ETHUSD_d.csv")
    env = SimulationEnvironment("SOL", df, 1000, 50, 0.005)
    strategy = GridTrading(env, [1000, 2000, 3000, 4000, 5000])

    env.bind('update', strategy.update)

    env.start()
    env.plot()
