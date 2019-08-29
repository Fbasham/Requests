from concurrent.futures import ThreadPoolExecutor
import pandas as pd


class chunkedDF:

    def __init__(self, df, chunksize=None):
        self.df = df
        self.length = len(df)
        self.chunksize = chunksize or self.length//10
        self.chunks = (self.df[chunk:chunk+self.chunksize] for chunk in range(0, self.length, self.chunksize))
        self.threadpool = ThreadPoolExecutor()

    def row_sum(self):
        with self.threadpool as executor:
            result = executor.map(lambda x: x.sum(1), self.chunks)
            return pd.concat(result)

    def row_sub(self):
        with self.threadpool as executor:
            result = executor.map(lambda x: x.iloc[:, 0] - x.iloc[:, 1:].sum(1), self.chunks)
            return pd.concat(result)

    def col_sum(self):
        with self.threadpool as executor:
            result = executor.map(lambda x: x.sum(), self.chunks)
            return pd.concat(result,1).sum(1)

    def gb_sum(self, columns):
        def grp_sum(chunk):
            return chunk.groupby(columns).sum()        
        with self.threadpool as executor:
            result = executor.map(grp_sum, self.chunks)
            return pd.concat(result).groupby(columns).mean()
        
            





