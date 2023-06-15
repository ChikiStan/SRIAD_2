from asyncpg import Pool
from pydantic import BaseModel


class ExperimentValues(BaseModel):
    timestamp: int
    head: str
    feet_r: str


class ExperimentValuesRepository:
    def __init__(self, db: Pool):
        self._db = db

    async def add_new(
        self,
        experiment_id: int,
        feet_r: str,
        feet_l: str,
    ) -> None:
        sql = """
            insert into "experiment_values" (
            "experiment_id",
            "feet_r",
            "feet_l")
            values ($1,$2,$3)"""
        async with self._db.acquire() as c:
            await c.execute(sql, experiment_id, feet_r, feet_l)
