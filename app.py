from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    familiarity = db.Column(db.String(50))
    escuro_vs_escuro_30 = db.Column(db.String(50))
    escuro_vs_escuro_40 = db.Column(db.String(50))
    escuro_30_vs_escuro_40 = db.Column(db.String(50))
    claro_vs_claro_30 = db.Column(db.String(50))
    claro_vs_claro_40 = db.Column(db.String(50))
    claro_30_vs_claro_40 = db.Column(db.String(50))
    escuro_vs_claro_30 = db.Column(db.String(50))
    escuro_vs_claro_40 = db.Column(db.String(50))
    escuro_vs_claro = db.Column(db.String(50))

@app.before_first_request
def create_tables():
    db.create_all()

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

            result = Result(
                familiarity=familiarity,
                escuro_vs_escuro_30=escuro_vs_escuro_30,
                escuro_vs_escuro_40=escuro_vs_escuro_40,
                escuro_30_vs_escuro_40=escuro_30_vs_escuro_40,
                claro_vs_claro_30=claro_vs_claro_30,
                claro_vs_claro_40=claro_vs_claro_40,
                claro_30_vs_claro_40=claro_30_vs_claro_40,
                escuro_vs_claro_30=escuro_vs_claro_30,
                escuro_vs_claro_40=escuro_vs_claro_40,
                escuro_vs_claro=escuro_vs_claro
            )
            db.session.add(result)
            db.session.commit()

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
    data = Result.query.all()
    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
