import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import operator
import json
import os
from backend.data_process import get_cur_path, get_previous_quarter
from flask import session


def get_data(report):
    path = get_cur_path()
    csv_path = os.path.join(path, "data", report + ".csv")
    df = pd.read_csv(csv_path, dtype=str)
    df.columns = ['Company', 'Quarter', 'Item_ID', 'Item']
    df = df.set_index(['Company', 'Quarter'])
    df.sort_index(inplace=True)
    return df



# previous day's Value-at-risk (VaR)-based measure
# IR, Debt, Equity, FX, Commodities
# return JSON: {id: [{item_name_1: item_value_1}, {item_name_2: item_value_2}]}
def test_asset_VaR_query(quarter_date):
    raw_data = get_data('FFIEC102')
    asset_VaR_item_names = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']
    data = raw_data.query('Item_ID in @asset_VaR_item_names and Quarter == @quarter_date')
    # print(data)
    asset_VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    for k, v in asset_VaR_data.items():
        asset_VaR_data[k] = list(map(lambda x: {x[0]: x[1]}, v))
    res = json.dumps(asset_VaR_data)
    # data.reset_index(inplace=True)
    # data.set_index(['Company', 'Quarter', 'Item_ID'], inplace=True)
    # result = data.to_json(orient="index", indent=4)
    # print(result)


# Previous day's VaR-based measure and Most recent stressed VaR-based measure
# return JSON: {id: [[item_name_1, item_value_1], [item_name_2, item_value_2]]}
def test_VaR_sVarR_query(quarter_date):
    raw_data = get_data('FFIEC102')
    VaR_item_names = ['MRRRS298', 'MRRRS302']
    data = raw_data.query('Item_ID in @VaR_item_names and Quarter == @quarter_date')
    VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    return VaR_data

# Bar chart quarterly comparison:
# 1. VaR and sVaR Comparison
# 2. Trading Asset Comparison
# 3. Trading Asset to Risk Ratio
# 4. Trading Revenue to VaR Ratio

def item_name_mapping(x, mapping):
    data_map = {}
    data_list = x.values.tolist()
    for item in data_list:
        data_map[mapping[item[0]]] = item[1]
    return data_map

## Quarterly Highlights Key
def get_total_capital_stack(quarter, comp_dict):
    asset_dict = {'AAAB8274': 'Tier 1 Capital',
                  'AAAB5311': 'Tier 2 Capital'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAB8274', 'AAAB5311']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res

def get_total_RWA_bar(quarter, comp_dict):
    asset_dict = {'AAABA223': 'Total Risk-weighted Assets'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAABA223']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res

def key_ratio_comparison_bar(quarter, comp_dict):
    asset_dict = {'AAABP793': 'Common equity tier 1 capital ratio',
                  'AAAB7206': 'Tier 1 capital ratio',
                  'AAAB7205': 'Total capital ratio'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAABP793', 'AAAB7206', 'AAAB7205']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res

def get_buffer_stack(quarter, comp_dict):
    # AAABP902 AAABP903 AAABP904 AAABP905 AAABP906

    asset_dict = {'AAABFB52': 'conservation buffer',
                  'AAABFB53': 'countercyclical buffer',
                  'AAABFB54': 'GSIB buffer'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAABFB52', 'AAABFB53', 'AAABFB54']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data = data.reset_index()

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res

def get_total_exposure_decomposition(quarter_date, comp_dict):
    # 'AAAAD956', 'AAAAY826', 'AAAAY829', 'AAAAY831'

    asset_dict = {'AAAAD956': 'on-balance sheet exposure',
                  'AAAAY826': 'total derivative exposure',
                  'AAAAY829': 'total repo exposure',
                  'AAAAY831': 'off-balance sheet exposure'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAD956', 'AAAAY826', 'AAAAY829', 'AAAAY831']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')

    data = data.reset_index()
    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})

    exposure_comparison = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], exposure_comparison[key]) for key in exposure_comparison)
    return res

