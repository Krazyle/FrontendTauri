# OGC API Features - Items

This document describes the API for interacting with features (items) within a spatial collection.

## Architecture

1. **Global Read-Only Endpoints**: Proxied directly to `pg_featureserv`. These follow the OGC API Features standard for retrieval.
2. **Project-Scoped Management Endpoints**: Native FastAPI endpoints for transactional editing (Part 4: Editing) within a project context.

---

## Global Proxied Endpoints (via `pg_featureserv`)

Standard OGC retrieval of features.

### `GET /collections/{collection_id}/items`
Returns features in the collection as a GeoJSON `FeatureCollection`.

**Query Parameters:**
- `limit`: Number of features to return (default: 10).
- `offset`: Pagination offset.
- `bbox`: Bounding box filter (`minx,miny,maxx,maxy`).
- `filter`: CQL2 filtering.

### `GET /collections/{collection_id}/items/{item_id}`
Returns a single feature as GeoJSON.

---

## Project-Scoped Management Endpoints (Native)

Transactional operations on features within a project.

### Feature Management
- `POST /projects/{project_id}/collections/{collection_id}/items/`: Add a new feature.
- `GET /projects/{project_id}/collections/{collection_id}/items/{feature_id}`: Read a specific feature.
- `PATCH /projects/{project_id}/collections/{collection_id}/items/{feature_id}`: Partially update a feature (geometry or properties).
- `DELETE /projects/{project_id}/collections/{collection_id}/items/{feature_id}`: Delete a feature.
