import csv
import numpy as np
import matplotlib.pyplot as plt

def read_csv_file(file_path):
    """
    Читает данные из CSV-файла с разделителем '|' и возвращает их в виде списка словарей.

    Parameters:
    - file_path (str): Путь к CSV-файлу.

    Returns:
    - data (list): Список словарей, представляющих строки CSV-файла.
    """
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            data.append(row)
    return data

def preprocess_data(data):
    """
    Преобразует данные в числовой формат, необходимый для алгоритма кластеризации.

    Parameters:
    - data (list): Список словарей, представляющих строки данных.

    Returns:
    - numeric_data (numpy.ndarray): 2D массив числовых данных.
    """
    numeric_data = []
    for row in data:
        numeric_row = [float(row['step']), float(row['amount'])]
        numeric_data.append(numeric_row)
    return np.array(numeric_data)

def kmeans(X, k=2, num_iterations=100):
    """
    Реализует алгоритм KMeans для кластеризации данных.

    Parameters:
    - X (numpy.ndarray): 2D массив данных.
    - k (int): Количество кластеров.
    - num_iterations (int): Количество итераций алгоритма.

    Returns:
    - labels (numpy.ndarray): Метки кластеров для каждой точки данных.
    - centroids (numpy.ndarray): Координаты центроидов кластеров.
    """
    centroids = X[np.random.choice(len(X), k, replace=False)]

    for _ in range(num_iterations):

        distances = np.linalg.norm(X[:, np.newaxis, :] - centroids, axis=2)

        labels = np.argmin(distances, axis=1)

        centroids = np.array([X[labels == j].mean(axis=0) for j in range(k)])

    return labels, centroids

def plot_clusters(X, labels, centroids, user_id):
    """
    Визуализирует результаты кластеризации и подписывает точки данных.

    Parameters:
    - X (numpy.ndarray): 2D массив данных.
    - labels (numpy.ndarray): Метки кластеров для каждой точки данных.
    - centroids (numpy.ndarray): Координаты центроидов кластеров.
    - user_id (str): Идентификатор пользователя.
    """
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.5, label='Транзакции')
    plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200, label='Центроиды')
    plt.title(f'Кластеризация транзакций методом KMeans для пользователя {user_id}')
    plt.xlabel('Шаг (Step)')
    plt.ylabel('Сумма (Amount)')
    plt.legend()
    plt.grid()

    for i, step in enumerate(X[:, 0]):
        plt.annotate(f"{step:.2f}", (X[i, 0], X[i, 1]), textcoords="offset points", xytext=(0, 5), ha='center')

    plt.show()

def detect_suspicious_transactions(data, user_id, num_clusters=2):
    """
    Анализирует транзакции пользователя с использованием алгоритма KMeans и визуализирует результаты.

    Parameters:
    - data (list): Список словарей, представляющих строки данных.
    - user_id (str): Идентификатор пользователя.
    - num_clusters (int): Количество кластеров для KMeans.

    Returns:
    - suspicious_transactions (list): Список подозрительных транзакций.
    """
    user_data = [row for row in data if row['customer'] == user_id]

    numeric_data = preprocess_data(user_data)

    if len(numeric_data) == 0:
        print(f"Для пользователя {user_id} нет данных для анализа.")
        return []

    labels, centroids = kmeans(numeric_data, k=num_clusters)

    plot_clusters(numeric_data, labels, centroids, user_id)

    suspicious_transactions = [user_data[i] for i, cluster in enumerate(labels) if cluster == 1]
    return suspicious_transactions


file_path = 'sorted_transactions.csv'
transactions_data = read_csv_file(file_path)

user_id = input("Введите идентификатор пользователя для анализа: ")
suspicious_transactions = detect_suspicious_transactions(transactions_data, user_id)
