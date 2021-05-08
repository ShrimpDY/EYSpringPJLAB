import logging
import urllib3
from flask import jsonify, request, Blueprint, session, current_app
from flask_cors import CORS
from backend.data_process import load_data_config_file, init_data, add_data
from backend.backend_analysis_plotting import *

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bp = Blueprint("views", __name__)
# cors = CORS(bp, resources={r"/getMsg": {"origins": "*"}})
CORS(bp, supports_credentials=True)


def updateCompDict(data_info):
    comp_dict = {rssd_id: info['Nick'] for rssd_id, info in data_info['institutions'].items()}
    session["comp_dict"] = comp_dict
    session['data_loaded'] = True
    session.permanent = True


# TODO: When visiting the homepage, we may add some logic to update the data periodically
#   instead of clicking the update button to update the data manually.
#   For example, updating the data every quarter
@bp.route('/home', methods=('GET', 'POST'))
def index():
    """
    Currently if 'data_status' is in data config file and data folder exists,
    no need to update data each time we visit the homepage
    """
    config_info = load_data_config_file()
    institution_info = config_info["institutions"]
    need_update = False
    for rssd_id in institution_info:
        if 'data_status' not in institution_info[rssd_id]:
            need_update = True
    path = os.path.join(get_cur_path(), 'data/raw_data')
    if not os.path.exists(path):
        need_update = True
    data_info = init_data() if need_update else config_info
    updateCompDict(data_info)
    response = jsonify(data_info)
    return response


@bp.route('/updateData', methods=('GET', 'POST'))
def updateData():
    """
    Update all data for companies in the data_setting.json file
    """
    data_info = init_data()
    response = jsonify(data_info)
    updateCompDict(data_info)
    return response


@bp.route('/addDataByID', methods=['GET', 'POST'])
def addData():
    args = request.args
    rssd_id = args['rssd_id']
    name = args['name']
    nick_name = args['nickName']
    res = add_data(rssd_id, name, nick_name)
    data_info = load_data_config_file()
    updateCompDict(data_info)
    return jsonify(res)


# TODO: better implementation using CORS and session at the same time
#   Currently, we need to add request and response headers to make session works under CORS
#   And the frontend host should be specified in the config.py and used in the response header
def response_processing(result):
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', current_app.config['FRONT_END_HOST'])
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@bp.route('/getVaRsVarRComparison', methods=['GET'])
def getVaRsVarRComparison():
    quarter = request.args['quarter']
    logging.info("getVaRsVarRComparison comp_dict: %s", session["comp_dict"])
    result = get_VaR_sVaR_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingAssetComparison', methods=['GET'])
def getTradingAssetComparison():
    quarter = request.args['quarter']
    result = get_trading_asset_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingAssetToRiskRatio', methods=['GET'])
def getTradingAssetToRiskRatio():
    quarter = request.args['quarter']
    result = get_asset_to_var_ratio_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingRevenueToVarRatio', methods=['GET'])
def getTradingRevenueToVarRatio():
    quarter = request.args['quarter']
    result = get_revenue_to_var_ratio_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getStandardizedRiskWeightedAssets', methods=['GET'])
def getStandardizedRiskWeightedAssets():
    quarter = request.args['quarter']
    result = get_standardized_risk_weighted_assets_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getVaRByAssetClassDiversification', methods=['GET'])
def getVaRByAssetClassDiversification():
    quarter = request.args['quarter']
    result = get_asset_class_var_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingAssetsAndChangeByQuarter', methods=['GET'])
def getTradingAssetsAndChangeByQuarter():
    quarter = request.args['quarter']
    result = get_trading_assets_and_change_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingLiabilitiesAndChangeByQuarter', methods=['GET'])
def getTradingLiabilitiesAndChangeByQuarter():
    quarter = request.args['quarter']
    result = get_trading_liabilities_and_change_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getNetTradingAssetAndPercentChange', methods=['GET'])
def getNetTradingAssetAndPercentChange():
    quarter = request.args['quarter']
    result = get_net_trading_asset_and_percent_change_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getGrossTradingAssetAndPercentChange', methods=['GET'])
def getGrossTradingAssetAndPercentChange():
    quarter = request.args['quarter']
    result = get_gross_trading_asset_and_percent_change_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getAdvancedMarketRiskWeightedAssets', methods=['GET'])
def getAdvancedMarketRiskWeightedAssets():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_risk_weighted_asset_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getChangeInVaRBasedMeasureOvertime', methods=['GET'])
def getChangeInVaRBasedMeasureOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_var_measure_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getVaRsVaRRatioOvertime', methods=['GET'])
def getVaRsVaRRatioOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_ratio_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getVaRBreachOvertime', methods=['GET'])
def getVaRBreachOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_num_var_breach_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getDiversificationVarOvertime', methods=['GET'])
def getDiversificationVarOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_var_diversification_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getStressWindowOvertime', methods=['GET'])
def getStressWindowOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = get_stress_window_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return jsonify(res)
