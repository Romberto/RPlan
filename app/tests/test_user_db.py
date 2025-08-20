import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.shemas.user import Role


@pytest.mark.asyncio
async def test_db_users(session: AsyncSession, create_users):
    user, admin = create_users
    assert user.role == Role.user
    assert admin.role == Role.admin
