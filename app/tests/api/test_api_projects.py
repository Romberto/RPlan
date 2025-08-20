
from pprint import pprint
from uuid import UUID

import pytest
from fastapi import HTTPException
from httpx import AsyncClient
from pydantic_core import ValidationError
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from starlette import status
from contextlib import nullcontext as not_raise_exc
from app.core.models import Projects
from app.shemas.products import ProjectCreate


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


async def test_get_project_by_project_name(client: AsyncClient, init_db):
    _init_db = init_db
    project_name = _init_db["projects"][0].project_name
    response = await client.get(f"/project/{project_name}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert UUID(data["id"]) == _init_db["projects"][0].id



@pytest.mark.parametrize(
    "project_name, exc", [
        ("valid_product_name", not_raise_exc()),
        (12345, pytest.raises(ValidationError))
        ]
    )
async def test_add_project(session: AsyncSession, init_db, client: AsyncClient , project_name, exc):
    with exc:
        data = ProjectCreate(project_name=project_name, comments="", photos=[])
        stmt_start = select(func.count()).select_from(Projects)
        result_start = await session.execute(stmt_start)
        start_count = result_start.scalar_one()
        response = await client.post("/add_project", json=data.model_dump())
        assert response.status_code == status.HTTP_200_OK
        stmt_end = select(func.count()).select_from(Projects)
        result_end = await session.execute(stmt_end)
        end_count = result_end.scalar_one()
        assert start_count == end_count - 1

