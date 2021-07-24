'''This file reads sec_bhavdata_full.csv and previous days data with analysis_of_delivery.csv and gives us stock list with high delivery'''

import pandas as pd
import numpy as np
import os


def highlight(s):
    if s > 500:
        return ['background-color: yellow']
    else:
        return ['background-color: red']


def highlight_greaterthan_1(s):
    # if s.BEST_STK is True:
    if s.MEAN_DELIV > 500:
        return ['background-color: yellow']
    else:
        return ['background-color: white']


def create_dir():
    directory = str(pd.to_datetime('today').date())
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)


def read_files():
    crnt_data = pd.read_csv(r'sec_bhavdata_full.csv', index_col='SYMBOL')
    crnt_data.drop([' DATE1', ' LAST_PRICE', ' AVG_PRICE', ' TTL_TRD_QNTY',
                    ' DELIV_PER'], axis=1, inplace=True)

    # removing columns where SERIES is not equal to "EQ"
    crnt_data = crnt_data[crnt_data[' SERIES'] == " EQ"]
    newDataFrame = crnt_data

    prev_data = pd.read_csv(r'analysis_of_delivery.csv', index_col='SYMBOL')

    listCurrSymbol = crnt_data.index.values.tolist()
    listPrevSymbol = prev_data.index.values.tolist()

    newDataFrame['DELIV_QTY7'] = prev_data['DELIV_QTY6']
    newDataFrame['DELIV_QTY6'] = prev_data['DELIV_QTY5']
    newDataFrame['DELIV_QTY5'] = prev_data['DELIV_QTY4']
    newDataFrame['DELIV_QTY4'] = prev_data['DELIV_QTY3']
    newDataFrame['DELIV_QTY3'] = prev_data['DELIV_QTY2']
    newDataFrame['DELIV_QTY2'] = prev_data[' DELIV_QTY']
    newDataFrame[' DELIV_QTY'] = crnt_data[' DELIV_QTY']

    listNewComing = list(set(listCurrSymbol) - set(listPrevSymbol))
    listOutGoing = list(set(listPrevSymbol) - set(listCurrSymbol))
    # There may be some stocks which were present in one list but not present in
    # others, we need to fill appropriate value for them
    for stk in listNewComing:
        newDataFrame.at[stk, 'DELIV_QTY2'] = crnt_data.at[stk, ' DELIV_QTY']
        newDataFrame.at[stk, 'DELIV_QTY3'] = crnt_data.at[stk, ' DELIV_QTY']
        newDataFrame.at[stk, 'DELIV_QTY4'] = crnt_data.at[stk, ' DELIV_QTY']
        newDataFrame.at[stk, 'DELIV_QTY5'] = crnt_data.at[stk, ' DELIV_QTY']
        newDataFrame.at[stk, 'DELIV_QTY6'] = crnt_data.at[stk, ' DELIV_QTY']
        newDataFrame.at[stk, 'DELIV_QTY7'] = crnt_data.at[stk, ' DELIV_QTY']

    newDataFrame['MEAN_DELIV'] = newDataFrame[['DELIV_QTY2', 'DELIV_QTY3',
                                               'DELIV_QTY4', 'DELIV_QTY5', 'DELIV_QTY6', 'DELIV_QTY7']].mean(axis="columns")

    # n_list = list(filter(lambda x: x > 100, newDataFrame[' TURNOVER_LACS']))
    newDataFrame['GOOD_TURNOVER'] = (newDataFrame[' TURNOVER_LACS'] > 300)
    newDataFrame['SPREAD'] = (
        (newDataFrame[' HIGH_PRICE'] - newDataFrame[' LOW_PRICE']) / newDataFrame[' LOW_PRICE']) * 100
    newDataFrame['CHANGE'] = (
        (newDataFrame[' CLOSE_PRICE'] - newDataFrame[' PREV_CLOSE']) / newDataFrame[' PREV_CLOSE']) * 100
    newDataFrame['CHN_GT_3'] = abs(newDataFrame['CHANGE']) > 3
    newDataFrame['NOT_PENNY'] = newDataFrame[' CLOSE_PRICE'] > 5
    # print(newDataFrame.head())
    # print(newDataFrame['MEAN_DELIV'].unique)

    newDataFrame[' DELIV_QTY'] = newDataFrame[' DELIV_QTY'].astype('int64')
    newDataFrame['MEAN_DELIV'] = newDataFrame['MEAN_DELIV'].astype('int64')

    newDataFrame['CHNG_DELIV'] = (
        (newDataFrame[' DELIV_QTY'] - newDataFrame['MEAN_DELIV']) / newDataFrame['MEAN_DELIV']) * 100

    newDataFrame['TMP_CHNG_DELIV'] = newDataFrame['CHNG_DELIV'] > 50
    newDataFrame['PRC_VOL'] = newDataFrame[[
        'GOOD_TURNOVER', 'CHN_GT_3', 'NOT_PENNY']].all(axis="columns")
    newDataFrame['BEST_STK'] = newDataFrame[['PRC_VOL', 'TMP_CHNG_DELIV']].all(axis="columns")
    newDataFrame['AVG_TRADE_SIZE'] = newDataFrame[' TURNOVER_LACS'] / newDataFrame[' NO_OF_TRADES']
    newDataFrame.drop([' HIGH_PRICE', ' LOW_PRICE', ' OPEN_PRICE',
                       ' PREV_CLOSE', ' SERIES', 'GOOD_TURNOVER', 'CHN_GT_3',
                       'TMP_CHNG_DELIV', 'NOT_PENNY', ' NO_OF_TRADES'], axis=1, inplace=True)

    newDataFrame = newDataFrame[[' CLOSE_PRICE',
                                 'BEST_STK', 'PRC_VOL', 'CHNG_DELIV', 'CHANGE',
                                 'SPREAD', ' DELIV_QTY', 'MEAN_DELIV',
                                 'DELIV_QTY2', 'DELIV_QTY3', 'DELIV_QTY4',
                                 'DELIV_QTY5', 'DELIV_QTY6', 'DELIV_QTY7',
                                 ' TURNOVER_LACS', 'AVG_TRADE_SIZE']]
    # print(pd.to_datetime('today').date())
    # newDataFrame.to_html('tmp11.html')
    # newDataFrame.style.apply(highlight_greaterthan_1, axis=1).render()It had a gate level issue. If you have sent the same to customer then you should send v19.0.3-55 TBX patch generated yesterday.

    # with pd.ExcelWriter('test.xlsx') as writer:
    #     newDataFrame.to_excel(writer, sheet_name="Sheet1")

    # styled = newDataFrame.style.apply(highlight_greaterthan_1, axis=1)
    # styled.render()
    # styled = newDataFrame.style.applymap(highlight)
    # styled.to_excel('styled.xlsx', engine='openpyxl')
    directory_name = str(pd.to_datetime('today').date())
    file_xlsx = str(directory_name + '/' + directory_name + '_bhav_copy' + '.xlsx')

    buy_stock = newDataFrame
    buy_stock = buy_stock[buy_stock['CHANGE'] > 1]
    buy_stock = buy_stock[buy_stock['BEST_STK']]  # handling of boolean

    sell_stock = newDataFrame
    sell_stock = sell_stock[sell_stock['CHANGE'] < 1]
    sell_stock = sell_stock[sell_stock['BEST_STK']]

    with pd.ExcelWriter(file_xlsx) as writer:
        newDataFrame.to_excel(writer, sheet_name="Sheet1")
        buy_stock.to_excel(writer, sheet_name="Sheet2")
        sell_stock.to_excel(writer, sheet_name="Sheet3")

    writer.save()
    newDataFrame.to_csv('analysis_of_delivery.csv')


def main():
    create_dir()
    read_files()
    print("Main called")


if __name__ == "__main__":
    main()
