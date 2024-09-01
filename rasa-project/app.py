from flask import Flask, redirect, url_for, request, render_template
import requests
import json

app = Flask(__name__, template_folder='./')
context_set = ""

response = [] # A list that will store the conversation

@app.route('/stories', methods = ['GET'])
def stories():
    return render_template('graph.html')  

@app.route('/', methods = ['GET'])
def index():
    response.clear()
    return render_template('index.html', val ='')

@app.route('/msg', methods=['POST'])
def msg():
    val = str(request.form['text'])
    data = json.dumps({"sender": "Rasa", "message": val})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    try:
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data=data, headers=headers)
        res.raise_for_status()

        # Log the response content for debugging
        print("Rasa response content:", res.content)

        # Parse JSON
        res_json = res.json()

        if not val or val[0] == '/':
            return render_template('index.html', val=response)
        else:
            message = ''
            response.append(val)
            for x in res_json:
                payload = list(without_keys(x, 'recipient_id').values())
                message = message + "  " + str(payload[0])
            response.append(message)
            return render_template('index.html', val=response)

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Rasa server: {e}")
        return render_template('index.html', val=response + ["Error connecting to Rasa server"])

    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        print("Response content:", res.content)
        return render_template('index.html', val=response + ["Invalid JSON response from Rasa server"])

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5006)