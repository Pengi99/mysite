from flask import Flask, request, render_template, url_for, redirect, session
import pandas as pd
import invest
from database import MyDB
from dotenv import load_dotenv
import os
from data import querys

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('secret')

mydb = MyDB(
    host = os.getenv('host'),
    port = int(os.getenv('port')),
    user = os.getenv('user'),
    pwd = os.getenv('pwd'),
    db = os.getenv('db')
)

mydb.execute_query(querys.create_query)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin', methods=['post'])
def signin():
    input_id = request.form['id']
    input_pass = request.form['password']

    login_result = mydb.execute_query(querys.login_query, input_id, input_pass)

    if len(login_result) == 1:
        session['user_info'] = [input_id, input_pass]
        return redirect('/invest')
    else:
        return redirect('/')


@app.route('/signup2', methods=['post'])
def signup2():
    input_id = request.form['id']
    input_pass = request.form['password']
    input_name = request.form['name']

    check_result = mydb.execute_query(querys.check_query, input_id)

    if len(check_result) == 0:
        mydb.execute_query(querys.signup_query, input_id, input_pass,input_name, inplace=True)
        return redirect('/')
    else:
        return redirect('signup')

@app.route('/invest')
def first():
    if 'user_info' in session:
        return render_template('invest.html')
    else:
        return redirect('/')


@app.route('/dashboard')
def dashboard():
    if 'user_info' not in session:
        return redirect('/')
    input_code = request.args['code']
    input_year = request.args['year']
    input_month = request.args['month']
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
    result = result[['Close', 'trade', 'rtn', 'acc_rtn']]
    result['ym'] = result.index.strftime('%Y-%m')
    result = pd.concat(
        [
            result.groupby('ym')[['Close', 'trade', 'acc_rtn']].max(),
            result.groupby('ym')[['rtn']].mean()
        ], axis=1
    )
    result.reset_index(inplace=True)
    result.columns = ['시간', '종가', '보유내역', '누적 수익율', '일별 수익율']

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