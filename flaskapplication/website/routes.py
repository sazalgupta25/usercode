from flask import Blueprint, render_template
from flask import request
from .models import Result
import openai

routes = Blueprint('routes', __name__)
openai.api_key = 'sk-mJMiKCRTmkwfElTz5m9mUE9GeIDH7hkUIJasg6dK-eT3BlbkFJ79wRCWCd-aPgELp_t4Htr5IyRp1Z2jp050I-JzJeQA'
completion = openai.Completion()

historyData = []
@routes.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        query = request.args.get('query')
        if query == "" or query is None:
            return render_template('response_view.html')
        response = ask(query)
        dataList = []
        queryMessage = Result(time="This Time", messagetype="other-message float-right", message=query)
        responseMessage = Result(time="This Time", messagetype="my-message", message=response)
        dataList.append(queryMessage)
        dataList.append(responseMessage)
        historyData.append(queryMessage)
        historyData.append(responseMessage)
        return render_template('response_view.html', results=dataList)
    else:
        return render_template('history.html', results=historyData) 

def ask(question, chat_log=None):
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = completion.create(
        prompt=prompt, engine="gpt-3.5-turbo", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer