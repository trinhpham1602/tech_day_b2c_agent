import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/posts"

def get_b2c_log(payload: dict):
  df = pd.read_json("src/service/tools/log_result.json")
  return df.to_dict()
  # return response.json()
