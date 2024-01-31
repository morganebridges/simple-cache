
This project is a simple key/value datastore. 

It will provide the following functionality:
- SET a value based on a key / value pair
- GET the current value for a key (no transaction isolation implemented)
- UNSET the current value for a key (no transaction isolation implemented)
- BEGIN a transaction (re-entrant, so we may nest transactions, and roll back the inner while committing the outer)
- COMMIT all open transactions
- ROLLBACK a transaction (rolling back the latest changes only, multiple rollbacks are possible if multiple transactions are open)


