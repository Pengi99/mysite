from flask import Flask, request, render_template, url_for
import pandas as pd


app = Flask(__name__)

@app.route('/invest')
def invest():
    return render_template('invest.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

app.run(debug=True)