import azure.functions as func
import requests
from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    webpage_url = "https://www.publicbankgroup.com/investor-relations/annual-reports/2022-annual-report/"
    response = requests.get(webpage_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=bdaa7009;AccountKey=en5DvEVHxnBvyKF97Ho7BO2nXyonV66bMY+5l25hneHVUT8QQBvRzuUnL4xnY8QovyIv1NY0H4tW+ASt+1LktA==;EndpointSuffix=core.windows.net")
    container_client = blob_service_client.get_container_client("publicbank")

    for link in soup.find_all('a'):
        if link.get('href').endswith('.pdf'):
            pdf_url = link.get('href')
            pdf_response = requests.get(pdf_url)
            pdf_name = pdf_url.split('/')[-1]

            blob_client = container_client.get_blob_client(pdf_name)
            blob_client.upload_blob(pdf_response.content)

    return func.HttpResponse(f"This HTTP triggered function executed successfully.")
