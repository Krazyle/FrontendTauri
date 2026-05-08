# OGC API Features - Collections

This document describes the API for managing spatial collections, following the OGC API - Features (Part 1: Core) standard. These endpoints are served as **Read-Only** by `pg_featureserv` and will be matched with **Write Operations** in the FastAPI backend.

## Endpoints

### `GET /collections`
Returns a list of all available spatial collections (PostGIS tables and views).

**Response:**
- `200 OK`: A `CollectionList` object containing an array of `Collection` metadata.

### `GET /collections/{collectionId}`
Returns detailed metadata for a specific collection.

**Path Parameters:**
- `collectionId`: The unique identifier of the collection (usually in `schema.table` format).

**Response:**
- `200 OK`: A `Collection` object.
- `404 Not Found`: If the collection does not exist.

---

## Proposed Write Operations (FastAPI Backend)

To complement `pg_featureserv`, the following write operations will be implemented in the FastAPI backend.

### `POST /collections`
*Note: This is out of scope for pg_featureserv automatic discovery, but could be used to create new tables.*

- **Action**: Create a new spatial collection (database table).
- **Body**: Table schema definition and geometry type.
