import os
from openai import AzureOpenAI

api_key = os.getenv("AZURE_API_KEY")
endpoint = os.getenv("AZURE_API_BASE")
api_version = os.getenv("AZURE_API_VERSION")
deployment_name = "gpt-4o-deployment"

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)