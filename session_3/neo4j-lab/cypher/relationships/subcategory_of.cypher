// Laptop and Audio are sub-categories of Electronics
MATCH (child:Category), (electronics:Category {categoryId: 'CAT01'})
WHERE child.categoryId IN ['CAT02', 'CAT03']
MERGE (child)-[:SUBCATEGORY_OF]->(electronics)
