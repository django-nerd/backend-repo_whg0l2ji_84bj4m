import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Person

app = FastAPI(title="Hundred API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hundred backend is running"}


@app.get("/test")
def test_database():
    """Verify database connectivity and show sample collections"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# -------- People Endpoints --------
class PersonCreate(BaseModel):
    name: str
    initials: Optional[str] = None
    avatar_url: Optional[str] = None
    color: Optional[str] = None
    bio: Optional[str] = None
    tier: int = 3
    tags: List[str] = []
    favorite: bool = False
    angle: Optional[float] = None


@app.post("/api/people")
def create_person(person: PersonCreate):
    try:
        inserted_id = create_document("person", person)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/people")
def list_people(limit: int = 100, tier: Optional[int] = None):
    try:
        filter_dict = {}
        if tier in (1, 2, 3, 4):
            filter_dict["tier"] = tier
        docs = get_documents("person", filter_dict=filter_dict, limit=limit)
        # Convert ObjectId to string for JSON
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return {"people": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
