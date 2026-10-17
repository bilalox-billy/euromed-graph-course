from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import os

from neo4j import GraphDatabase, Driver, Session
from dotenv import load_dotenv

load_dotenv()



@dataclass(frozen=True)
class Neo4jConfig:
    """Immutable client for Neo4j database connection."""

    uri: str
    username: str
    password: str
    database: str

    @classmethod
    def from_env(cls) -> Neo4jConfig:
        return cls(
            uri=os.getenv("NEO4J_URI"),
            username=os.getenv("NEO4J_USERNAME"),
            password=os.getenv("NEO4J_PASSWORD"),
            database=os.getenv("NEO4J_DATABASE", "neo4j"),
        )