## Quarterly Highlights Detail
def get_tier1deductions_adjustment_stack(quarter, comp_dict):
    # 'AAABP841', 'AAABP842', 'AAABP843', 'AAABP849', 'AAABQ258', 'AAABP887', 'AAABP888'

    asset_dict = {'AAABP841': 'Goodwill net',
                  'AAABP842': 'Other intangible assets',
                  'AAABP843': 'Deferred tax assets',
                  'AAABP849': 'Accumulated net G/L',
                  'AAABQ258': 'Unrealized G/L',
                  'AAABP887': 'Defined-benefit pension fund assets',
                  'AAABP888': 'Investments in own shares'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAABP841', 'AAABP842', 'AAABP843', 'AAABP849', 'AAABQ258', 'AAABP887', 'AAABP888']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res


def get_tier1composition_stack(quarter, comp_dict):
    # 'AAABP840', 'AAABP858', 'AAABP864', 'AAABP865'

    asset_dict = {'AAABP840': 'Common equity tier 1 capital',
                  'AAABP858': 'Total tier 1 capital adjustments and deductions',
                  'AAABP864': 'Total additional tier 1 capital deductions',
                  'AAABP865': 'Additional tier 1 capital'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAABP840', 'AAABP858', 'AAABP864', 'AAABP865']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data = data.reset_index()
    data.loc[data[data['Item_ID'] == 'AAABP858'].index, 'Item'] = -data.loc[
        data[data['Item_ID'] == 'AAABP858'].index, 'Item'].astype(int)
    data.loc[data[data['Item_ID'] == 'AAABP864'].index, 'Item'] = -data.loc[
        data[data['Item_ID'] == 'AAABP864'].index, 'Item'].astype(int)

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res


def get_tier2deduction_adjustment_stack(quarter, comp_dict):
    # AAABP902 AAABP903 AAABP904 AAABP905 AAABP906

    asset_dict = {'AAABP902': 'Investments',
                  'AAABP903': 'Reciprocal cross-holdings',
                  'AAABP904': 'Non-significant investments',
                  'AAABP905': 'Significant investments in financial institutions',
                  'AAABP906': 'Other deductions'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAABP902', 'AAABP903', 'AAABP904', 'AAABP905', 'AAABP906']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data = data.reset_index()

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res

def get_tier2_before_deduction_stack(quarter, comp_dict):
    #'AAABP866', 'AAABP867', 'AAABP868', 'AAAB5310', 'AAABP870'

    asset_dict = {'AAABP866': 'Tier2 capital instrument plus related surplus',
                  'AAABP867': 'Non-qualifying capital instruments',
                  'AAABP868': 'Total capital minority interest',
                  'AAAB5310': 'Eligible credit reserves'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAABP866', 'AAABP867', 'AAABP868', 'AAAB5310']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data = data.reset_index()

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res

def get_exposure_adjustment_stack(quarter, comp_dict):
    #'AAAAFS87', 'AAAAFS88', 'AAAAFS89', 'AAAAFS90', 'AAAAFS91', 'AAAAFS92', 'AAAALB41'

    asset_dict = {'AAAAFS87': 'investments',
                  'AAAAFS88': 'derivative transacts',
                  'AAAAFS89': 'repo-style transacts',
                  'AAAAFS90': 'off-bal sheet exposures',
                  'AAAAFS91': 'deduct from tier 1 capital',
                  'AAAAFS92': 'freq calculations',
                  'AAAALB41': 'deductions'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAFS87', 'AAAAFS88', 'AAAAFS89', 'AAAAFS90', 'AAAAFS91', 'AAAAFS92', 'AAAALB41']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data.loc[data[data['Item_ID'] == 'AAAAFS91'].index,'Item'] = -data.loc[data[data['Item_ID'] == 'AAAAFS91'].index,'Item'].astype(int)
    data.loc[data[data['Item_ID'] == 'AAAAFS92'].index,'Item'] = -data.loc[data[data['Item_ID'] == 'AAAAFS92'].index,'Item'].astype(int)
    data.loc[data[data['Item_ID'] == 'AAAALB41'].index,'Item'] = -data.loc[data[data['Item_ID'] == 'AAAALB41'].index,'Item'].astype(int)

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)

    return res

def get_on_balance_sheet_exposure_decomposition(quarter_date, comp_dict):
    # 'AAAAD956', 'AAAAY826', 'AAAAY829', 'AAAAY831'

    asset_dict = {'AAAAY830': 'The balance sheet carrying value',
                  'AAAAM349': 'Deductions from CET1 and additional T1 capital',
                  'AAAALB41': 'Deductions of qualifying central bank deposits'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAY830', 'AAAAM349', 'AAAALB41']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')

    data = data.reset_index()

    data.loc[data[data['Item_ID'] == 'AAAAM349'].index,'Item'] = -data.loc[data[data['Item_ID'] == 'AAAAM349'].index,'Item'].astype(int)
    data.loc[data[data['Item_ID'] == 'AAAALB41'].index,'Item'] = -data.loc[data[data['Item_ID'] == 'AAAALB41'].index,'Item'].astype(int)

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})

    exposure_comparison = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], exposure_comparison[key]) for key in exposure_comparison)
    return res


def get_derivative_exposure_decomposition(quarter_date, comp_dict):
    # 'AAAAD956', 'AAAAY826', 'AAAAY829', 'AAAAY831'

    asset_dict = {'AAAAM337': 'Replacement cost for all derivative transactions',
                  'AAAAM339': 'Add-on amounts for potential future exposure',
                  'AAAAY822': 'Gross-up for collateral',
                  'AAAAM340': 'Adjusted effective notional principal amount of sold credit protection',
                  'AAAAY823': 'Deduction of receivable assets',
                  'AAAAY824': 'Exempted exposures to CCPs',
                  'AAAAY825': 'Offsets and PFE deductions'
                  }

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAM337', 'AAAAM339', 'AAAAY822', 'AAAAM340', 'AAAAY823', 'AAAAY824', 'AAAAY825']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')

    data = data.reset_index()

    data.loc[data[data['Item_ID'] == 'AAAAY823'].index, 'Item'] = -data.loc[data[data['Item_ID'] == 'AAAAY823'].index, 'Item'].astype(int)
    data.loc[data[data['Item_ID'] == 'AAAAY824'].index, 'Item'] = -data.loc[data[data['Item_ID'] == 'AAAAY824'].index, 'Item'].astype(int)
    data.loc[data[data['Item_ID'] == 'AAAAY825'].index, 'Item'] = -data.loc[data[data['Item_ID'] == 'AAAAY825'].index, 'Item'].astype(int)

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})

    exposure_comparison = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], exposure_comparison[key]) for key in exposure_comparison)
    print(res)
    return res

def get_repo_exposure_decomposition(quarter_date, comp_dict):
    # 'AAAAD956', 'AAAAY826', 'AAAAY829', 'AAAAY831'

    asset_dict = {'AAAAM334': 'Gross assets for repo-style transactions',
                  'AAAAN507': 'Counterparty credit risk',
                  'AAAAY827': 'Exposure amount for repo-style transactions',
                  'AAAAY828': 'Reduction of the gross value of receivables'
                  }

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAM334', 'AAAAN507', 'AAAAY827', 'AAAAY828']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')

    data = data.reset_index()

    data.loc[data[data['Item_ID'] == 'AAAAY828'].index, 'Item'] = -data.loc[data[data['Item_ID'] == 'AAAAY828'].index, 'Item'].astype(int)

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})

    exposure_comparison = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], exposure_comparison[key]) for key in exposure_comparison)
    return res

def get_off_balance_sheet_exposure_decomposition(quarter_date, comp_dict):
    # 'AAAAD956', 'AAAAY826', 'AAAAY829', 'AAAAY831'

    asset_dict = {'AAAAH012': 'Off-balance sheet exposures at gross notional amounts',
                  'AAAAH013': 'Adjustments for conversion to credit equivalent amounts',
                  }

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAH012', 'AAAAH013']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')

    data = data.reset_index()

    data.loc[data[data['Item_ID'] == 'AAAAH013'].index, 'Item'] = -data.loc[data[data['Item_ID'] == 'AAAAH013'].index, 'Item'].astype(int)

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})

    exposure_comparison = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], exposure_comparison[key]) for key in exposure_comparison)
    return res

def get_comparison_asset_exposure_bar(quarter, comp_dict):
    asset_dict = {'AAAA2170': 'Total Consolidated Assets Reported',
                  'AAAAH015': 'Total Leverage Exposure'}

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAA2170', 'AAAAH015']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()

    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res

