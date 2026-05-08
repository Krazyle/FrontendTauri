# OGC API Features - Collections

This document describes the API for managing spatial collections (metadata and tables), following the OGC API - Features (Part 1: Core) standard.

## Architecture

The API is split into two parts:
1. **Global Read-Only Endpoints**: Proxied directly to `pg_featureserv`. These follow the OGC API Features standard exactly and are used for data discovery and visualization.
2. **Project-Scoped Management Endpoints**: Native FastAPI endpoints for managing collection metadata, permissions, and registration within the context of a project.

---

## Global Proxied Endpoints (via `pg_featureserv`)

These endpoints provide a standard OGC view of all published spatial tables.

### `GET /collections`
Returns a list of all available spatial collections discovered by `pg_featureserv`.

### `GET /collections/{collection_id}`
Returns detailed metadata for a specific collection.

---

## Project-Scoped Management Endpoints (Native)

These endpoints manage the `project_collections` metadata and allow registration of tables to projects.

### Registration & Lifecycle
- `POST /projects/{project_id}/collections/`: Register a new collection (metadata only). Does **not** trigger DDL (table creation).
- `GET /projects/{project_id}/collections/`: List collections registered to a project.
- `GET /projects/{project_id}/collections/{id}`: Get metadata for a specific registered collection.
- `PATCH /projects/{project_id}/collections/{id}`: Update collection metadata (title, description, etc.).
- `PUT /projects/{project_id}/collections/{id}`: Replace collection metadata.
- `DELETE /projects/{project_id}/collections/{id}`: Unregister a collection (metadata removal). Does **not** drop the physical table.
