from flask import Flask, request, render_template, url_for
import pandas as pd


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

    return render_template('dashboard.html')

app.run(debug=True)