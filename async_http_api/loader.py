from fastapi import FastAPI
from api_wrapper.wrapper import APIWrapper

app = FastAPI()
api_wrapper: APIWrapper = APIWrapper()
