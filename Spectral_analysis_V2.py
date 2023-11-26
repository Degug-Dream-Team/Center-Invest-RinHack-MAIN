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
    Преобразует данные в числовой формат, необходимый для анализа.

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

def plot_transaction_amount_over_time(data, user_id):
    """
    Строит график суммы транзакций от времени для указанного пользователя.

    Parameters:
    - data (list): Список словарей, представляющих строки данных.
    - user_id (str): Идентификатор пользователя.

    Returns:
    - None
    """
    user_data = [row for row in data if row['customer'] == user_id]
    numeric_data = preprocess_data(user_data)

    if len(numeric_data) == 0:
        print(f"Для пользователя {user_id} нет данных для анализа.")
        return

    filtered_data = numeric_data[(numeric_data[:, 1] > 50) | (numeric_data[:, 1] < 0.1)]

    if len(filtered_data) == 0:
        print(f"Для пользователя {user_id} нет данных для анализа после фильтрации.")
        return

    average_amount = np.mean(filtered_data[:, 1])

    # Строим график со всеми значениями транзакций
    plt.vlines(x=numeric_data[:, 0], ymin=0, ymax=numeric_data[:, 1], color='b', label='Транзакции')
    plt.scatter(numeric_data[:, 0], numeric_data[:, 1], marker='o', color='red', label='Точки')
    plt.axhline(y=average_amount, color='green', linestyle='--', label='Среднее значение')

    plt.title(f'График суммы транзакции от времени для пользователя {user_id}')
    plt.xlabel('Время (шаги)')
    plt.ylabel('Сумма транзакции')
    plt.legend()
    plt.grid()

    for i, step in enumerate(numeric_data[:, 0]):
        plt.text(step, numeric_data[i, 1], f' {int(step)}', ha='left', va='bottom')

    plt.show()

file_path = 'sorted_transactions.csv'
transactions_data = read_csv_file(file_path)

user_id = input("Введите идентификатор пользователя для анализа: ")
plot_transaction_amount_over_time(transactions_data, user_id)
