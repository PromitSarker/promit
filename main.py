import json
import os
import secrets
import uuid
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BASE = Path(__file__).parent
DATA = BASE / "data.json"
TOKEN = os.getenv("ADMIN_TOKEN", "change-me")  # দিয়ে চালান: ADMIN_TOKEN=আপনার-গোপন-কোড

app = FastAPI(title="Portfolio API")

class Project(BaseModel):
    title: str
    desc: str
    tags: List[str] = []
    github: str = ""
    live: str = ""
    icon: str = ""

def load_data() -> list:
    """Load projects from data.json."""
    if not DATA.exists():
        return []
    return json.loads(DATA.read_text("utf-8"))

def save_data(data: list) -> None:
    """Save projects to data.json."""
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")

def authenticate(token: Optional[str]) -> None:
    """Check if the provided token matches the admin token."""
    if not secrets.compare_digest(token or "", TOKEN):
        raise HTTPException(status_code=401, detail="ভুল অ্যাডমিন কোড")

@app.get("/api/projects")
def list_projects():
    """Retrieve all projects."""
    return load_data()

@app.post("/api/projects", status_code=201)
def add_project(project: Project, x_token: Optional[str] = Header(None)):
    """Add a new project."""
    authenticate(x_token)
    data = load_data()
    
    new_item = {
        "id": uuid.uuid4().hex[:8],
        **project.model_dump()
    }
    
    data.insert(0, new_item)
    save_data(data)
    
    return new_item

@app.put("/api/projects/{project_id}")
def edit_project(project_id: str, project: Project, x_token: Optional[str] = Header(None)):
    """Edit an existing project."""
    authenticate(x_token)
    data = load_data()
    
    for i, item in enumerate(data):
        if item.get("id") == project_id:
            data[i] = {
                "id": project_id,
                **project.model_dump()
            }
            save_data(data)
            return data[i]
            
    raise HTTPException(status_code=404, detail="প্রজেক্ট পাওয়া যায়নি")

@app.delete("/api/projects/{project_id}")
def remove_project(project_id: str, x_token: Optional[str] = Header(None)):
    """Delete a project."""
    authenticate(x_token)
    data = load_data()
    
    new_data = [item for item in data if item.get("id") != project_id]
    
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="প্রজেক্ট পাওয়া যায়নি")
        
    save_data(new_data)
    return {"ok": True}

@app.get("/admin")
def admin_page():
    """Serve the admin interface."""
    return FileResponse(BASE / "static/admin.html")

# Serve the static files (index.html, styles, etc.) at the root
app.mount("/", StaticFiles(directory=BASE / "static", html=True), name="static")
