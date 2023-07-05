import requests
from flask import Flask, request, jsonify
import concurrent.futures

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            numbers = data.get('numbers', [])
            return numbers
    except requests.exceptions.RequestException:
        pass
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    numbers = []
    print(1)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_numbers, url) for url in urls]

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                numbers.extend(result)

    numbers = sorted(list(set(numbers)))

    return jsonify(numbers=numbers)

if __name__ == '__main__':
    app.run(port=8008)
