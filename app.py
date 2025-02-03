from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_armstrong(n):
    digits = [int(d) for d in str(n)]
    power = len(digits)
    return sum(d ** power for d in digits) == n

@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    number = request.args.get('number')
    
    if not number.isdigit():
        return jsonify({"number": number, "error": True}), 400

    number = int(number)
    
    # Get a fun fact from Numbers API
    response = requests.get(f"http://numbersapi.com/{number}/math")
    fun_fact = response.text if response.status_code == 200 else "No fun fact available."

    result = {
        "number": number,
        "is_prime": is_prime(number),
        "is_perfect": is_armstrong(number),
        "properties": get_properties(number),
        "digit_sum": sum(int(digit) for digit in str(number)),
        "fun_fact": fun_fact
    }

    return jsonify(result)

def get_properties(number):
    properties = []
    if is_armstrong(number):
        properties.append("armstrong")
    if number % 2 == 0:
        properties.append("even")
    else:
        properties.append("odd")
    return properties

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
