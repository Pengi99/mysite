from flask import Flask, request, render_template, url_for
import pandas as pd
import invest


app = Flask(__name__)

@app.route('/invest')
def invest():
    return render_template('invest.html')


@app.route('/dashboard')
def dashboard():
    input_code = request.args['code']
    input_year = request.args['month']
    input_month = request.args['year']
    input_day = request.args['day']
    input_time = f'{input_year}-{input_month}-{input_day}'
    input_type = request.args['type']

    df = invest.load_data(input_code, input_time)
    invest_class = invest.Invest(df, _col='Close', _start=input_time)
    if input_type == 'bnh':
        result = invest_class.buyandhold()
    elif input_type == 'boll':
        result = invest_class.bollinger()
    elif input_type == 'mmt':
        result = invest_class.momentum()
    result.reset_index(inplace=True)
    result = result[['Date', 'Close', 'trade', 'rtn', 'acc_rtn']]
    result.columns = ['시간', '종가', '보유내역', '일별 수익율', '누적 수익율']
    cols_list = list(result.columns)
    dict_data = result.to_dict(orient='records')
    x_data = list(result['시간'])
    y_data = list(result['일별 수익율'])
    y1_data = list(result['누적 수익율'])
    return render_template('dashboard.html',
                           table_cols=cols_list,
                           table_data=dict_data,
                           x_data=x_data,
                           y_data=y_data,
                           y1_data=y1_data)

app.run(debug=True)