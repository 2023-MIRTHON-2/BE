import requests
import json
import base64

# 윈도우 파일 경로
file_path = r"C:\Users\amu66\OneDrive\바탕 화면\기획서_및_와이어프레임.pdf"

# 파일을 읽고 base64로 인코딩합니다.
with open(file_path, 'rb') as f:
    document_encoded = base64.b64encode(f.read()).decode('utf-8')

    # print(document_encoded)

# 테스트할 데이터를 준비합니다.
data = {
    "username": "test2goohaeseung",
    "password1": "ghsghs1111",
    "password2": "ghsghs1111",
    "realname": "홍길동",
    "phone": "010-1234-5678",
    "license": "123-45-67890",
    "document": document_encoded,
    "category": "요식업",
    "location": "서울",
}

# 요청을 보냅니다.
response = requests.post('http://127.0.0.1:8000/users/register/true/', json=data)

# 응답을 출력합니다.
print(response.status_code)
print(response.text)
