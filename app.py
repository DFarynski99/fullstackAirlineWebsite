from flask import Flask, render_template
from main import perform_scrape  # Make sure this is the correct function to call

app = Flask(__name__)


@app.route('/')
def index():
    return "Welcome to my Flight Scraper!"


@app.route('/search', methods=['GET'])
def search():
    # Call perform_scrape to get the data
    results = perform_scrape()
    # Render the template with the results
    return render_template('search_results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
