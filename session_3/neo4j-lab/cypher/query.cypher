MATCH (alice:Customer {name: 'Alice Chen'})
          -[:PLACED]->(:Order)
          -[:CONTAINS]->(aliceProduct:Product)
          -[:SIMILAR_TO]->(similarProduct:Product)
          <-[:CONTAINS]-(:Order)
          <-[:PLACED]-(otherCustomer:Customer)
          -[:PLACED]->(:Order)
          -[:CONTAINS]->(recommended:Product)
    WHERE otherCustomer <> alice
      AND NOT (alice)-[:PLACED]->(:Order)-[:CONTAINS]->(recommended)
    RETURN recommended.name  AS productName,
           recommended.price AS price,
           COUNT(DISTINCT otherCustomer) AS buyerCount
    ORDER BY buyerCount DESC
    LIMIT 20