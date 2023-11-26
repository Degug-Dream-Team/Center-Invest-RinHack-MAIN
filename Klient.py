import socket

def send_data_to_server(data_to_send):
    """
    Отправляет данные на сервер и выводит результат выполнения метода.

    Parameters:
    - data_to_send (str): Данные для отправки на сервер в формате "user_id,method".

    Returns:
    - None
    """
    host = "127.0.0.1"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(data_to_send.encode("utf-8"))
    result = client_socket.recv(4096).decode("utf-8")

    print(f"Результат выполнения метода: {result}")

    client_socket.close()

if __name__ == "__main__":
    user_id = input("Введите идентификатор пользователя: ")
    print("Выберите метод:")
    print("1. SVM")
    print("2. KMeans")
    print("3. Spectral_analysis_V2")

    selected_method = int(input("Введите номер выбранного метода: "))

    method_dict = {1: "SVM", 2: "KMeans", 3: "Spectral_analysis_V2"}
    method = method_dict.get(selected_method)

    if method:
        data_to_send = f"{user_id},{method}"
        send_data_to_server(data_to_send)
    else:
        print("Некорректный выбор метода.")
