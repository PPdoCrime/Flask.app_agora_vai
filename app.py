from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Configuração do Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Nome da planilha e da aba (worksheet)
spreadsheet_name = "Resultados"
worksheet_name = "Resultados"

try:
    sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
except Exception as e:
    print(f"Erro ao acessar a planilha ou aba: {e}")

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

            row = [familiarity, escuro_vs_escuro_30, escuro_vs_escuro_40, escuro_30_vs_escuro_40, claro_vs_claro_30,
                   claro_vs_claro_40, claro_30_vs_claro_40, escuro_vs_claro_30, escuro_vs_claro_40, escuro_vs_claro]
            sheet.append_row(row)

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
    data = sheet.get_all_records()
    return render_template('results.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
