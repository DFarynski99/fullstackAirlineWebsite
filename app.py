import os
from flask import Flask, render_template, request
from main import jetstarScrape  # Import your scraping functions

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    if request.method == 'POST':
        action = request.form['action']
        if action == 'searchFlights':

            options = {
                'airline': request.form.get('airline'),
                'departureAirport': request.form.get('departureAirport'),
                'arrivalAirport': request.form.get('arrivalAirport'),
                'departureDate': request.form.get('departureDate'),
                'returnDate': request.form.get('returnDate', None)  # Optional, defaults to None if not present
            }

            if options['airline'] == 'jetstar':
                message = jetstarScrape(options)

            elif options['airline'] == 'qantas':
                message = "Qantas is selected"
            elif options['airline'] == 'regionalExpress':
                message = "Regional Express is selected"
                # Add more conditions for other airlines

            elif action == 'scrapeFlights':
                message = "Scrape Flights button pressed"

    return render_template('index.html', message=message)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
