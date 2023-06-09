# Author: Ty Andrews
# Date: 2023-05-05

import os
import sys

import pandas as pd
import pyarrow.parquet as pq
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Get environment variables
AZ_DATA_CONTAINER = os.getenv("AZ_BLOB_DATA_CONTAINER")
AZ_ACCOUNT_URL = os.getenv("AZ_BLOB_ACCOUNT_URL")


class AzureBlob:
    def __init__(self, container_name=AZ_DATA_CONTAINER, account_url=AZ_ACCOUNT_URL):
        """Initialize Azure Blob Storage client and authenticate.

        Parameters
        ----------
        container_name : str, optional
            Name of the container, by default AZ_DATA_CONTAINER
        account_url : str, optional
            URL of the Azure Blob Storage account, by default AZ_ACCOUNT_URL

        Returns
        -------
        None
        """
        self.container_name = container_name
        self.account_url = account_url
        self.default_credential = DefaultAzureCredential(
            exclude_shared_token_cache_credential=True
        )
        self.blob_service_client = BlobServiceClient(
            account_url, credential=self.default_credential
        )
        self.container_client = self.blob_service_client.get_container_client(
            container=self.container_name
        )

    def list_blobs(self):
        """List all blobs in the container

        Returns
        -------
        list
            List of blobs in the container
        """
        return self.container_client.list_blobs()

    def load_parquet(self, blob_path):
        """Load a parquet file from Azure Blob Storage

        Parameters
        ----------
        blob_path : str
            Path to the parquet file in the container

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame of the parquet file

        Raises
        ------
        FileNotFoundError
            If the blob_path does not exist in the container
        """
        downloaded_blob = self.container_client.download_blob(blob_path)
        bytes_io = BytesIO(downloaded_blob.readall())
        df = pd.read_parquet(bytes_io)

        return df
