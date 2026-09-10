# Architecture

Campus Lost & Found is a modular monolith. The browser uses the Fetch API to call Flask REST blueprints. Routes validate HTTP concerns and delegate business rules to services. SQLAlchemy models represent the MySQL contract, while image processing is isolated behind an image matching engine so the embedding model can be replaced later.

```text
frontend (HTML, Bootstrap, JavaScript)
              |
        Flask REST API
              |
 authentication | items | matching | messaging | admin services
              |
       SQLAlchemy + MySQL
              |
     file storage + embeddings
```

Phase 1 establishes the app factory, configuration boundary, database extension, upload directory, CORS policy, consistent errors, and health endpoint. Later phases add one vertical slice at a time and verify each slice before moving on.
