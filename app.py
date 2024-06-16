from flask import Flask, render_template, request
import pandas as pd
from prophet import Prophet

app = Flask(__name__)

# Load the dataset
data = pd.read_csv('dam_data.csv')

# Rename the columns
data = data.rename(columns={'Timestamp': 'ds', 'Water_Level(m)': 'y'})

# Convert the 'ds' column to datetime
data['ds'] = pd.to_datetime(data['ds'])

# Create a Prophet model instance
model = Prophet()

# Fit the model to the data
model.fit(data[['ds', 'y']])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        forecast_hours = int(request.form['forecast_hours'])
        future = model.make_future_dataframe(periods=forecast_hours, freq='H')
        forecast = model.predict(future)
        forecast_data = forecast[['ds', 'yhat']].tail(forecast_hours).to_html(index=False)
        print(forecast_data)
        # return forecast_data
        return render_template('forecast.html', forecast_data=forecast_data, days = forecast_hours)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)