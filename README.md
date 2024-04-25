Make sure to port forward the Neo4j database from the server:

```bash
ssh -L 7474:localhost:7474 -L 7687:localhost:7687 username@remote_server_ip
```

Example Cyper query to display all the names of nodes:

MATCH (n)
RETURN DISTINCT labels(n) AS node_labels