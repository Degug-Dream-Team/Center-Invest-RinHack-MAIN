import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

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
    Преобразует данные в числовой формат, необходимый для обучения SVM.

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

def train_svm(data, user_id):
    """
    Обучает модель SVM на данных пользователя и визуализирует результаты.

    Parameters:
    - data (list): Список словарей, представляющих строки данных.
    - user_id (str): Идентификатор пользователя.

    Returns:
    - svm_clf (SVC): Обученная модель SVM.
    """
    user_data = [row for row in data if row['customer'] == user_id]
    numeric_data = preprocess_data(user_data)

    if len(numeric_data) == 0:
        print(f"Для пользователя {user_id} нет данных для обучения.")
        return None

    # Разделение данных на обучающий и тестовый наборы
    X = numeric_data[:, :2]
    y = numeric_data[:, -1].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Стандартизация данных
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Создание и обучение модели SVM
    svm_clf = SVC(kernel='rbf', C=10.0, gamma='scale')
    svm_clf.fit(X_train_scaled, y_train)

    y_pred = svm_clf.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    plt.scatter(X_train[:, 0], X_train[:, 1], c='blue', alpha=0.5, label='Обучающий набор')
    plt.scatter(X_test[:, 0], X_test[:, 1], c='red', alpha=0.5, marker='x', label='Тестовый набор')

    # Создание сетки для оценки модели
    h = 0.5
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = svm_clf.predict(np.c_[xx.ravel(), yy.ravel()])

    # Отображение разделяющей гиперплоскости и полос
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap='viridis', alpha=0.3)

    for i, (step, amount) in enumerate(zip(X[:, 0], X[:, 1])):
        plt.annotate(f"{step:.0f}, {amount:.0f}", (step, amount), textcoords="offset points", xytext=(0, 5), ha='center')

    plt.title(f'График SVM для пользователя {user_id}')
    plt.xlabel('Шаг (Step)')
    plt.ylabel('Сумма (Amount)')
    plt.legend()
    plt.grid()

    plt.show()

    return svm_clf

file_path = 'sorted_transactions.csv'
transactions_data = read_csv_file(file_path)

user_id = input("Введите идентификатор пользователя для обучения SVM: ")
svm_clf = train_svm(transactions_data, user_id)
