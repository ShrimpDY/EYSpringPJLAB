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

@bp.route('/getOverallExposureAdjustStack', methods=['GET'])
def getOverallExposureAdjustStack():
    quarter = request.args['quarter']
    result = get_exposure_adjustment_stack(quarter, session.get("comp_dict"))
    return response_processing(result)

@bp.route('/getTotalExposureOvertime', methods=['GET'])
def getTotalExposureOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_total_exposure_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


