from pprint import pprint
import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from starlette import status

from app.core.models import Projects


async def test_all_projects(
    client: AsyncClient, session: AsyncSession, create_projects
):
    response = await client.get("/all_project")
    assert response.status_code == status.HTTP_200_OK
    stmt = select(func.count()).select_from(Projects)
    result = await session.execute(stmt)
    count = result.scalar_one()
    data = response.json()
    assert count == len(data["projects"])


async def test_get_my_project(
    client: AsyncClient, create_projects, session: AsyncSession
):
    project1, project2, admin = create_projects
    response = await client.get(f"/my_projects/{admin.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 2


@pytest.mark.parametrize(
    "user_id, status_code",
    [
        ("1234", 422),  # некорректный UUID
        ("00000000-0000-0000-0000-000000000000", 200),  # валидный UUID, но нет проектов
    ],
)
async def test_get_my_project_invalid(client: AsyncClient, user_id, status_code):
    response = await client.get(f"/my_projects/{user_id}")
    assert response.status_code == status_code
