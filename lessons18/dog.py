from flask import Flask, jsonify
import requests
import random

app = Flask(__name__)

DOG_API_URL = 'https://dogapi.dog/api/v2/breeds'

@app.route('/dog', methods=['GET'])
def get_random_breed():
    try:
        response = requests.get(DOG_API_URL)
        response.raise_for_status()  
        data = response.json()

        breeds = data.get('data', [])
        if not breeds:
            return jsonify({'error': 'No breeds found'}), 404

        random_breed = random.choice(breeds)
        breed_name = random_breed['attributes']['name']
        description = random_breed['attributes'].get('description', 'No description available.')

        return jsonify({
            'breed': breed_name,
            'description': description
        })

    except requests.RequestException as e:
        return jsonify({'error': 'Failed to fetch breeds', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
