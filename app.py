import os
from flask import Flask, render_template, request
from main import jetstarScrape  # Import your scraping functions
from main import qantasScrape  # Import your scraping functions
from main import rexScrape
from main import virginScrape

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    results = None  # Initialize an empty variable for results

    if request.method == 'POST':
        action = request.form['action']
        if action == 'searchFlights':

            functionality = {
                'airline': request.form.get('airline'),
                'departureAirport': request.form.get('departureAirport'),
                'arrivalAirport': request.form.get('arrivalAirport'),
                'departureDate': request.form.get('departureDate'),
                'returnDate': request.form.get('returnDate', None)  # Optional, defaults to None if not present
            }

            # Determine if this is a one-way or return flight based on whether a return date is provided
            flight_type = 'return' if functionality['returnDate'] else 'one-way'

            if functionality['airline'] == 'jetstar':
                # Pass the flight type to your scraping function
                message = jetstarScrape(functionality, flight_type)

            elif functionality['airline'] == 'qantas':
                message = qantasScrape(functionality, flight_type)

            elif functionality['airline'] == 'regionalExpress':
                results = virginScrape(functionality, flight_type)

            elif functionality['airline'] == 'virgin':
                results = virginScrape(functionality, flight_type)



    return render_template('index.html', results=results)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(host='0.0.0.0', port=port, debug=True)
