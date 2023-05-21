import time
import os

a = int(os.getenv('TEST', 1))
print("비동기 처리 테스트 코드")
print(f"{a} 초 수행")
time.sleep(a)