def get_TC_DA_by_quarter(quarter_from,comp_dict):
    """
    return the QoQ change from Q1 to Q2 2020
    """
    asset_dict = {'AAAB3792': 'Total Capital',
                  'AAAAY826': 'Derivative Exposure',
                  }
    quarter = quarter_from
    a = quarter_from[-1]
    if(a=="4"):
        tmpquarter2 = int(quarter[0:4])
        tmpquarter2 += 1
        quarter2 = str(tmpquarter2)+"Q1"
    else:
        tmpquarter2 = int(quarter[-1])
        tmpquarter2 += 1
        quarter2 = quarter[0:5]+str(tmpquarter2)

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())
    item_names = ['AAAB3792', 'AAAAY826']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter2')
    data2 = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()
    data2 = data2.reset_index()
    data.loc[:,'QoQ']=data.loc[:,'Item'].astype(float)/data2.loc[:,'Item'].astype(float)-1
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'QoQ']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res

def get_total_on_balance_sheet_exposure(quarter_date, comp_dict):

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAD956', 'AAABH015', 'AAAAFS87']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')


    data = data.reset_index()
    data['Item'] = data['Item'].astype(float)
    data.loc[data[data['Item_ID'] == 'AAAAFS87'].index, 'Item'] = np.array(data[data['Item_ID'] == 'AAAAD956']['Item'].to_list()) / np.array(data[data['Item_ID'] == 'AAABH015']['Item'].to_list())


    on_balance_sheet_exposure = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], on_balance_sheet_exposure[key]) for key in on_balance_sheet_exposure)

    return res

def get_derivative_exposure(quarter_date, comp_dict):

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAY826', 'AAABH015', 'AAAAFS87']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')


    data = data.reset_index()
    data['Item'] = data['Item'].astype(float)
    data.loc[data[data['Item_ID'] == 'AAAAFS87'].index, 'Item'] = np.array(data[data['Item_ID'] == 'AAAAY826']['Item'].to_list()) / np.array(data[data['Item_ID'] == 'AAABH015']['Item'].to_list())


    derivative_sheet_exposure = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], derivative_sheet_exposure[key]) for key in derivative_sheet_exposure)

    return res

def get_repo_exposure(quarter_date, comp_dict):

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAY829', 'AAABH015', 'AAAAFS87']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')


    data = data.reset_index()
    data['Item'] = data['Item'].astype(float)
    data.loc[data[data['Item_ID'] == 'AAAAFS87'].index, 'Item'] = np.array(data[data['Item_ID'] == 'AAAAY829']['Item'].to_list()) / np.array(data[data['Item_ID'] == 'AAABH015']['Item'].to_list())


    repo_exposure = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], repo_exposure[key]) for key in repo_exposure)

    return res

def get_offbalance_exposure(quarter_date, comp_dict):

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAAFS90', 'AAABH015', 'AAAAFS87']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')


    data = data.reset_index()
    data['Item'] = data['Item'].astype(float)
    data.loc[data[data['Item_ID'] == 'AAAAFS87'].index, 'Item'] = np.array(data[data['Item_ID'] == 'AAAAFS90']['Item'].to_list()) / np.array(data[data['Item_ID'] == 'AAABH015']['Item'].to_list())


    repo_exposure = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], repo_exposure[key]) for key in repo_exposure)

    return res


def get_leverage_supplementary(quarter_date, comp_dict):
    asset_dict = {'AAAB8274': 'Tier-1 leverage ratio',
                  'AAAAH036': 'Supplementary leverage ratio',
                  'AAAA2170': 'Temp'
                  }

    raw_data = get_data('FFIEC101')
    raw_data.update(raw_data.groupby('Company').ffill())

    item_names = ['AAAB8274', 'AAAA2170', 'AAAAH036']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter_date')


    data = data.reset_index()
    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    data.loc[data[data['Item_ID'] == 'AAAB8274'].index, 'Item'] = (np.array(data[data['Item_ID'] == 'AAAB8274']['Item'].to_list()) / np.array(data[data['Item_ID'] == 'AAAA2170']['Item'].to_list())) * 100

    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    del res['Temp']
    return res


# Line chart overtime comparison:
# 1. Advanced market risk-weighted assets over time
# 2. Change in VaR-based measure over time
# 3. sVaR to VaR ratio over time
# 4. Change in diversification as a percentage of VaR over time
# 5. Change in number of VaR Breaches overtime

# TODO: The returned JSON only contains data in valid quarters
#   for example: quarter_from=2010Q4, quarter_to=2020Q4
#   the overtime analysis functions will only return list data from 2015Q3 to 2020Q4
#   Therefore, the frontend should add NaN values to the series data in echarts option

def get_item_overtime(item_id, quarter_from, quarter_to):
    """
    get item overtime data using item_id from FFIEC102 full csv file directly
    """
    raw_data = get_data('FFIEC101')
    data = raw_data.query('Item_ID == @item_id and Quarter <= @quarter_to and Quarter >= @quarter_from')
    data = data.reset_index()
    data['Item'] = pd.to_numeric(data['Item'])
    item_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    return item_data

def get_item_overtime_for_ratio(item_id, quarter_from, quarter_to):
    """
    get item overtime data using item_id from FFIEC102 full csv file directly
    """
    raw_data = get_data('FFIEC101')
    data = raw_data.query('Item_ID == @item_id and Quarter <= @quarter_to and Quarter >= @quarter_from')
    data = data.reset_index()
    data['Item'] = pd.to_numeric(data['Item'])
    data.loc[data[data['Item_ID'] == item_id[0]].index, 'Item'] = np.array(data[data['Item_ID'] == item_id[0]]['Item'].to_list()) / np.array(data[data['Item_ID'] == item_id[1]]['Item'].to_list())
    data = data[data['Item_ID'] == item_id[0]]

    item_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    return item_data

