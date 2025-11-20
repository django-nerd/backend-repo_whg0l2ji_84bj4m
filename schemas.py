"""
Database Schemas for Hundred

Each Pydantic model represents a collection in MongoDB. The collection name
is the lowercase of the class name (e.g., Person -> "person").
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Literal


class Person(BaseModel):
    """A person in the user's Hundred network.

    Collection: "person"
    """
    name: str = Field(..., description="Full name")
    initials: Optional[str] = Field(None, description="Initials fallback if no avatar")
    avatar_url: Optional[HttpUrl] = Field(None, description="URL to circular avatar image")
    color: Optional[str] = Field(None, description="Hex color identity for the node (e.g., #6D9EF5)")
    bio: Optional[str] = Field(None, description="Short, warm micro-bio shown on hover/modal")
    tier: Literal[1, 2, 3, 4] = Field(3, description="Closeness ring: 1=Inner, 2=Close, 3=Familiar, 4=Extended")
    tags: List[str] = Field(default_factory=list, description="Clusters/tags like Family, Friends, Work")
    favorite: bool = Field(False, description="Is this a starred/favorited person")
    angle: Optional[float] = Field(None, description="Optional polar angle (degrees) for placement")


# Example additional models can be defined here if needed
