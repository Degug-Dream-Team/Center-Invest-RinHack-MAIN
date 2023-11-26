import csv

def sort_and_write_to_new_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        header = next(reader)
        data = list(reader)

    # Sort data by the "fraud" column (assuming it is at index 10)
    sorted_data = sorted(data, key=lambda x: int(x[10].strip("'")))

    # Filter only rows with "fraud" equal to 1
    filtered_data = [row for row in sorted_data if int(row[10].strip("'")) == 1]

    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='|')
        writer.writerow(header)
        writer.writerows(filtered_data)

input_file_path = 'sorted_transactions.csv'
output_file_path = 'sorted_fraud.cvs'
sort_and_write_to_new_file(input_file_path, output_file_path)
