import json
from typing import Any
from sqlalchemy import text, Table, MetaData, Column, Integer, String, select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_AsGeoJSON, ST_GeomFromGeoJSON

from collections.models import Collection
from items.schemas import ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.metadata = MetaData()

    async def _get_table(self, collection: Collection) -> Table:
        # For simplicity in this prototype, we reflect or construct the table dynamically.
        # In a production app, we might want to cache these table objects.
        
        # We construct the table definition based on collection metadata
        table = Table(
            collection.table_name,
            self.metadata,
            Column(collection.id_column, Integer, primary_key=True),
            # Other columns are dynamic. We might need to reflect them to be fully generic.
            schema=collection.schema_name,
            extend_existing=True
        )
        return table

    async def create(self, collection: Collection, item: ItemCreate) -> dict[str, Any]:
        geom_json = json.dumps(item.geometry)
        
        cols = [collection.geometry_column]
        vals = ["ST_GeomFromGeoJSON(:geom)"]
        params = {"geom": geom_json}
        
        if item.properties:
            for k, v in item.properties.items():
                cols.append(k)
                vals.append(f":{k}")
                params[k] = v
                
        query = text(f"""
            INSERT INTO {collection.schema_name}.{collection.table_name} 
            ({", ".join(cols)})
            VALUES ({", ".join(vals)})
            RETURNING {collection.id_column}, ST_AsGeoJSON({collection.geometry_column}) as geometry, *
        """)
        
        result = await self.session.execute(query, params)
        row = result.mappings().first()
        await self.session.commit()
        
        if row:
            return self._row_to_item(row, collection)
        return {}

    async def get(self, collection: Collection, feature_id: str | int) -> dict[str, Any] | None:
        query = text(f"""
            SELECT {collection.id_column}, ST_AsGeoJSON({collection.geometry_column}) as geometry, *
            FROM {collection.schema_name}.{collection.table_name}
            WHERE {collection.id_column} = :id
        """)
        result = await self.session.execute(query, {"id": feature_id})
        row = result.mappings().first()
        
        if row:
            return self._row_to_item(row, collection)
        return None

    async def update(self, collection: Collection, feature_id: str | int, item: ItemUpdate) -> dict[str, Any] | None:
        # Partial update
        updates = []
        params = {"id": feature_id}
        
        if item.geometry:
            updates.append(f"{collection.geometry_column} = ST_GeomFromGeoJSON(:geom)")
            params["geom"] = json.dumps(item.geometry)
            
        if item.properties:
            for k, v in item.properties.items():
                updates.append(f"{k} = :{k}")
                params[k] = v
                
        if not updates:
            return await self.get(collection, feature_id)
            
        query = text(f"""
            UPDATE {collection.schema_name}.{collection.table_name}
            SET {", ".join(updates)}
            WHERE {collection.id_column} = :id
            RETURNING {collection.id_column}, ST_AsGeoJSON({collection.geometry_column}) as geometry, *
        """)
        
        result = await self.session.execute(query, params)
        row = result.mappings().first()
        await self.session.commit()
        
        if row:
            return self._row_to_item(row, collection)
        return None

    async def delete(self, collection: Collection, feature_id: str | int) -> bool:
        query = text(f"""
            DELETE FROM {collection.schema_name}.{collection.table_name}
            WHERE {collection.id_column} = :id
        """)
        result = await self.session.execute(query, {"id": feature_id})
        await self.session.commit()
        return result.rowcount > 0

    def _row_to_item(self, row: dict[str, Any], collection: Collection) -> dict[str, Any]:
        data = dict(row)
        fid = data.pop(collection.id_column)
        geometry = json.loads(data.pop("geometry"))
        # Remove internal columns if any (e.g. the original geom column which is now binary)
        data.pop(collection.geometry_column, None)
        
        return {
            "id": fid,
            "geometry": geometry,
            "properties": data,
            "type": "Feature"
        }
