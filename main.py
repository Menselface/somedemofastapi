import os

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from http_client import CMCHTTPClient
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


cmc_client = CMCHTTPClient(
    base_url="https://pro-api.coinmarketcap.com",
    api_key=os.getenv('CMS_API_KEY')
)


@app.get("/cryptocurrencies")
async def get_cryptocurrencies():
    return await cmc_client.get_listings()


@app.get("/cryptocurrencies/{currency_id}")
async def get_cryptocurrencies(currency_id: int):
    return await cmc_client.get_currency(currency_id)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
