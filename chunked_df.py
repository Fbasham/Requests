# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:53:07 2019

@author: Fbasham
"""


from concurrent.futures import ThreadPoolExecutor
import pandas as pd


class chunkedDF:

    def __init__(self, df, chunksize=None):
        self.df = df
        self.length = len(df)
        self.chunksize = chunksize or self.length//7 if self.length > 500_000 else self.length
        self.num_chunks = pd.np.ceil(self.length/self.chunksize).astype(int)
        self.chunks = (self.df[chunk:chunk+self.chunksize] for chunk in range(0, self.length, self.chunksize))
        self.threadpool = ThreadPoolExecutor()
        self.columns = df.columns

    @classmethod
    def from_np_rand(cls, rows, cols, columns=None):
        return cls(pd.DataFrame(pd.np.random.rand(rows, cols), columns=columns))    
    
    def row_sum(self):
        with self.threadpool as executor:
            result = executor.map(lambda x: x.sum(1), self.chunks)
            return pd.concat(result)

    def col_sub(self):
        with self.threadpool as executor:
            result = executor.map(lambda x: x.iloc[:, 0] - x.iloc[:, 1:].sum(1), self.chunks)
            return pd.concat(result)

    def col_sum(self, columns=None):
        columns = columns or self.columns
        with self.threadpool as executor:
            result = executor.map(lambda x: x[columns].sum(), self.chunks)
            return pd.concat(result,1).sum(1)

    def gb_sum(self, columns):
        def grp_sum(chunk):
            return chunk.groupby(by=columns, as_index=False).sum()      
        with self.threadpool as executor:
            result = executor.map(grp_sum, self.chunks)
            return pd.concat(result).groupby(by=columns).sum()
        
    
    def gb_mean(self, columns):
        def grp_mean(chunk):
            return chunk.groupby(by=columns, as_index=False).mean()      
        with self.threadpool as executor:
            result = executor.map(grp_mean, self.chunks)
            return pd.concat(result).groupby(by=columns).mean()
        
        