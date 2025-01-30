import os
import json
import datetime
 
import boto3
import pandas as pd
from datetime import datetime
from io import StringIO
 
s3 = boto3.client('s3')
target_bucket_name = "cinexideralposjoan-analisis"
today = datetime.today()
 
def lambda_handler(event, context):
    try:      
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        file_key = event['Records'][0]['s3']['object']['key']
        # bucket_name = "cinexideralposjoan"
        # file_key = "cinema-pos-1737648439.json"
 
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        
        json_data = response["Body"].read().decode("utf-8")
        data = json.loads(json_data)
        df = pd.json_normalize(data)

        df = df.fillna(0)

        df['dateTime'] = pd.to_datetime(df['dateTime'])
        df['anio'] = df['dateTime'].dt.year 
        df['mes'] = df['dateTime'].dt.month 
        df['dia'] = df['dateTime'].dt.day 
        df['hora'] = df['dateTime'].dt.hour 
        df['minuto'] = df['dateTime'].dt.minute

        df['sortdate'] = df['anio'].astype(str) + "/" + df['mes'].astype(str) + "/" + df['dia'].astype(str)
        df = df.drop(columns=["dateTime"])  

        grouped = df.sort_values(by="sortdate").groupby("sortdate")

        for sortdate, group in grouped:
            timefolder = sortdate + "/"
           
            filename = "data_revision/" + timefolder + "pos_data_processed.csv"
            # group_data = group.to_dict(orient='records')

            target_file_content = get_target_file_content(filename)
       
            if target_file_content is not None:
                csv_dataframe = pd.concat([target_file_content, group], ignore_index=True)
            else:
                csv_dataframe = group
        
            csv_buffer = StringIO()
            csv_dataframe.to_csv(csv_buffer, index=False, header=True)
    
            s3.put_object(Bucket=target_bucket_name, Key=filename, Body=csv_buffer.getvalue())

        return {
            'statusCode': 200,
            'body': "exito"
        }

    except Exception as e:
        print(f"Error durante la ejecución: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)})
        }

def get_target_file_content(filename: str):
    try:
        response = s3.get_object(Bucket=target_bucket_name, Key=filename)
        data = response["Body"].read().decode("utf-8")
        return pd.read_csv(StringIO(data))
    except Exception as e: #Should be NoSuchKey
        print(f"No target file {filename} in {target_bucket_name}: {e}")
        return None