from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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

        results = [
            familiarity, escuro_vs_escuro_30, escuro_vs_escuro_40, escuro_30_vs_escuro_40,
            claro_vs_claro_30, claro_vs_claro_40, claro_30_vs_claro_40, 
            escuro_vs_claro_30, escuro_vs_claro_40, escuro_vs_claro
        ]

        # Save results to a CSV file
        with open('results.csv', 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(results)

        return redirect(url_for('thank_you'))

    return render_template('index.html')

@app.route('/thank_you')
def thank_you():
    return "<h1>Thank you for your submission!</h1>"

@app.route('/results')
def results():
    data = []
    if os.path.exists('results.csv'):
        with open('results.csv', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            headers = next(reader, None)  # Skip header if exists
            for row in reader:
                data.append(row)
    return render_template('results.html', data=data)

if __name__ == '__main__':
    # Create results.csv if it doesn't exist
    if not os.path.exists('results.csv'):
        with open('results.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([
                'Familiarity', 'Escuro_vs_Escuro_30', 'Escuro_vs_Escuro_40', 'Escuro_30_vs_Escuro_40',
                'Claro_vs_Claro_30', 'Claro_vs_Claro_40', 'Claro_30_vs_Claro_40', 
                'Escuro_vs_Claro_30', 'Escuro_vs_Claro_40', 'Escuro_vs_Claro'
            ])
    app.run(debug=True)
