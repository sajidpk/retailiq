"""
RetailIQ — simple Flask backend
Serves the dashboard and exposes /api/skus from data/skus.csv
Run:  pip install flask
      python server.py
Open: http://localhost:5000
"""

import csv
import os
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)
BASE = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE, 'data', 'skus.csv')


def read_skus():
    skus = []
    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            sku = {
                'id':       row['id'],
                'name':     row['name'],
                'cat':      row['cat'],
                'supplier': row['supplier'],
                'lead':     row['lead'],
                'stock':    int(row['stock']),
                'safety':   int(row['safety']),
                'rop':      int(row['rop']),
                'forecast': int(row['forecast']),
                'status':   row['status'],
                'trend':    float(row['trend']),
                'dos':      float(row['dos']),
                'risk':     row['risk'],
                'conf':     int(row['conf']),
            }
            if row.get('perishable', '').lower() == 'true':
                sku['perishable'] = True
                sku['shelfLife']  = int(row['shelfLife'])
                sku['dte']        = int(row['dte'])
                sku['sarValue']   = int(row['sarValue'])
            skus.append(sku)
    return skus


@app.route('/')
def index():
    return send_from_directory(BASE, 'inventory-forecast.html')


@app.route('/api/skus')
def get_skus():
    try:
        return jsonify(read_skus())
    except FileNotFoundError:
        return jsonify({'error': f'CSV not found: {CSV_PATH}'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/skus/reload')
def reload_skus():
    """Force re-read of CSV — useful during a demo to show live updates."""
    try:
        data = read_skus()
        return jsonify({'reloaded': True, 'count': len(data), 'skus': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print(f'\n  RetailIQ backend  →  http://localhost:5000\n')
    app.run(debug=True, port=5000)
