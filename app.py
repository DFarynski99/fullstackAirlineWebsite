from flask import Flask, render_template, request
from main import perform_scrape
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    if request.method == 'POST':
        # Perform the scrape when the form is submitted
        results = perform_scrape()
        # Render index.html with results, which could be passed back to the same page
    return render_template('index.html', results=results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
