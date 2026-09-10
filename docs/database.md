# Database Design

The normalized schema is in `database/schema.sql`. Users own items; items own image references; matches link one lost item to one found item; messages, notifications, and reports reference the relevant users and records.

Private verification answers are stored on the item but are never included in public item responses. Images and embeddings remain files, with only safe references stored in MySQL. Search indexes cover report type, status, category, location, and date to support candidate filtering.
