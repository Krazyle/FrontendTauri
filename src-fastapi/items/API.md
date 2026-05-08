# OGC API Features - Items

This document describes the API for interacting with features within a collection. While `pg_featureserv` provides the Read-Only Core, the FastAPI backend will provide the **Part 4: Editing** (Transactional) functionality.

## Read Operations (pg_featureserv)

### `GET /collections/{collectionId}/items`
Fetch a set of features from a collection.

**Query Parameters:**
- `limit`: Number of features to return (default 10).
- `offset`: Number of features to skip.
- `bbox`: Bounding box filter (`min_lon,min_lat,max_lon,max_lat`).
- `properties`: Comma-separated list of properties to include.
- `transform`: Server-side spatial transformation (e.g., `Centroid`).

**Response:**
- `200 OK`: A GeoJSON `FeatureCollection`.

### `GET /collections/{collectionId}/items/{featureId}`
Fetch a single feature by ID.

**Response:**
- `200 OK`: A GeoJSON `Feature`.

---

## Write Operations (FastAPI Backend)

The following endpoints implement the **OGC API - Features - Part 4: Editing** standard.

### `POST /collections/{collectionId}/items`
Create a new feature in the collection.

**Body:** A GeoJSON `Feature` or a dictionary of properties.
**Response:** `201 Created` with a `Location` header pointing to the new feature.

### `PATCH /collections/{collectionId}/items/{featureId}`
Update specific properties or the geometry of an existing feature.

**Body:** Partial GeoJSON `Feature` object.
**Response:** `200 OK` or `204 No Content`.

### `PUT /collections/{collectionId}/items/{featureId}`
Replace an entire feature.

**Body:** Full GeoJSON `Feature` object.
**Response:** `200 OK` or `204 No Content`.

### `DELETE /collections/{collectionId}/items/{featureId}`
Permanently remove a feature from the collection.

**Response:** `204 No Content`.
