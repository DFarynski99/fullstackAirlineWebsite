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
            airline = request.form.get('airline')
            if airline == 'jetstar':
                message = "Jetstar is selected"
                jetstarScrape()
                message = "Jetstar is selected"
            elif airline == 'qantas':
                message = "Qantas is selected"
            elif airline == 'regionalExpress':
                message = "Regional Express is selected"
            # Add actions for 'searchFlights'


        elif action == 'scrapeFlights':
            message = "Scrape Flights button pressed"
    return render_template('index.html', message=message)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
