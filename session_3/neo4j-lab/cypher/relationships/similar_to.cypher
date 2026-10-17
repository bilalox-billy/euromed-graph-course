// Bidirectional product similarity scores
UNWIND [
  {from: 'P001', to: 'P003', score: 0.87},
  {from: 'P003', to: 'P001', score: 0.87},
  {from: 'P002', to: 'P004', score: 0.91},
  {from: 'P004', to: 'P002', score: 0.91}
] AS row
MATCH (a:Product {productId: row.from}),
      (b:Product {productId: row.to})
MERGE (a)-[:SIMILAR_TO {score: row.score}]->(b)
