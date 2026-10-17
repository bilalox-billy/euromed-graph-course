// Customers placed orders
UNWIND [
  {customerId: 'C001', orderId: 'O001', channel: 'web'},
  {customerId: 'C002', orderId: 'O002', channel: 'mobile'},
  {customerId: 'C003', orderId: 'O003', channel: 'web'}
] AS row
MATCH (c:Customer {customerId: row.customerId}),
      (o:Order    {orderId:    row.orderId})
MERGE (c)-[:PLACED {channel: row.channel}]->(o)
