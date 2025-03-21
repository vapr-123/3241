import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(0)
conn, addr = sock.accept()
print(addr)

msg = ''

while True:
	data = conn.recv(1024)
	if not data:
		break
	msg += data.decode()
	conn.send(data)

print(msg)

conn.close()

# Импортируем необходимые модули
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # Для прогресс-бара

# Запрашиваем у пользователя имя хоста или IP-адрес для сканирования
host = input("Пожалуйста, введите имя хоста или IP-адрес для сканирования: ")

# Пытаемся разрешить имя хоста в IP-адрес
try:
    host_ip = socket.gethostbyname(host)
except socket.gaierror:
    print(f"Имя хоста '{host}' не может быть разрешено. Выход.")
    sys.exit()

# Определяем диапазон портов для сканирования
start_port = 1      # Начальный номер порта
end_port = 1024     # Конечный номер порта
# Примечание: измените end_port на 65535, чтобы сканировать все возможные порты

# Информируем пользователя о начале сканирования
print(f"Начинаем сканирование хоста {host} ({host_ip}) с порта {start_port} до {end_port}")

# Определяем функцию, которая будет сканировать один порт
def scan_port(port):
    """
    Пытается подключиться к заданному хосту на указанном порту.
    Возвращает номер порта, если он открыт.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # Таймаут в секундах
    result = sock.connect_ex((host_ip, port))
    sock.close()
    if result == 0:
        # Если попытка подключения возвращает 0, порт открыт
        return port
    else:
        # Порт закрыт или фильтруется
        return None

# Список для хранения открытых портов
open_ports = []

try:
    # Используем ThreadPoolExecutor для управления пулом потоков
    with ThreadPoolExecutor(max_workers=100) as executor:
        # Словарь для отслеживания соответствия future и порта
        future_to_port = {executor.submit(scan_port, port): port for port in range(start_port, end_port + 1)}
        
        # Создаем прогресс-бар
        with tqdm(total=end_port - start_port + 1, desc="Сканирование портов") as pbar:
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                    if result is not None:
                        open_ports.append(result)
                except KeyboardInterrupt:
                    print("\nСканирование прервано пользователем.")
                    sys.exit()
                except Exception as exc:
                    print(f"Порт {port} вызвал исключение: {exc}")
                finally:
                    pbar.update(1)
except KeyboardInterrupt:
    print("\nСканирование прервано пользователем.")
    sys.exit()
except socket.error as e:
    print(f"Ошибка сокета: {e}")
    sys.exit()

# После сканирования выводим открытые порты по порядку
open_ports.sort()
if open_ports:
    print("Открытые порты:")
    for port in open_ports:
        print(f"Порт {port} открыт")
else:
    print("В указанном диапазоне не найдено открытых портов.")

# Информируем пользователя о завершении сканирования
print("Сканирование завершено.")