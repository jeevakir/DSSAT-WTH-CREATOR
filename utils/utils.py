import os
def get_csv_files(directory):
    csv_files = []
    for file in os.listdir(directory):
        if file.lower().endswith('.csv'):
            csv_files.append(file)
    return csv_files