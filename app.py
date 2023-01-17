from flask import Flask, request, jsonify
import csv
import io
from util import seek_stop_id, format_datetime, lookup, get_coordinates

app = Flask(__name__)

@app.route('/api', methods=['POST', 'GET'])
def compass_api():

    data = get_coordinates('Vancouver, B.C')

    # csv_file = request.files['file']
    
    # data = []

    # raw_data = csv_file.read().decode('utf-8')
    # csv_data = csv.reader(io.StringIO(raw_data))
    # next(csv_data)

    # for row in csv_data:

    #     location = seek_stop(row[1])

    #     if location is not None:
    #         date_time = format_datetime(row[0])
            
    #         if location.isnumeric():
    #             bus_stop = lookup(location)
    #             data.append({
    #                 'type': 'bus',
    #                 'info': bus_stop,
    #                 'timestamp': date_time,
    #             })
    #         else:
    #             data.append({
    #                 'type': 'location',
    #                 'info': {
    #                     'name': location,
    #                     'coordinates': get_coordinates(location),
    #                 },
    #                 'timestamp': date_time,
    #             })
    #     else:
    #         continue

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)