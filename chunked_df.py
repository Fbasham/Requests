# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 10:53:07 2019

@author: Fbasham
"""


from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from ast import literal_eval


@pd.api.extensions.register_dataframe_accessor("chunk")
class chunkedDF:

    def __init__(self, df, chunksize=None):
        self.df = df
        self.length = len(df)
        self.chunksize = chunksize if chunksize else self.length//7 if self.length > 500_000 else self.length
        self.chunks = (df[chunk:chunk+self.chunksize] for chunk in range(0, self.length, self.chunksize))
        self.threadpool = ThreadPoolExecutor()

        
    @classmethod
    def from_randint(cls, low, high, rows, cols, columns=None, chunksize=None):
        return cls(pd.DataFrame(pd.np.random.randint(low, high, (rows, cols)), columns=columns), chunksize=chunksize)
    
    
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


    def test(self, columns, aggfunc):
        def tgroup(chunk):
            return eval(f'chunk.groupby(by={columns}, as_index=False).{aggfunc}()')
        with self.threadpool as executor:
            result = executor.map(tgroup, self.chunks)
            return eval(f'pd.concat(result).groupby(by={columns}).{aggfunc}()')


    
        
