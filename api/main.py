import json
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, 'q-vercel-python.json')) as f:
    students_data = json.load(f)

@app.get('/')
async def index():
    return {"message": "Welcome to the FastAPI application!"}


@app.get('/api')
async def get_marks(names: List[str] = Query(None)):
    if not names:
        return {"error": "No names provided"}
    marks = []
    for name in names:
        mark = next((student["marks"] for student in students_data 
                     if student["name"].lower() == name.lower()), None)
        marks.append(mark)
    
    return {"marks": marks}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)
