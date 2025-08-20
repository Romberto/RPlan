

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Users
from app.tests.conftest import session


async def test_project_db(create_projects):
    pr1, pr2, admin = create_projects
    assert pr1.project_name == "project1"
    assert pr1.user_id == admin.id
    assert pr2.project_name == "project2"
    assert pr2.user_id == admin.id

async def test_photo_project_db(create_photo_projects):
    photo_proj1, photo_proj2, photo_proj3,photo_proj4,photo_proj5, project1, project2 = create_photo_projects
    assert photo_proj1.project_id == project1.id
    assert photo_proj5.project_id != project1.id
    assert photo_proj5.project_id == project2.id
    assert photo_proj4.project_id == project2.id
