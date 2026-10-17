from pathlib import Path
from neo4j import GraphDatabase, Driver
from typing import Any
from neo4j_config import Neo4jConfig

# Root of the cypher folder (one level above src/)
CYPHER_DIR = Path(__file__).parent.parent / "neo4j-lab" / "cypher"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _run_dir(session, directory: Path) -> None:
    """Execute every *.cypher file in *directory* (sorted) as a single query each."""
    for cypher_file in sorted(directory.glob("*.cypher")):
        session.run(_read(cypher_file))
        print(f"    {cypher_file.name}")


def create_ecommerce_seed_graph(driver: Driver, database: str = "neo4j") -> None:
    """
    Create a minimal e-commerce property graph for module demonstrations.

    Schema:
        (:Customer)-[:PLACED]->(:Order)-[:CONTAINS {quantity, unitPrice}]->(:Product)
        (:Product)-[:BELONGS_TO]->(:Category)-[:SUBCATEGORY_OF]->(:Category)
        (:Product)-[:SIMILAR_TO {score}]->(:Product)
    """
    with driver.session(database=database) as session:

        # Step0: Load Constraints (split on ; because each is a separate DDL statement) ──
        print("  Constraints:")
        for stmt in _read(CYPHER_DIR / "constraints.cypher").split(";"):
            stmt = stmt.strip()
            if stmt:
                session.run(stmt)
        print("    constraints.cypher")

        # Step1: Load Nodes
        print("  Nodes:")
        _run_dir(session, CYPHER_DIR / "nodes")

        # Step2 LoadRelationships
        print("  Relationships:")
        _run_dir(session, CYPHER_DIR / "relationships")

    print("✓ Seed graph created successfully")


def run_alice_recommendation_query(driver: Driver, database: str = "neo4j") -> list[dict[str, Any]]:
    """
    Execute recommendation query:
    'Products bought by customers who bought products similar to what Alice bought'

    Returns list of {productName, price, buyerCount} dicts sorted by buyerCount desc.
    """
    query = _read(CYPHER_DIR / "query.cypher").strip()

    with driver.session(database=database) as session:
        result = session.run(query)
        return [dict(record) for record in result]


if __name__ == "__main__":
    config = Neo4jConfig.from_env()
    driver = GraphDatabase.driver(config.uri, auth=(config.username, config.password))

    try:
        create_ecommerce_seed_graph(driver, config.database)
        recommendations = run_alice_recommendation_query(driver, config.database)
        print(recommendations)
        print("\n--- Alice's Recommendations ---")
        for rec in recommendations:
            print(f"  {rec['productName']} (${rec['price']:.2f}) — bought by {rec['buyerCount']} similar customer(s)")
    finally:
        driver.close()
