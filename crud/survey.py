from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import CrudBase
from model import Survey


class CrudSurvey(CrudBase[Survey]):
    def __init__(self, db: AsyncSession):
        super().__init__(Survey, db)
