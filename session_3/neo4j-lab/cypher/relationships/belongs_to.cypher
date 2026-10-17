// Products assigned to their categories
UNWIND [
  {productId: 'P001', categoryId: 'CAT02'},
  {productId: 'P003', categoryId: 'CAT02'},
  {productId: 'P002', categoryId: 'CAT03'},
  {productId: 'P004', categoryId: 'CAT03'},
  {productId: 'P005', categoryId: 'CAT01'}
] AS row
MATCH (p:Product    {productId:   row.productId}),
      (c:Category   {categoryId:  row.categoryId})
MERGE (p)-[:BELONGS_TO]->(c)
