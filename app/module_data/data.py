from datetime import date, datetime
import json
from io import StringIO
import boto3
import pandas as pd
from botocore.exceptions import ClientError

from app.utils import generate_file_path


def get_s3_file_content(bucket_name, file_key):
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        file_content = obj['Body'].read().decode('utf-8')
        return file_content
    except Exception as e:
        return None


def get_data():
    json_data = get_s3_file_content("xideralcinedata","cinema-pos-1737647739.json")
    json_string = json_data.replace("\n", "").replace("\\"," ")
    data = json.loads(json_string)
    return data


def get_data_json():
    json_data = get_s3_file_content("cinexideralposjoan-analisis","data_revision/cinema_pos_processed_info.json")
    json_string = json_data.replace("\n", "").replace("\\"," ")
    data = json.loads(json_string)
    return data


def get_data_csv(year: int, month: int, day: int):
    csv_content = get_s3_file_content("cinexideralposjoan-analisis", generate_file_path(year, month, day))

    if csv_content is None:
        return "No content"
    csv_buffer = StringIO()
    csv_buffer.write(csv_content)
    csv_buffer.seek(0)
    try:
        df = pd.read_csv(csv_buffer, sep=",")
        return df.to_json(orient="records")

    except Exception as e:
        return f"parse error: {str(e)}"
    # df = pd.read_csv(csv_buffer, sep=",")
    # # json_string = json_data.replace("\n", "").replace("\\"," ")
    # # data = json.loads(json_string)
    # return str(df.head(2))