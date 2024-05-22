from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

# Configuração do MongoDB
mongodb_uri = os.getenv('mongodb+srv://ppsramalho1505:NvJdoBqdA5L5VKlu@cluster0.hicua8w.mongodb.net/')
client = MongoClient(mongodb_uri)
db = client.get_database('results_db')
results_collection = db.get_collection('results')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            familiarity = request.form['familiarity']
            escuro_vs_escuro_30 = request.form['escuro_vs_escuro_30']
            escuro_vs_escuro_40 = request.form['escuro_vs_escuro_40']
            escuro_30_vs_escuro_40 = request.form['escuro_30_vs_escuro_40']
            claro_vs_claro_30 = request.form['claro_vs_claro_30']
            claro_vs_claro_40 = request.form['claro_vs_claro_40']
            claro_30_vs_claro_40 = request.form['claro_30_vs_claro_40']
            escuro_vs_claro_30 = request.form['escuro_vs_claro_30']
            escuro_vs_claro_40 = request.form['escuro_vs_claro_40']
            escuro_vs_claro = request.form['escuro_vs_claro']

            result = {
                'familiarity': familiarity,
                'escuro_vs_escuro_30': escuro_vs_escuro_30,
                'escuro_vs_escuro_40': escuro_vs_escuro_40,
                'escuro_30_vs_escuro_40': escuro_30_vs_escuro_40,
                'claro_vs_claro_30': claro_vs_claro_30,
                'claro_vs_claro_40': claro_vs_claro_40,
                'claro_30_vs_claro_40': claro_30_vs_claro_40,
                'escuro_vs_claro_30': escuro_vs_claro_30,
                'escuro_vs_claro_40': escuro_vs_claro_40,
                'escuro_vs_claro': escuro_vs_claro
            }
            results_collection.insert_one(result)

            return redirect(url_for('thank_you'))
        except Exception as e:
            app.logger.error(f"Error: {e}")
            return "There was an error processing your request."

    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return "<h1>Thank you for your submission!</h1>"

@app.route('/results')
def results():
    data = results_collection.find()
    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
