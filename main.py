from fastapi import FastAPI

app = FastAPI()

#Path Operator  Decorator
@app.get('/') #Home
def home():
    return {"Hello":"World"}