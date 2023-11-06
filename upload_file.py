import requests

url = 'http://127.0.0.1:8000/users/register/true/'

# 파일 경로
file_path = 'C:/Users/amu66/OneDrive/바탕 화면/아이유 드코.pdf'

# 다른 필드 데이터
data = {
    'username': 'user122223',
    'realname': 'John Doe',
    'phone': '123-456-7890',
    'license': '12345',
    'category': '요식업',
    'location': '서울특별시',
    'is_ceo': True,
}

# 파일과 데이터를 함께 전송
files = {'document': open(file_path, 'rb')}
response = requests.post(url, files=files, data=data)
