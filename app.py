import decimal

from scipy.stats import gmean
import numpy as np

from stocks import Stock, StockType
from stockmarket import StockOperations


def create_sample_gbce_stock_instances() -> tuple[Stock, Stock, Stock, Stock, Stock]:
    """Creates Sample data from the Global Beverage Corporation Exchange"""

    stock_1 = Stock(stock_symbol='TEA', stock_type=StockType.Common,
                    last_dividend=0, fixed_dividend=None, par_value=100)
    stock_2 = Stock(stock_symbol='POP', stock_type=StockType.Common,
                    last_dividend=8, fixed_dividend=None, par_value=100)
    stock_3 = Stock(stock_symbol='ALE', stock_type=StockType.Common,
                    last_dividend=23, fixed_dividend=None, par_value=60)
    stock_4 = Stock(stock_symbol='GIN', stock_type=StockType.Preferred,
                    last_dividend=8, fixed_dividend=0.02, par_value=100)
    stock_5 = Stock(stock_symbol='JOE', stock_type=StockType.Common,
                    last_dividend=13, fixed_dividend=None, par_value=250)
    return stock_1, stock_2, stock_3, stock_4, stock_5


def create_sample_gbce_stocks_trade_bulk_records(stock_instance: Stock) -> StockOperations:
    stock_operations = StockOperations(stock_instance)
    for _ in range(4, 8):
        stock_operations.record_trade(quantity=np.random.randint(10, 25),
                                      buy_or_sell_indicator='B',
                                      traded_price=np.random.randint(250, 350))

    for _ in range(4):
        stock_operations.record_trade(quantity=np.random.randint(5, 10),
                                      buy_or_sell_indicator='S',
                                      traded_price=np.random.randint(250, 350))
    return stock_operations


def print_volume_weighted_stock_prices(stock_operations_instances: tuple) -> None:

    tea_ops, pop_ops, ale_ops, gin_ops, joe_ops = stock_operations_instances
    tea_vwsp: decimal = tea_ops.calculate_volume_weighted_stock_price()
    pop_vwsp: decimal = pop_ops.calculate_volume_weighted_stock_price()
    ale_vwsp: decimal = ale_ops.calculate_volume_weighted_stock_price()
    gin_vwsp: decimal = gin_ops.calculate_volume_weighted_stock_price()
    joe_vwsp: decimal = joe_ops.calculate_volume_weighted_stock_price()

    print(f'Volume Weighted Stock Price for tea stock = {tea_vwsp}')
    print(f'Volume Weighted Stock Price for pop stock = {pop_vwsp}')
    print(f'Volume Weighted Stock Price for ale stock = {ale_vwsp}')
    print(f'Volume Weighted Stock Price for gin stock = {gin_vwsp}')
    print(f'Volume Weighted Stock Price for joe stock = {joe_vwsp}')
    print('\n')


def print_gbce_all_share_index() -> None:
    all_share_price_arr = StockOperations.TRADE_RECORDS_DF.traded_price.values
    gbce_all_share_index = gmean(all_share_price_arr)
    print(f'The GBCE All Share Index is {gbce_all_share_index}')


def show_trade_records() -> None:
    print('\n')
    print('============================================================================')
    print('Showing Trade Records ...')
    print('============================================================================')
    print(StockOperations.TRADE_RECORDS_DF)
    print('\n')


def clean_trade_records() -> None:
    print('\n')
    print('Cleaning up Trade records ...')
    del StockOperations.TRADE_RECORDS_DF


def main() -> None:

    # Setting up a stock
    pop_stock = Stock(stock_symbol='POP', stock_type=StockType.Common,
                      last_dividend=8, fixed_dividend=None, par_value=100)
    pop_stock_ops = StockOperations(pop_stock)

    # Setting up Input price for example
    input_price: int = 100

    # For given input price , calculating Dividend Yield for a stock
    pop_stock_dividend_yield = pop_stock_ops.calculate_dividend_yield(input_price)
    print(f'The dividend yield for POP stock is {pop_stock_dividend_yield} ')

    # For given input price , calculating PE Ratio for a stock
    pop_stock_pe_ratio = pop_stock_ops.calculate_pe_ratio(input_price)
    print(f'The PE Ratio for POP stock is {pop_stock_pe_ratio} ')

    # Recording a Trade for a stock in memory
    pop_stock_ops.record_trade(quantity=4,
                               buy_or_sell_indicator='B',
                               traded_price=250)

    # Showing the recorded trade
    show_trade_records()

    # Set up stock instances and load up sample trading records in memory
    print('Loading up sample trading data in memory ...')
    stock_operations_instances = tuple(map(create_sample_gbce_stocks_trade_bulk_records,
                                           create_sample_gbce_stock_instances()))

    # Showing the loaded sample trading records
    show_trade_records()

    # Calculating Volume Weighted Stock Price based on trades in past 15 minutes for a stock
    print_volume_weighted_stock_prices(stock_operations_instances)

    # printing out the GBCE All Share Index based on available in-memory data
    print_gbce_all_share_index()

    # Final Clean up of in-memory data
    clean_trade_records()


if __name__ == "__main__":
    main()
