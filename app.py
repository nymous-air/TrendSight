from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', app_name="TrendSight")

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return "No file uploaded"

    # Read CSV or Excel automatically
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    # Convert data preview to HTML
    table_html = df.head(20).to_html(classes="table table-striped table-bordered")

    # ---- BASIC CALCULATIONS ----
    numeric_df = df.select_dtypes(include='number')

    summary_stats = numeric_df.describe().round(2).to_html(classes="table table-hover table-dark")
    column_totals = numeric_df.sum().round(2).to_frame("Total").to_html(classes="table table-bordered")
    column_means = numeric_df.mean().round(2).to_frame("Mean").to_html(classes="table table-bordered")

    # ---- AI INSIGHTS DISABLED MESSAGE ----
    ai_message = (
        "AI insights are temporarily unavailable because no OpenAI/OpenRouter "
        "credits are currently active. Upload your file normally — calculations "
        "will still work."
    )

    return render_template(
        'results.html',
        app_name="TrendSight",
        table=table_html,
        summary_stats=summary_stats,
        totals=column_totals,
        means=column_means,
        ai_message=ai_message,
    )

if __name__ == "__main__":
    app.run(debug=True)

