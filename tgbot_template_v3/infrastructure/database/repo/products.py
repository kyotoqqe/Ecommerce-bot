from sqlalchemy import select
from sqlalchemy.orm import joinedload

from infrastructure.database.models import Product
from infrastructure.database.repo.base import BaseRepo



class ProductRepo(BaseRepo):
    async def products_list(self):
        stmt = select(Product).options(joinedload(Product.feature_media)).order_by(Product.product_id)
        res = await self.session.execute(stmt)
        return res.unique().scalars()
    
    async def get_single(self,product_id):
        stmt = select(Product).options(joinedload(Product.medias)).filter_by(product_id=product_id)
        res = await self.session.execute(stmt)
        return res.unique().scalar_one()

    

