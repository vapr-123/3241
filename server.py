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

import socket  # Модуль для работы с сокетами
import threading  # Модуль для работы с потоками

def client_handler(conn, addr):
    # Функция для обработки взаимодействия с клиентом в отдельном потоке
    print(f"Подключен клиент {addr}")
    msg = ''
    while True:
        # Бесконечный цикл для приема данных от клиента
        data = conn.recv(1024)
        # Получаем данные размером до 1024 байт
        if not data:
            # Если данных нет, значит клиент отключился
            break
        msg = data.decode()
        # Декодируем байтовые данные в строку
        print(f"Получено сообщение от {addr}: {msg}")
        conn.send(data)
        # Отправляем данные обратно клиенту (эхо)
    print(f"Клиент {addr} отключился")
    conn.close()
    # Закрываем соединение с данным клиентом

def main():
    sock = socket.socket()
    # Создаем сокет (TCP по умолчанию)
    sock.bind(('', 9090))
    # Связываем сокет с адресом и портом. Пустая строка означает, что сервер будет принят запросы с любых сетевых интерфейсов.
    sock.listen()
    # Переводим сокет в режим прослушивания входящих подключений
    print("Сервер запущен и ожидает подключений...")
    while True:
        # Бесконечный цикл для принятия новых клиентов
        conn, addr = sock.accept()
        # Принимаем новое входящее подключение
        # conn — новый сокет для обмена данными с клиентом
        # addr — адрес клиента
        client_thread = threading.Thread(target=client_handler, args=(conn, addr))
        # Создаем новый поток для обслуживания клиента
        client_thread.start()
        # Запускаем поток

if __name__ == "__main__":
    main()