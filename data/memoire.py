import pandas as pd
import csv

path_tsv = 'year_origin_destination_hs07_6.tsv'
path_bec = 'HS2007-BEC4_Correlation_and_conversionTable.xls'
period = list(map(str,range(2007,2019)))
accepted_hs = list()
treatment = {'intermediate goods': ['53'],
'consumer goods': ['51','521','522'],
'capital goods': ['4','41','42']
}
df = pd.read_excel(path_bec, sheet_name='BEC4-HS2007', dtype = {'BEC4': str, 'HS2007': str} )
bool_s = df['HS2007'].astype(str).str.startswith('87')
df = df[bool_s]
df['HS2007'] = df['HS2007'].astype(str).str.replace('.', '')
intermediate_goods = df[df['BEC4'].isin(['53'])].set_index('HS2007')
finish_goods = df[df['BEC4'].isin(['51','521','522','4','41','42'])].set_index('HS2007')
total_goods = df[df['BEC4'].isin(['53','51','521','522','4','41','42'])].set_index('HS2007')
def clean_data(path_tsv,intermediate_goods,finish_goods,total_goods,period):
    with open(path_tsv) as tsvfile:
        trade_total_goods = pd.DataFrame(columns=['year', 'origin', 'dest', 'hs07', 'export_val', 'import_val','goods_type'])
        reader = csv.reader(tsvfile, delimiter='\t')
        i = 0
        for row in reader:     
            if row[0] in period:
                if row[3] in total_goods.index:
                    row[4] = row[4] if row[4] != 'NULL' else 0
                    row[5] = row[5] if row[5] != 'NULL' else 0
                    if row[3] in intermediate_goods.index:
                        row.append('intermediate')
                    elif row[3] in finish_goods.index:
                        row.append('finish')
                    else:
                        row.append('unknow')
                    trade_total_goods.loc[i] = row
                    i+=1
        return trade_total_goods
    
trade_total_goods = clean_data(path_tsv,intermediate_goods,finish_goods,total_goods,period)
trade_total_goods.to_csv('automotive_2008-2017_trade.csv', sep='|',index=False)

