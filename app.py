# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from model.predictor import predict_diabetes
from model.database import create_table, insert_prediction, get_all_predictions, clear_history
from markupsafe import Markup  # for formatted HTML in model insights

app = Flask(__name__)
app.secret_key = 'afiya08'  # Needed for flash messages

# Initialize the database table once
create_table()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect form data
        input_data = [
            float(request.form['pregnancies']),
            float(request.form['glucose']),
            float(request.form['blood_pressure']),
            float(request.form['skin_thickness']),
            float(request.form['insulin']),
            float(request.form['bmi']),
            float(request.form['dpf']),
            float(request.form['age']),
        ]
    except (ValueError, KeyError):
        flash("Please enter valid numeric values for all fields.")
        return redirect(url_for('index'))

    # Make prediction (now returns 4 values)
    result, prob, band, advice = predict_diabetes(input_data)

    # Save to database with probability and risk level
    insert_prediction(input_data, result, prob, band)

    return render_template('result.html',
                           input_data=input_data,
                           result=result,
                           prob=prob,
                           band=band,
                           advice=advice)

@app.route('/history')
def history():
    predictions = get_all_predictions()
    return render_template('history.html', predictions=predictions)

@app.route('/clear', methods=['POST'])
def clear():
    clear_history()
    flash("Prediction history cleared.")
    return redirect(url_for('history'))

@app.route('/report')
def report():
    raw_insights = [
        "Overall accuracy is 72 %, which is respectable for a simple Decision Tree on this dataset.",
        "Recall for the at‑risk class is <strong>0.80</strong>, meaning the model misses relatively few true cases — important in healthcare.",
        "Precision for the at‑risk class is 0.69; roughly 7 of 10 flagged users are indeed at risk, so some false alarms remain.",
        "Class distribution is balanced (124 vs 126 samples), reducing bias toward either class.",
        "Macro and weighted F1 scores (~0.71‑0.72) show consistent performance across classes."
    ]
    # Convert bold tags into safe HTML
    insights = [Markup(note) for note in raw_insights]
    return render_template('report.html', insights=insights)

#if __name__ == '__main__':
 #   app.run(debug=True)     # This is for local run

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

