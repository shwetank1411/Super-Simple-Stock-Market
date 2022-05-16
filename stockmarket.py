import decimal
import datetime

import pandas as pd

from stocks import Stock, StockType


class StockOperations:
    TRADE_RECORDS_DF = pd.DataFrame(
        columns=['stock',
                 'quantity_of_shares',
                 'traded_price',
                 'total_traded_shares_value',
                 'buy_or_sell_ind',
                 'timestamp']
    )

    @classmethod
    def _insert_trade_records(cls, trade_record: list) -> None:
        cls.TRADE_RECORDS_DF.loc[len(cls.TRADE_RECORDS_DF.index)] = trade_record

    def __init__(self, stock: Stock):
        self.stock = stock

    def record_trade(self, quantity: int, buy_or_sell_indicator: str,
                     traded_price: decimal) -> None:

        stock_name = self.stock.stock_symbol
        stock_quantity_of_shares = quantity
        stock_traded_price = traded_price
        stock_total_traded_shares_value = quantity * traded_price
        stock_buy_or_sell_ind = buy_or_sell_indicator

        StockOperations._insert_trade_records([stock_name,
                                               stock_quantity_of_shares,
                                               stock_traded_price,
                                               stock_total_traded_shares_value,
                                               stock_buy_or_sell_ind,
                                               datetime.datetime.now()])

    def calculate_applicable_dividend(self) -> decimal:
        if self.stock.stock_type == StockType.Common:
            return self.stock.last_dividend
        elif self.stock.stock_type == StockType.Preferred:
            return self.stock.fixed_dividend * self.stock.par_value

    def calculate_dividend_yield(self, price: decimal):
        if price > 0:
            applicable_dividend = self.calculate_applicable_dividend()
            return applicable_dividend / price if applicable_dividend > 0 else 'N/A'
        return 'N/A'

    def calculate_pe_ratio(self, price: decimal):
        if price > 0:
            applicable_dividend = self.calculate_applicable_dividend()
            return price / applicable_dividend if applicable_dividend > 0 else 'N/A'
        return 'N/A'

    def calculate_volume_weighted_stock_price(self) -> decimal:
        stock_condition = self.TRADE_RECORDS_DF.stock == self.stock.stock_symbol
        last_15_min_records_cond = datetime.datetime.now() - self.TRADE_RECORDS_DF.timestamp <= pd.to_timedelta('15m')
        agg_dict = {'total_traded_shares_value': 'sum', 'quantity_of_shares': 'sum'}
        agg_df = self.TRADE_RECORDS_DF.loc[stock_condition & last_15_min_records_cond].groupby('stock').agg(agg_dict)
        result_arr = agg_df[['total_traded_shares_value', 'quantity_of_shares']].values[0]
        volume_weighted_stock_price = result_arr[0] / result_arr[1]
        return volume_weighted_stock_price
