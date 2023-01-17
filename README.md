# Compass Viewer
I was too lazy to click on each item for the Compass website so I made this. Pretty straightforward, just download your transaction history from Compass and upload and it will show HTML with location history and time of all transactions.

## Todo
- [ ] Merge into a Single Map & Heatmap (https://developers.google.com/maps/documentation/javascript/examples/layer-heatmap)
- [ ] Caching System for Bus Routes
- [ ] Bus Route History
- [ ] CSV Export of Data


## Installation

### Requirements
1. Install Python 3.10+
2. (Optional) Create a virtual environment with `python -m venv venv` (or `python3` if you have multiple versions of Python installed
3. Install the requirements with `pip install -r requirements.txt`

### Running
For **production**, you can deploy with either Gunicorn or Waitress with the following commands:
- `gunicorn -b 0.0.0.:5000 app:app`
- `waitress-serve --port=5000 app:app`

For **development**, you can use Flask's built-in development server with `flask run` in the current folder or `python app.py`