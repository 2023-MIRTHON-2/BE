import requests
from baloyeogi.settings import API_KEY

def check_license_number(license_number):
    api_url = f'https://bizno.net/api/fapi?key={API_KEY}&gb=1&q={license_number}&type=json&pagecnt=1'
    try:

        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])
        if items:
            company_data = items[0]
            company_number = company_data.get('bno', '')
            if company_data.get('company', ''):
                return company_number  # 유효한 사업자 등록 번호일 경우 company_number 반환
            else:
                return None  # 유효하지 않은 경우 None 반환
        else:
            return None
    except requests.exceptions.RequestException as e:
        raise e  # 오류 발생 시 예외 처리를 위해 예외를 다시 발생시킵니다.
