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

## Graphs in the quarterly highlihghts key
@bp.route('/getTotalCapitalStack', methods=['GET'])
def getTotalCapitalStack():
    quarter = request.args['quarter']
    result = get_total_capital_stack(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTotalRWA', methods=['GET'])
def getTotalRWA():
    quarter = request.args['quarter']
    result = get_total_RWA_bar(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getKeyRatios', methods=['GET'])
def getKeyRatios():
    quarter = request.args['quarter']
    result = key_ratio_comparison_bar(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getBufferStack', methods=['GET'])
def getBufferStack():
    quarter = request.args['quarter']
    result = get_buffer_stack(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTotalExposureDecomposition', methods=['GET'])
def getTotalExposureDecomposition():
    quarter = request.args['quarter']
    result = get_total_exposure_decomposition(quarter, session.get("comp_dict"))
    return response_processing(result)

## Graphs in the quarterly highlights detail
@bp.route('/getTierIDeductionsAdjustStack', methods=['GET'])
def getTierIDeductionsAdjustStack():
    quarter = request.args['quarter']
    result = get_tier1deductions_adjustment_stack(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTierICompositionStack', methods=['GET'])
def getTierICompositionStack():
    quarter = request.args['quarter']
    result = get_tier1composition_stack(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTierIIDeductionsAdjustStack', methods=['GET'])
def getTierIIDeductionsAdjustStack():
    quarter = request.args['quarter']
    result = get_tier2deduction_adjustment_stack(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTierIIBeforeDeductionStack', methods=['GET'])
def getTierIIBeforeDeductionStack():
    quarter = request.args['quarter']
    result = get_tier2_before_deduction_stack(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getOverallExposureAdjustStack', methods=['GET'])
def getOverallExposureAdjustStack():
    quarter = request.args['quarter']
    result = get_exposure_adjustment_stack(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getAssetExposureComparison', methods=['GET'])
def getAssetExposureComparison():
    quarter = request.args['quarter']
    result = get_comparison_asset_exposure_bar(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTCDA', methods=['GET'])
def getTCDA():
    quarter = request.args['quarter']
    result = get_TC_DA_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getLeverageSup', methods=['GET'])
def getLeverageSup():
    quarter = request.args['quarter']
    result = get_leverage_supplementary(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTotalOnBalanceSheetExposure', methods=['GET'])
def getTotalOnBalanceSheetExposure():
    quarter = request.args['quarter']
    result = get_total_on_balance_sheet_exposure(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getDerivativeExposure', methods=['GET'])
def getDerivativeExposure():
    quarter = request.args['quarter']
    result = get_derivative_exposure(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getRepoExposure', methods=['GET'])
def getRepoExposure():
    quarter = request.args['quarter']
    result = get_repo_exposure(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getOffBalanceExposure', methods=['GET'])
def getOffBalanceExposure():
    quarter = request.args['quarter']
    result = get_offbalance_exposure(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTotalOnBalanceSheetExposureDecomp', methods=['GET'])
def getTotalOnBalanceSheetExposureDecomp():
    quarter = request.args['quarter']
    result = get_on_balance_sheet_exposure_decomposition(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getDerivativeExposureDecomp', methods=['GET'])
def getDerivativeExposureDecomp():
    quarter = request.args['quarter']
    result = get_derivative_exposure_decomposition(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getRepoExposureDecomp', methods=['GET'])
def getRepoExposureDecomp():
    quarter = request.args['quarter']
    result = get_repo_exposure_decomposition(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getOffBalanceSheetExposureDecomp', methods=['GET'])
def getOffBalanceSheetExposureDecomp():
    quarter = request.args['quarter']
    result = get_off_balance_sheet_exposure_decomposition(quarter, session.get("comp_dict"))
    return response_processing(result)

## Overtime Analysis
@bp.route('/getTier1CapitalOvertime', methods=['GET'])
def getTier1CapitalOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_tier1_capital_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTier2CapitalOvertime', methods=['GET'])
def getTier2CapitalOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_tier2_capital_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTier1RetainedEarningOvertime', methods=['GET'])
def getTier1RetainedEarningOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_tier1_retainedearnings_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTier1GoodwillOvertime', methods=['GET'])
def getTier1GoodwillOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_tier1_goodwill_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTier2MinorityIntOvertime', methods=['GET'])
def getTier2MinorityIntOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_tier2_minority_int_notin_tier1_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTier2CapitalRatioOvertime', methods=['GET'])
def getTier2CapitalRatioOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_tier2_ratio_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTier2DeductionOvertime', methods=['GET'])
def getTier2DeductionOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_tier2_deduction_ratio_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getCET1RatioOvertime', methods=['GET'])
def getCET1RatioOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_cet1_ratio_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTier1RatioOvertime', methods=['GET'])
def getTier1RatioOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_tier1_ratio_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getCETVsTier1RatioOvertime', methods=['GET'])
def getCETVsTier1RatioOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_CET1vsTier1_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTotalExposureOvertime', methods=['GET'])
def getTotalExposureOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_total_exposure_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getOnBalanceSheetOvertime', methods=['GET'])
def getOnBalanceSheetOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_on_balance_sheet_exp_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getDerivativeOvertime', methods=['GET'])
def getDerivativeOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_derivative_exp_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getRepoOvertime', methods=['GET'])
def getRepoOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_repo_exp_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getOffBalanceOvertime', methods=['GET'])
def getOffBalanceOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_off_balance_exp_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getOnBalanceSheetRatio', methods=['GET'])
def getOnBalanceSheetRatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_on_balance_sheet_exp_ratio_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getDerivativeExposureRatio', methods=['GET'])
def getDerivativeExposureRatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_derivative_exposure_ratio_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getRepoExposureRatio', methods=['GET'])
def getRepoExposureRatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_repo_exposure_ratio_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getOffBalanceExposureRatio', methods=['GET'])
def getOffBalanceExposureRatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_off_balance_sheet_exp_ratio_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getT2CTCRatio', methods=['GET'])
def getT2CTCRatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_T2C_TC_ratio_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTCOBSIRatio', methods=['GET'])
def getTCOBSIRatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_TC_OBSI_ratio_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTCDARatio', methods=['GET'])
def getTCDARatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_TC_DA_ratio_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTCRARatio', methods=['GET'])
def getTCRARatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_TC_RA_ratio_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTCOFFBSIRatio', methods=['GET'])
def getTCOFFBSIRatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_TC_OffBSI_ratio_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getRWATARatio', methods=['GET'])
def getRWATARatio():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_RWA_TA_ratio_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


