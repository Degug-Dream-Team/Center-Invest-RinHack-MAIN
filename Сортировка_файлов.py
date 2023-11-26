import csv

def sort_and_write_to_new_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        header = next(reader)
        data = list(reader)

    sorted_data = sorted(data, key=lambda x: x[2].strip("'"))

    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(header)
        writer.writerows(sorted_data)

input_file_path = 'fraud_dataset.csv'
output_file_path = 'sorted_transactions.csv'
sort_and_write_to_new_file(input_file_path, output_file_path)