def get_tier1_capital_overtime(quarter_from, quarter_to, comp_dict):
    tier1_capital_ID= 'AAAB8274'
    item_data = get_item_overtime(tier1_capital_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_tier2_capital_overtime(quarter_from, quarter_to, comp_dict):
    tier2_capital_ID= 'AAAB5311'
    item_data = get_item_overtime(tier2_capital_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_tier1_retainedearnings_overtime(quarter_from, quarter_to, comp_dict):
    tier2_capital_ID= 'AAAB3247'
    item_data = get_item_overtime(tier2_capital_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_tier1_goodwill_overtime(quarter_from, quarter_to, comp_dict):
    tier2_capital_ID= 'AAABP841'
    item_data = get_item_overtime(tier2_capital_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_tier2_ratio_overtime(quarter_from, quarter_to, comp_dict):
    capital_compare = ['AAAB5311', 'AAAB3792']
    item_data = get_item_overtime_for_ratio(capital_compare, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_tier2_minority_int_notin_tier1_overtime(quarter_from, quarter_to, comp_dict):
    minority_int_notin_tier1_ID= 'AAABP868'
    item_data = get_item_overtime(minority_int_notin_tier1_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_tier2_deduction_ratio_overtime(quarter_from, quarter_to, comp_dict):
    deduction_bar = ['AAABP872', 'AAABP870']
    item_data = get_item_overtime_for_ratio(deduction_bar, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_cet1_ratio_overtime(quarter_from, quarter_to, comp_dict):
    cet1_ratio_ID = 'AAABP793'
    item_data = get_item_overtime(cet1_ratio_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)
    return res

def get_tier1_ratio_overtime(quarter_from, quarter_to, comp_dict):
    cet1_ratio_ID = 'AAAB7206'
    item_data = get_item_overtime(cet1_ratio_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)
    return res

def get_total_exposure_overtime(quarter_from, quarter_to, comp_dict):
    total_exp_overtime_ID= 'AAABH015'
    item_data = get_item_overtime(total_exp_overtime_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_CET1vsTier1_overtime(quarter_from, quarter_to, comp_dict):
    CETTierOneComparison = ['AAABP793', 'AAAB7206']
    item_data = get_item_overtime_for_ratio(CETTierOneComparison, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_on_balance_sheet_exp_overtime(quarter_from, quarter_to, comp_dict):
    exposure_comparison_bar = 'AAAAD956'
    item_data = get_item_overtime(exposure_comparison_bar, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_derivative_exp_overtime(quarter_from, quarter_to, comp_dict):
    exposure_comparison_bar = 'AAAAY826'
    item_data = get_item_overtime(exposure_comparison_bar, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_repo_exp_overtime(quarter_from, quarter_to, comp_dict):
    exposure_comparison_bar = 'AAAAY829'
    item_data = get_item_overtime(exposure_comparison_bar, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_off_balance_exp_overtime(quarter_from, quarter_to, comp_dict):
    exposure_comparison_bar = 'AAAAFS90'
    item_data = get_item_overtime(exposure_comparison_bar, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_on_balance_sheet_exp_ratio_overtime(quarter_from, quarter_to, comp_dict):
    exposure_comparison_bar = ['AAAAD956', 'AAABH015']
    item_data = get_item_overtime_for_ratio(exposure_comparison_bar, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_derivative_exposure_ratio_overtime(quarter_from, quarter_to, comp_dict):
    exposure_comparison_bar = ['AAAAY826','AAABH015']
    item_data = get_item_overtime_for_ratio(exposure_comparison_bar, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_repo_exposure_ratio_overtime(quarter_from, quarter_to, comp_dict):
    exposure_comparison_bar = ['AAAAY829','AAABH015']
    item_data = get_item_overtime_for_ratio(exposure_comparison_bar, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_off_balance_sheet_exp_ratio_overtime(quarter_from, quarter_to, comp_dict):
    exposure_comparison_bar = ['AAAAFS90','AAABH015']
    item_data = get_item_overtime_for_ratio(exposure_comparison_bar, quarter_from, quarter_to)

    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res

def get_T2C_TC_ratio_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the ratio of Tier 2 Capital and Total Capital overtime
    """
    raw_data = get_data('FFIEC101')
    total_capital = 'AAAB3792'
    tier_2_capital = 'AAAB5311'
    data = raw_data.query('Item_ID == @total_capital and Quarter <= @quarter_to and '
                          'Quarter >= @quarter_from')

    data_2 = raw_data.query('Item_ID == @tier_2_capital and Quarter <= @quarter_to and '
                            'Quarter >= @quarter_from')
    data.loc[:, 'Item_2'] = data_2.loc[:, 'Item']
    data.loc[:, 'Ratio'] = data.loc[:, 'Item_2'].astype(float) / data.loc[:, 'Item'].astype(float)
    data = data.drop(['Item', 'Item_2'], axis=1).rename(columns={'Ratio': 'Item'})
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res

def get_TC_OBSI_ratio_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the ratio of Total Capital and On Balance Sheet Items overtime
    """
    raw_data = get_data('FFIEC101')
    on_balance_sheet_items = 'AAAAD956'
    total_capital = 'AAAB3792'
    data = raw_data.query('Item_ID == @on_balance_sheet_items and Quarter <= @quarter_to and '
                          'Quarter >= @quarter_from')

    data_2 = raw_data.query('Item_ID == @total_capital and Quarter <= @quarter_to and '
                            'Quarter >= @quarter_from')
    data.loc[:, 'Item_2'] = data_2.loc[:, 'Item']
    data.loc[:, 'Ratio'] = data.loc[:, 'Item_2'].astype(float) / data.loc[:, 'Item'].astype(float)
    data = data.drop(['Item', 'Item_2'], axis=1).rename(columns={'Ratio': 'Item'})
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res

def get_TC_DA_ratio_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the ratio of Total Capital and Derivative Assets overtime
    """
    raw_data = get_data('FFIEC101')
    derivative_assets = 'AAAAY826'
    total_capital = 'AAAB3792'
    data = raw_data.query('Item_ID == @derivative_assets and Quarter <= @quarter_to and '
                          'Quarter >= @quarter_from')

    data_2 = raw_data.query('Item_ID == @total_capital and Quarter <= @quarter_to and '
                            'Quarter >= @quarter_from')
    data.loc[:, 'Item_2'] = data_2.loc[:, 'Item']
    data.loc[:, 'Ratio'] = data.loc[:, 'Item_2'].astype(float) / data.loc[:, 'Item'].astype(float)
    data = data.drop(['Item', 'Item_2'], axis=1).rename(columns={'Ratio': 'Item'})
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res


def get_TC_RA_ratio_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the ratio of Total Capital and Repo Assets overtime
    """
    raw_data = get_data('FFIEC101')
    repo_asset = 'AAAAY829'
    total_capital = 'AAAB3792'
    data = raw_data.query('Item_ID == @repo_asset and Quarter <= @quarter_to and '
                          'Quarter >= @quarter_from')

    data_2 = raw_data.query('Item_ID == @total_capital and Quarter <= @quarter_to and '
                            'Quarter >= @quarter_from')
    data.loc[:, 'Item_2'] = data_2.loc[:, 'Item']
    data.loc[:, 'Ratio'] = data.loc[:, 'Item_2'].astype(float) / data.loc[:, 'Item'].astype(float)
    data = data.drop(['Item', 'Item_2'], axis=1).rename(columns={'Ratio': 'Item'})
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    print(res)
    return res

def get_TC_OffBSI_ratio_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the ratio of Total Capital and Off Balance Sheet Items overtime

    """
    raw_data = get_data('FFIEC101')
    off_balance_sheet_items = 'AAAAY831'
    total_capital = 'AAAB3792'
    data = raw_data.query('Item_ID == @off_balance_sheet_items and Quarter <= @quarter_to and '
                          'Quarter >= @quarter_from')

    data_2 = raw_data.query('Item_ID == @total_capital and Quarter <= @quarter_to and '
                            'Quarter >= @quarter_from')
    data.loc[:, 'Item_2'] = data_2.loc[:, 'Item']
    data.loc[:, 'Ratio'] = data.loc[:, 'Item_2'].astype(float) / data.loc[:, 'Item'].astype(float)
    data = data.drop(['Item', 'Item_2'], axis=1).rename(columns={'Ratio': 'Item'})
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res

def get_RWA_TA_ratio_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the ratio of RWA and Total Assets overtime
    """
    raw_data = get_data('FFIEC101')
    on_balance_sheet_items = 'AAAAD956'
    derivative_assets = 'AAAAY826'
    repo_assets = 'AAAAY829'
    off_balance_sheet_items = 'AAAAY831'
    total_assets = 'AAABA223'
    data = raw_data.query('Item_ID == @on_balance_sheet_items and Quarter <= @quarter_to and '
                          'Quarter >= @quarter_from')
    data3 = raw_data.query('Item_ID == @derivative_assets and Quarter <= @quarter_to and '
                           'Quarter >= @quarter_from')
    data4 = raw_data.query('Item_ID == @repo_assets and Quarter <= @quarter_to and '
                           'Quarter >= @quarter_from')
    data5 = raw_data.query('Item_ID == @off_balance_sheet_items and Quarter <= @quarter_to and '
                           'Quarter >= @quarter_from')
    data_2 = raw_data.query('Item_ID == @total_assets and Quarter <= @quarter_to and '
                            'Quarter >= @quarter_from')


    data.loc[:, 'Item1'] = data.loc[:,'Item'].astype(float)+data3.loc[:, 'Item'].astype(float)+data4.loc[:, 'Item'].astype(float)+data5.loc[:, 'Item'].astype(float)
    data.loc[:, 'Item'] = data_2.loc[:, 'Item']
    data.loc[:, 'Ratio'] = data.loc[:, 'Item'].astype(float) / data.loc[:, 'Item1'].astype(float)
    data = data.drop(['Item', 'Item1'], axis=1).rename(columns={'Ratio': 'Item'})
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res


'''
# VaR sVaR Comparison
def get_VaR_sVaR_item_by_quarter(quarter, comp_dict):
    """
    VaR_sVaR_comparison, return the amount of VaR and sVaR at each quarter in specific quarters
    MRRRS298: Previous day's VaR-based measure
    MRRRS302: Most recent stressed VaR-based measure
    """
    raw_data = get_data('FFIEC102')
    VaR_comp_map = {'MRRRS298': 'VaR', 'MRRRS302': 'SVaR'}
    data = raw_data.query('Item_ID in @VaR_comp_map.keys() and Quarter == @quarter')
    data['Item'] = pd.to_numeric(data['Item'])
    VaR_data = data.groupby('Company')[['Item_ID', 'Item']].apply(item_name_mapping, mapping=VaR_comp_map).to_dict()
    res = dict((comp_dict[key], VaR_data[key]) for key in VaR_data)  # change the id to name
    return res


# Trading asset comparison
def get_trading_asset_item_by_quarter(quarter, comp_dict):
    """
    return the amount of net and gross trading asset at specific quarter
    BHCK3545: Trading Assets
    BHCK3548: Trading Liabilities
    """
    raw_data = get_data('FRY9C')
    trading_asset_item_names_asset = ['BHCK3545']
    trading_asset_item_names_liability = ['BHCK3548']
    trading_asset_item_names = ['BHCK3545', 'BHCK3548']
    data = raw_data.query('Item_ID in @trading_asset_item_names and Quarter == @quarter')
    data_asset = raw_data.query('Item_ID in @trading_asset_item_names_asset and Quarter == @quarter')
    data_liability = raw_data.query('Item_ID in @trading_asset_item_names_liability and Quarter == @quarter')

    data_asset.loc[:, 'Item_2'] = data_liability.loc[:, 'Item']
    data_asset.loc[:, 'Gross'] = data_asset.loc[:, 'Item'].astype(int) + data_asset.loc[:, 'Item_2'].astype(int)
    data_asset.loc[:, 'Net'] = data_asset.loc[:, 'Item'].astype(int) - data_asset.loc[:, 'Item_2'].astype(int)
    data_asset = data_asset.drop(['Item', 'Item_2'], axis=1)
    data_asset = data_asset.reset_index()
    whole_val = []
    Flag = 1
    for index, row in data_asset.iterrows():
        if Flag == 1:
            whole_val.append(row['Gross'])
            Flag = -1
        if Flag == -1:
            whole_val.append(row['Net'])
            Flag = 1
    new = pd.Series(whole_val)
    data.loc[:, 'Item'] = new.values
    trading_asset_map = {'BHCK3545': 'Net Trading Asset', 'BHCK3548': 'Gross Trading Asset'}
    trading_asset_data = data.groupby('Company')[['Item_ID', 'Item']].apply(item_name_mapping, mapping=trading_asset_map).to_dict()
    res = dict((comp_dict[key], trading_asset_data[key]) for key in trading_asset_data)  # change the id to name
    return res


def name_list_mapping(x, keys):
    values = x.values.tolist()[0]
    return dict(zip(keys, values))


def get_asset_to_var_ratio_item_by_quarter(quarter, comp_dict):
    """
    return trading asset to risk ratio in specific quarters,
    the ratios order is: 'Net/VaR', 'Gross/VaR', 'Net/sVaR', 'Gross/sVaR'
    """
    raw_data_var = get_data('FFIEC102')
    raw_data_asset = get_data('FRY9C')
    var_item_names = ['MRRRS298', 'MRRRS302']
    data_var = raw_data_var.query('Item_ID in @var_item_names and Quarter == @quarter').reset_index()

    data_var1 = data_var[data_var['Item_ID'] == 'MRRRS298'].rename(columns={'Item': 'VaR'}).drop(['Item_ID'], axis=1)
    data_var2 = data_var[data_var['Item_ID'] == 'MRRRS302'].rename(columns={'Item': 'sVaR'}).drop(['Item_ID'], axis=1)
    data_var = pd.merge(data_var1, data_var2, on=['Company', 'Quarter']).reset_index(drop=True)
    data_var[['VaR', 'sVaR']] = data_var[['VaR', 'sVaR']].astype('int')

    trading_asset_item_names_asset = ['BHCK3545']
    trading_asset_item_names_liability = ['BHCK3548']
    trading_asset_item_names = ['BHCK3545', 'BHCK3548']
    data = raw_data_asset.query('Item_ID in @trading_asset_item_names and Quarter == @quarter')
    data_asset = raw_data_asset.query('Item_ID in @trading_asset_item_names_asset and Quarter == @quarter')
    data_liability = raw_data_asset.query('Item_ID in @trading_asset_item_names_liability and Quarter == @quarter')
    data_asset.loc[:, 'Item_2'] = data_liability.loc[:, 'Item']
    data_asset.loc[:, 'Gross'] = data_asset.loc[:, 'Item'].astype(int) + data_asset.loc[:, 'Item_2'].astype(int)
    data_asset.loc[:, 'Net'] = data_asset.loc[:, 'Item'].astype(int) - data_asset.loc[:, 'Item_2'].astype(int)
    data_asset = data_asset.drop(['Item', 'Item_2', 'Item_ID'], axis=1)
    data_asset = data_asset.reset_index()

    tot_data = pd.merge(data_var, data_asset, on=['Company', 'Quarter'])
    tot_data['Net/VaR'] = tot_data['Net'] / tot_data['VaR']
    tot_data['Gross/VaR'] = tot_data['Gross'] / tot_data['VaR']
    tot_data['Net/sVaR'] = tot_data['Net'] / tot_data['sVaR']
    tot_data['Gross/sVaR'] = tot_data['Gross'] / tot_data['sVaR']
    tot_data = tot_data.drop(['VaR', 'sVaR', 'Gross', 'Net'], axis=1)

    # You can just remember the name and order of this 4 things...

    ratio_list = ['Net Trading \nAsset / VaR', 'Gross Trading \nAsset / VaR',
                  'Net Trading \nAsset / sVaR', 'Gross Trading \nAsset / sVaR']
    total_data = tot_data.groupby('Company')[['Net/VaR', 'Gross/VaR', 'Net/sVaR', 'Gross/sVaR']].apply(name_list_mapping, keys=ratio_list).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res


# TODO: remove SettingWithCopyWarning in pandas
def get_revenue_to_var_ratio_item_by_quarter(quarter, comp_dict):
    """
    return trading revenue to VaR and sVaR ratios in specific quarters,
    the ratios order is: 'revenue/VaR', 'revenue/sVaR'
    """
    raw_data_var = get_data('FFIEC102')
    raw_data_revenue = get_data('FRY9C')
    var_item_names = ['MRRRS298', 'MRRRS302']
    data_var = raw_data_var.query('Item_ID in @var_item_names and Quarter == @quarter').reset_index()

    data_var1 = data_var[data_var['Item_ID'] == 'MRRRS298'].rename(columns={'Item': 'VaR'}).drop(['Item_ID'], axis=1)
    data_var2 = data_var[data_var['Item_ID'] == 'MRRRS302'].rename(columns={'Item': 'sVaR'}).drop(['Item_ID'], axis=1)
    data_var = pd.merge(data_var1, data_var2, on=['Company', 'Quarter']).reset_index(drop=True)
    data_var[['VaR', 'sVaR']] = data_var[['VaR', 'sVaR']].astype('int')

    trading_revenue_item_names = ['BHCKA220']
    data_revenue = raw_data_revenue.query('Item_ID in @trading_revenue_item_names and Quarter == @quarter')

    tot_data = pd.merge(data_var, data_revenue, on=['Company', 'Quarter']).rename(columns={'Item': 'revenue'})
    tot_data.loc[:, 'revenue/VaR'] = tot_data.loc[:, 'revenue'].astype(int) / tot_data.loc[:, 'VaR']
    tot_data.loc[:, 'revenue/sVaR'] = tot_data.loc[:, 'revenue'].astype(int) / tot_data.loc[:, 'sVaR']
    tot_data = tot_data.drop(['VaR', 'sVaR', 'revenue', 'Item_ID'], axis=1)

    # You can just remember the name and order of these 2 things...
    ratio_list = ['Trading Revenue / VaR', 'Trading Revenue / sVaR']
    total_data = tot_data.groupby('Company')[['revenue/VaR', 'revenue/sVaR']].apply(name_list_mapping, keys=ratio_list).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res


# Stack bar chart quarterly comparison:
# 1. Standardized market risk-weighted assets breakdown by bank
# 2. VaR by Asset Class and Diversification Effect


# Standardized market risk-weighted assets breakdown by bank
def get_standardized_risk_weighted_assets_by_quarter(quarter, comp_dict):
    """
    return the amount of standardized market risk-weighted assets breakdown by bank in specific quarter
    """
    asset_dict = {'MRRRS345': 'De Minimis',
                  'MRRRS341': 'Std Comprehensive Risk',
                  'MRRRS315': 'Incremental Risk',
                  'MRRRS311': 'Add-Ons',
                  'MRRRS304': 'sVaR',
                  'MRRRS301': 'VaR'}

    raw_data = get_data('FFIEC102')
    raw_data.update(raw_data.groupby('Company').ffill())
    item_names = ['MRRRS345', 'MRRRS341', 'MRRRS315', 'MRRRS311', 'MRRRS304', 'MRRRS301']
    data = raw_data.query('Item_ID in @item_names and Quarter == @quarter')
    data = data.reset_index()
    data['Item'] = data['Item'].astype(float)
    data = data.replace({'Company': comp_dict})
    total_data = data.groupby('Item_ID')[['Company', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], total_data[key]) for key in total_data)
    return res


# VaR by Asset Class and Diversification Effect
def get_asset_class_var_item_by_quarter(quarter, comp_dict):
    """
    return VaR percentage in different asset classes and diversification effect of companies in specific quarter
    Previous day's VaR:
    IR='MRRRS348' Debt='MRRRS349' Equity='MRRRS350' FX='MRRRS351' Commodities='MRRRS352'
    """
    raw_data = get_data('FFIEC102')
    asset_classesID = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']
    asset_dict = {'MRRRS348': 'IR',
                  'MRRRS349': 'Debt',
                  'MRRRS350': 'Equity',
                  'MRRRS351': 'FX',
                  'MRRRS352': 'Commodities',
                  'MRRRS298': 'Diversification'}

    data_asset = raw_data.query('Item_ID in @asset_classesID and Quarter == @quarter')
    data_asset = data_asset.reset_index()
    data_asset['Item'] = data_asset.Item.astype(int)
    data_asset['total_asset_var'] = data_asset.groupby('Company')['Item'].transform('sum')

    varID = ['MRRRS298']
    data_day_var = raw_data.query('Item_ID in @varID and Quarter == @quarter')
    data_day_var = data_day_var.reset_index()
    data_day_var['Item'] = data_day_var.Item.astype(int)

    data = data_asset.append(data_day_var)
    data = data.replace({'Company': comp_dict})
    data.update(data.groupby('Company').ffill())
    data['total_asset_var'] = data.total_asset_var.astype(int)
    data['asset_var_by_percentage'] = 100 * (data.Item / data.total_asset_var)
    data.loc[data.Item_ID == 'MRRRS298', 'asset_var_by_percentage'] =\
        100 * \
        (data.loc[data.Item_ID == 'MRRRS298', 'Item']-data.loc[data.Item_ID == 'MRRRS298', 'total_asset_var'])/ \
        data.loc[data.Item_ID == 'MRRRS298', 'total_asset_var']
    data.sort_values(by='Company', inplace=True)
    output_data = data.groupby('Item_ID')[['Company', 'asset_var_by_percentage']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((asset_dict[key], output_data[key]) for key in output_data)  # change the id to name
    return res


# Bar line chart quarterly comparison:
# 1. Trading Assets and Change
# 2. Trading Liabilities and Change
# 3. Net Trading Assets and Change
# 3. Gross Trading Assets and Change


def get_trading_item_and_change_by_quarter(item_id, item_name, quarter, comp_dict):
    pre_quarter = get_previous_quarter(quarter)
    raw_data_asset = get_data('FRY9C')
    data_last = raw_data_asset.query('Item_ID == @item_id and Quarter == @pre_quarter').reset_index()
    data_current = raw_data_asset.query('Item_ID == @item_id and Quarter == @quarter').reset_index()
    data = pd.merge(data_last, data_current, on='Company', how='right', validate="one_to_one")
    data['Item_x'] = data.Item_x.astype(float)
    data['Item_y'] = data.Item_y.astype(float)
    data['percentage_change'] = 100 * (data.Item_y - data.Item_x) / data.Item_x
    data.rename(columns={'Item_y': item_name}, inplace=True)
    output_data = data.groupby('Company')[[item_name, 'percentage_change']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], output_data[key]) for key in output_data)
    return res


# Trading Assets and Change
def get_trading_assets_and_change_by_quarter(quarter, comp_dict):
    item_id, item_name = 'BHCK3545', 'Trading_Assets'
    res = get_trading_item_and_change_by_quarter(item_id, item_name, quarter, comp_dict)
    return res


# Trading Liabilities and Change
def get_trading_liabilities_and_change_by_quarter(quarter, comp_dict):
    item_id, item_name = 'BHCK3548', 'Trading_Liabilities'
    res = get_trading_item_and_change_by_quarter(item_id, item_name, quarter, comp_dict)
    return res


def calculate_trading_asset_and_percent_change(cal_type, quarter, comp_dict):
    op_dict = {"Net": operator.sub, "Gross": operator.add}
    op = op_dict[cal_type]
    pre_quarter = get_previous_quarter(quarter)
    raw_data_asset = get_data('FRY9C')
    trading_asset = 'BHCK3545'
    trading_liability = 'BHCK3548'
    data_asset_last = raw_data_asset.query('Item_ID == @trading_asset and Quarter == @pre_quarter')
    data_asset_current = raw_data_asset.query('Item_ID == @trading_asset and Quarter == @quarter')
    data_liability_last = raw_data_asset.query('Item_ID == @trading_liability and Quarter == @pre_quarter')
    data_liability_current = raw_data_asset.query('Item_ID == @trading_liability and Quarter == @quarter')

    data_asset_last.loc[:, 'Item_2'] = data_liability_last.loc[:, 'Item']
    data_asset_last.loc[:, cal_type] = op(data_asset_last.loc[:, 'Item'].astype(int), data_asset_last.loc[:, 'Item_2'].astype(int))
    data_asset_current.loc[:, 'Item_2'] = data_liability_current.loc[:, 'Item']
    data_asset_current.loc[:, cal_type] = op(data_asset_current.loc[:, 'Item'].astype(int), data_asset_current.loc[:, 'Item_2'].astype(int))
    data_asset_current = data_asset_current.drop(['Item', 'Item_2'], axis=1)
    data_asset_current = data_asset_current.reset_index()
    data_asset_last = data_asset_last.drop(['Item', 'Item_2'], axis=1)
    data_asset_last = data_asset_last.reset_index()

    data = pd.merge(data_asset_last, data_asset_current, on='Company', how='right', validate='one_to_one')
    pre_quarter_net, cur_quarter_net = cal_type + '_x', cal_type + '_y'
    data[pre_quarter_net] = data[pre_quarter_net].astype(float)
    data[cur_quarter_net] = data[cur_quarter_net].astype(float)
    data['percent_change'] = 100 * (data[cur_quarter_net] - data[pre_quarter_net]) / data[pre_quarter_net]
    trading_asset_item_name = cal_type + "_Trading_Assets"
    data.rename(columns={cur_quarter_net: trading_asset_item_name}, inplace=True)
    net_data = data.groupby('Company')[[trading_asset_item_name, 'percent_change']].apply(
        lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], net_data[key]) for key in net_data)
    return res


# Net trading asset by quarter (bar chart) and percent change from last quarter (line chart)
def get_net_trading_asset_and_percent_change_by_quarter(quarter, comp_dict):
    res = calculate_trading_asset_and_percent_change("Net", quarter, comp_dict)
    return res


# Gross trading asset by quarter (bar chart) and percent change from last quarter (line chart)
def get_gross_trading_asset_and_percent_change_by_quarter(quarter, comp_dict):
    res = calculate_trading_asset_and_percent_change("Gross", quarter, comp_dict)
    return res





# Advanced market risk-weighted assets
def get_risk_weighted_asset_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the amount of advanced market risk weighted assets overtime
    MRRRS347: MARKET RISK-WEIGHTED ASSETS
    """
    advanced_market_risk_weighted_assets_ID = 'MRRRS347'
    item_data = get_item_overtime(advanced_market_risk_weighted_assets_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res


# VaR-based measure overtime
def get_var_measure_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the amount of VaR-based measure overtime
    MRRRS298: Previous day's VaR-based measure
    """
    VaR_based_measure_overtime_ID = 'MRRRS298'
    item_data = get_item_overtime(VaR_based_measure_overtime_ID, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)  # change the id to name
    return res


# sVaR to VaR ratio overtime
def get_ratio_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the ratio of sVaR and VaR overtime
    MRRRS298: Previous day's VaR-based measure
    MRRRS302: Most recent stressed VaR-based measure
    """
    raw_data = get_data('FFIEC102')
    VaR_based_measure_overtime_ID = 'MRRRS298'
    sVaR_based_measure_overtime_ID = 'MRRRS302'
    data = raw_data.query('Item_ID == @VaR_based_measure_overtime_ID and Quarter <= @quarter_to and '
                          'Quarter >= @quarter_from')

    data_2 = raw_data.query('Item_ID == @sVaR_based_measure_overtime_ID and Quarter <= @quarter_to and '
                            'Quarter >= @quarter_from')
    data.loc[:, 'Item_2'] = data_2.loc[:, 'Item']
    data.loc[:, 'Ratio'] = data.loc[:, 'Item_2'].astype(int) / data.loc[:, 'Item'].astype(int)
    data = data.drop(['Item', 'Item_2'], axis=1).rename(columns={'Ratio': 'Item'})
    data = data.reset_index()
    asset_data = data.groupby('Company')[['Quarter', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], asset_data[key]) for key in asset_data)  # change the id to name
    return res


# Change in diversification as a percentage of VaR over time
def get_var_diversification_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the amount of diversification as a percentage of VaR overtime
    """
    raw_data = get_data('FFIEC102')
    asset_classesID = ['MRRRS348', 'MRRRS349', 'MRRRS350', 'MRRRS351', 'MRRRS352']

    data_asset = raw_data.query('Item_ID in @asset_classesID and Quarter <= @quarter_to and '
                                'Quarter >= @quarter_from')
    data_asset = data_asset.reset_index()
    data_asset['Item'] = data_asset.Item.astype(int)
    data_asset['total_asset_var'] = data_asset.groupby(['Company', 'Quarter'])['Item'].transform('sum')

    varID = 'MRRRS298'
    data_day_var = raw_data.query('Item_ID == @varID and Quarter<= @quarter_to and Quarter >= @quarter_from')
    data_day_var = data_day_var.reset_index()
    data_day_var['Item'] = data_day_var.Item.astype(int)

    data = data_asset.append(data_day_var)
    data.update(data.groupby(['Company', 'Quarter']).ffill())

    data['total_asset_var'] = data.total_asset_var.astype(int)
    data = data.loc[data.Item_ID == 'MRRRS298']

    data['diver_as_percent_of_Var'] = 100 * (data.total_asset_var-data.Item)/data.total_asset_var

    output_data = data.groupby('Company')[['Quarter', 'diver_as_percent_of_Var']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], output_data[key]) for key in output_data)  # change the id to name
    return res


# Change in number of VaR Breaches overtime
def get_num_var_breach_item_overtime(quarter_from, quarter_to, comp_dict):
    """
    return the amount of the number of VaR breaches overtime
    MRRRS362: Number of trading days in the calendar quarter where the trading day's trading loss
    exceeded the respective VaR estimate
    """
    num_bar_breach_id = 'MRRRS362'
    item_data = get_item_overtime(num_bar_breach_id, quarter_from, quarter_to)
    res = dict((comp_dict[key], item_data[key]) for key in item_data)
    return res


# Stress window overtime
def get_stress_window_item_overtime(quarter_date_from, quarter_date_to, comp_dict):
    """
    return the classification of stress window under criteria:
    if year in 2007/2008, then it is 2008 Financial Crisis;
    if year in 2019, then it is Covid 19
    """
    raw_data = get_data('FFIEC102')
    item_names = ['MRRRS366']
    data = raw_data.query('Item_ID in @item_names and Quarter <= @quarter_date_to and '
                          'Quarter >= @quarter_date_from')
    data = data.reset_index()
    for i in range(len(data['Item'])):
        if '2007' in data.loc[i, 'Item'] or '2008' in data.loc[i, 'Item']:
            data.loc[i, 'Item'] = '2008 Financial Crisis'
        if '2019' in data.loc[i, 'Item']:
            data.loc[i, 'Item'] = 'Covid 19'
    total_data = data.groupby('Company')[['Item_ID', 'Item']].apply(lambda x: x.values.tolist()).to_dict()
    res = dict((comp_dict[key], total_data[key]) for key in total_data)
    return res
'''