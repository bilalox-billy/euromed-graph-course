// Order line items
UNWIND [
  {orderId: 'O001', productId: 'P001', quantity: 1, unitPrice: 1999.00},
  {orderId: 'O001', productId: 'P002', quantity: 1, unitPrice:  349.99},
  {orderId: 'O002', productId: 'P004', quantity: 1, unitPrice:  279.99},
  {orderId: 'O003', productId: 'P003', quantity: 1, unitPrice: 1799.00},
  {orderId: 'O003', productId: 'P005', quantity: 1, unitPrice:   59.99}
] AS row
MATCH (o:Order   {orderId:   row.orderId}),
      (p:Product {productId: row.productId})
MERGE (o)-[:CONTAINS {quantity: row.quantity, unitPrice: row.unitPrice}]->(p)
