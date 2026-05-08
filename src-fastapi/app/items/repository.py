import json
from typing import Any
from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_AsGeoJSON, ST_GeomFromGeoJSON
from sqlalchemy import Column, MetaData, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.collections.models import Collection
from app.items.schemas import ItemCreate, ItemUpdate


class ItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _build_table(self, collection: Collection) -> Table:
        metadata = MetaData(schema=collection.schema_name)
        geom_type = collection.geometry_type.value.upper() if collection.geometry_type else None
        columns = [
            Column(collection.id_column),
            Column(
                collection.geometry_column,
                Geometry(geometry_type=geom_type, srid=collection.srid),
            ),
        ]
        return Table(collection.table_name, metadata, *columns, extend_existing=True)

    @staticmethod
    def _to_feature(
        row: Any, id_col: str, geom_col: str, geometry: dict[str, Any]
    ) -> dict[str, Any]:
        properties = {
            k: v for k, v in row._mapping.items() if k not in (id_col, geom_col, "geometry")
        }
        return {
            "id": row._mapping[id_col],
            "geometry": geometry,
            "properties": properties,
            "type": "Feature",
        }

    async def create(self, collection: Collection, item: ItemCreate) -> dict[str, Any] | None:
        table = self._build_table(collection)
        geom_col = collection.geometry_column
        id_col = collection.id_column
        values: dict[str, Any] = {geom_col: ST_GeomFromGeoJSON(item.geometry.model_dump_json())}
        if item.properties:
            values.update(item.properties)
        stmt = (
            table.insert()
            .values(**values)
            .returning(table, ST_AsGeoJSON(table.c[geom_col]).label("geometry"))
        )
        result = await self.session.execute(stmt)
        row = result.mappings().first()
        await self.session.commit()
        if row:
            return self._to_feature(row, id_col, geom_col, json.loads(row["geometry"]))
        return None

    async def update(
        self, collection: Collection, feature_id: str | int, item: ItemUpdate
    ) -> dict[str, Any] | None:
        table = self._build_table(collection)
        geom_col = collection.geometry_column
        id_col = collection.id_column
        values: dict[str, Any] = {}
        if item.geometry:
            values[geom_col] = ST_GeomFromGeoJSON(item.geometry.model_dump_json())
        if item.properties:
            values.update(item.properties)
        if not values:
            stmt = select(table, ST_AsGeoJSON(table.c[geom_col]).label("geometry")).where(
                table.c[id_col] == feature_id
            )
            result = await self.session.execute(stmt)
            row = result.mappings().first()
            if row:
                return self._to_feature(row, id_col, geom_col, json.loads(row["geometry"]))
            return None
        stmt = (
            table.update()
            .values(**values)
            .where(table.c[id_col] == feature_id)
            .returning(table, ST_AsGeoJSON(table.c[geom_col]).label("geometry"))
        )
        result = await self.session.execute(stmt)
        row = result.mappings().first()
        await self.session.commit()
        if row:
            return self._to_feature(row, id_col, geom_col, json.loads(row["geometry"]))
        return None

    async def delete(self, collection: Collection, feature_id: str | int) -> bool:
        table = self._build_table(collection)
        id_col = collection.id_column
        stmt = table.delete().where(table.c[id_col] == feature_id).returning(table.c[id_col])
        result = await self.session.execute(stmt)
        row = result.fetchone()
        await self.session.commit()
        return row is not None
