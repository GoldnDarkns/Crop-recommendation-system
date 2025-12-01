# save as test_batch_client.py
import requests

url = "http://127.0.0.1:8000/batch_predict"

files = {
    "file": ("sample_batch.csv", open("sample_batch.csv", "rb"), "text/csv")
}

response = requests.post(url, files=files)
print("Status:", response.status_code)
print("Response:", response.json())
