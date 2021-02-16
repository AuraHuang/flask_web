from flask import Blueprint, request, render_template, jsonify, redirect, url_for, flash, make_response
from werkzeug.utils import secure_filename
from apps.shares_resturn import shares_return
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from io import StringIO
import csv

shares_return_bp = Blueprint('shares_return', __name__)


@shares_return_bp.route("/", methods=['GET', 'POST'])
def index():
    try:

        if request.method == 'POST':

            # 轉借券餘額檔案
            detail_file = request.files.get('upload_detail_file')
            detail_data = secure_filename(detail_file.filename)
            detail_data = pd.read_csv(detail_file, encoding='ANSI')
            
            # 還券交易單
            return_file = request.files.get('upload_return_file')
            sheetname_1 = request.form['sheetname_1']
            sheetname_2 = request.form['sheetname_2']
            return_file = load_workbook(return_file)
            ws_1 = return_file[sheetname_1]
            ws_2 = return_file[sheetname_2]
            # 客戶還券（Return Detail）
            return_detail = pd.DataFrame(ws_1.values).dropna(how='any')
            return_detail = return_detail.iloc[:,1:]
            return_detail.columns = return_detail.iloc[0]
            return_detail = return_detail.iloc[1:].reset_index(drop=True)
            # Recall總計（Recall 雅）
            recall_detail = pd.DataFrame(ws_2.values).dropna(how='any')
            recall_detail = recall_detail.iloc[:,1:]
            recall_detail.columns = recall_detail.iloc[0]
            recall_detail = recall_detail.iloc[1:].reset_index(drop=True)

            # 自然人提前還券檔案
            retail_file = request.files.get('upload_retail_file')
            retail_file = retail_file.read()
            retail_file = str(retail_file, 'ANSI')
            rows = retail_file.split('\n')
            retail_detail = pd.DataFrame([np.char.strip(row.split(';')) for row in rows]).dropna(how='any').reset_index(drop=True)
            retail_detail.columns = retail_detail.iloc[0]
            retail_detail = retail_detail.replace('', np.nan).dropna(how='any', axis=1).reset_index(drop=True)
            retail_detail = retail_detail.iloc[1:].reset_index(drop=True)
            retail_detail['公司'] = retail_detail['公司'].astype(int)
            retail_detail['客戶帳號'] = retail_detail['客戶帳號'].str[2:-1].astype(int)
            retail_detail['股票代號'] = retail_detail['股票代號'].str[2:-1].astype(int)
            retail_detail['未還張數'] = retail_detail['未還張數'].astype(int)
            retail_detail['費率'] = retail_detail['費率'].astype(float)
            retail_detail['最後處理日期'] = retail_detail['最後處理日期'].astype(int)

            csvlist = [['8800 還券交易單'], ['還券申請日：'], ['a','b','c']]
            si = StringIO()
            cw = csv.writer(si)
            cw.writerows(csvlist)
            # utf-8-sig or ANSI
            output = make_response(si.getvalue().encode('utf-8-sig'))
            # 檔名用日期.序號.csv
            output.headers["Content-Disposition"] = "attachment; filename=export.csv"
            output.headers["Content-type"] = "text/csv"
            return output
                

        return render_template('shares_return/index.html')

    except Exception as e:
        raise e
