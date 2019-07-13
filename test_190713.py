from flask import Flask, render_template, request
import requests
from decouple import config

app = Flask(__name__)

api_url = 'https://api.telegram.org'
token = config('TOKEN')
admin_id = config('ADMIN_ID')
secret_url = config('SECRET_URL')
naver_client_id = config('NAVER_CLIENT_ID')
naver_client_secret = config('NAVER_CLIENT_SECRET')

commands = [
    '/번역 <키워드>',
    '/미세먼지',
]
no_err = '존재하지 않는 명령어입니다'

@app.route(f'/{secret_url}', methods=['POST'])
def telegram():
# print(request.get_json())  # 요청받아옴
    req = request.get_json()
    user = req['message']['from']['id']  # 유저의 chat id
    message = req['message']['text']  # 유저의 입력메시지
    # if message == 'admin':
    #     res = '안녕하세요 관리자님 :)'
    # else:
    #     res = '하이 손님 '
    keyword = '띵작'

    if message[0] == '/':
        if ' ' in message:  # 띄어 쓰기 이후에 추ㅏ 인풋있음
            words = message.split(' ')
            if words[0] == '/번역':
                headers = {
                    'X-Naver-Client-Id': naver_client_id,
                    'X-Naver-Client-Secret': naver_client_secret,
                }
                data = {
                    'source': 'ko',
                    'target': 'en',
                    'text': words[1],
                }
                res = requests.post(
                    'https://openapi.naver.com/v1/papago/n2mt',
                    data=data,
                    headers=headers
                )
                result = res.json()['message']['result']['translatedText']  # 번역결과
                pass  # 번역작업 words[1]의 값으로 사용

            else:
                result = no_err
        else:  # 띄어쓰기 없음
            if message == '/미세먼지':
                pass
            else:
                result = no_err
            if message =='/주식':
                pass
            else:
                result =no_err
            
    else:
        result = commands

    URL = f'{api_url}/bot{token}/sendMessage?chat_id={user}&text={result} :)'
    requests.get(URL)
    return ('success', 200)  # 200 안써놓으면 계속보냄



if __name__ == '__main__':
    app.run(debug=False, port=80)
