from datetime import date

def generate_file_path(year: int, month: int, day: int) -> str:
    file_path = f"data_revision/{year}/{month}/{day}/pos_data_processed.csv"
    return file_path