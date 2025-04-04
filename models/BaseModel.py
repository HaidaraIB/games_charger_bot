import sqlalchemy as sa
from models.DB import Base, lock_and_release, connect_and_close
from sqlalchemy.orm import Session, joinedload


class BaseModel(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    id = sa.Column(sa.Integer, autoincrement=True, primary_key=True)

    @classmethod
    @lock_and_release
    async def add(cls, vals: dict, s: Session = None):
        res = s.execute(sa.insert(cls).values(vals).prefix_with("OR IGNORE"))
        return res.lastrowid

    @classmethod
    @lock_and_release
    async def update(cls, row_id: int, update_dict: dict, s: Session = None):
        s.query(cls).filter_by(id=row_id).update(update_dict)

    @lock_and_release
    async def update_one(self, update_dict: dict, s: Session = None):
        s.query(type(self)).filter_by(id=self.id).update(update_dict)

    @classmethod
    @lock_and_release
    async def delete(cls, attr, val, s: Session = None):
        s.query(cls).filter(getattr(cls, attr) == val).delete()

    @lock_and_release
    async def delete_one(self, s: Session = None):
        s.query(type(self)).filter_by(id=self.id).delete()

    @classmethod
    @connect_and_close
    def get_by(
        cls,
        conds: dict = None,
        all: bool = False,
        limit: int = None,
        group_by: str = [],
        eager_load: list[str] = [],
        s: Session = None,
    ):
        query = sa.select(cls)

        if eager_load:
            query = query.options(
                joinedload(*[getattr(cls, relationship) for relationship in eager_load])
            )

        if conds:
            query = query.where(
                sa.and_(*[getattr(cls, attr) == val for attr, val in conds.items()])
            )
        if limit:
            query = query.limit(limit)

        # Execute query
        res = s.scalars(query)
        return res.all() if all else res.first()
