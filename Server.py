import socket
import subprocess
import threading

def run_method(user_id, method):
    """
    Выполняет запуск соответствующего метода анализа данных.

    Parameters:
    - user_id (str): Идентификатор пользователя.
    - method (str): Выбранный метод анализа данных.

    Returns:
    - None
    """
    try:

        if method == "SVM":
            subprocess.Popen(["python", "SVM.py", user_id], shell=True)
        elif method == "KMeans":
            subprocess.Popen(["python", "KMeans.py", user_id], shell=True)
        elif method == "Spectral_analysis_V2":
            subprocess.Popen(["python", "Spectral_analysis_V2.py", user_id], shell=True)
        else:
            print("Неизвестный метод.")
    except Exception as e:
        print(f"Ошибка выполнения метода: {str(e)}")

def handle_client(client_socket, addr):
    """
    Обрабатывает подключение от клиента.
    Принимает данные от клиента, инициирует выполнение соответствующего метода и отправляет результат клиенту.

    Parameters:
    - client_socket (socket.socket): Сокет клиента.
    - addr (tuple): Кортеж с IP-адресом и портом клиента.

    Returns:
    - None
    """
    data = client_socket.recv(4096).decode("utf-8")
    print(f"Принято подключение от {addr}")
    print(f"Получены данные: {data}")

    try:
        user_id, method = data.split(",")
        run_method(user_id, method)
        client_socket.send("Метод успешно выполнен".encode("utf-8"))
    except Exception as e:
        print(f"Ошибка выполнения метода: {str(e)}")
        client_socket.send("Ошибка выполнения метода".encode("utf-8"))

    client_socket.close()

def start_server():
    """
    Запускает сервер для обработки запросов от клиентов.
    Создает сокет сервера и прослушивает указанный порт.
    Принимает подключение от клиента и создает новый поток для обработки запроса.

    Returns:
    - None
    """
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Сервер слушает на порту {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
