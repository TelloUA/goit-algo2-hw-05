import json
import timeit
from HyperLogLog import HyperLogLog
# from datasketch import HyperLogLog


def read_log_file():
    file_path = "lms-stage-access.log"
    logs = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                log_entry = json.loads(line.strip())
                logs.append(log_entry)
            except json.JSONDecodeError as e:
                print(f"Помилка парсингу JSON: {e}")

    return logs 

logs = read_log_file()

def accurate_counting():
    unique_ips = set()
    for log in logs:
        ip = log.get('remote_addr')
        unique_ips.add(ip)

    return len(unique_ips)

def hll_counting():
    hll = HyperLogLog(p=14)    
    for log in logs:
        ip = log.get('remote_addr')
        hll.add(ip)

        # hll.update(ip.encode('utf-8'))
    return hll.count()

print('Результати порівняння:')
print('-----------------------------')
print('Точний підрахунок')
execution_time = timeit.timeit("accurate_counting()", globals=globals(), number=100)
print(f"Час виконання (сек): {execution_time:.6f}")
print(f"Унікальні елементи: {accurate_counting()}")
print('-----------------------------')
print('HyperLogLog')
execution_time = timeit.timeit("hll_counting()", globals=globals(), number=100)
print(f"Час виконання (сек): {execution_time:.6f}")
print(f"Унікальні елементи: {hll_counting():.6f}")

# висновки у readme