from sqlalchemy import select

from infrastructure.database.models import Category
from infrastructure.database.repo.base import BaseRepo

class CategoryRepo(BaseRepo):
    async def categories_list(self,parent_id=None):
        stmt = select(Category).filter_by(parent_id=parent_id).order_by(Category.name)
        res = await self.session.execute(stmt)
        return res.unique().scalars().all()