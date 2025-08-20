from sys import prefix
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from app.core.models import Projects
from app.core.models.db_helper import DataBaseHelper
from app.shemas.products import ProjectReadAll

router = APIRouter(tags=["Projects"])


@router.get("/my_projects/{user_id}")
async def get_my_project(
    user_id: str,
    session: AsyncSession = Depends(DataBaseHelper.session_getter),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid user_id: {user_id}",
        )
    try:
        my_project_stmt = (
            select(Projects)
            .where(Projects.user_id == user_uuid)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(
                    Projects.photos
                ),  # подтягиваем все фотографии одним запросом
                selectinload(Projects.user),  # подтягиваем пользователя одним запросом
            )
        )
        my_project_result = await session.execute(my_project_stmt)
        my_projects = my_project_result.scalars().all()
        stmt_total = (
            select(func.count())
            .select_from(Projects)
            .where(Projects.user_id == user_uuid)
        )
        result_total = await session.execute(stmt_total)
        total = result_total.scalar_one()
    except SQLAlchemyError as e:
        raise HTTPException(
            detail=f"Database error: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
    return {"projects": my_projects, "total": total}


@router.get("/all_project", response_model=ProjectReadAll)
async def all_project(
    session: AsyncSession = Depends(DataBaseHelper.session_getter),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    try:
        stmt = (
            select(Projects)
            .offset(skip)
            .limit(limit)
            .options(
                selectinload(
                    Projects.photos
                ),  # подтягиваем все фотографии одним запросом
                selectinload(Projects.user),  # подтягиваем пользователя одним запросом
            )
        )
        result = await session.execute(stmt)
        projects = result.scalars().all()
        stmt_total = select(func.count()).select_from(Projects)
        result_total = await session.execute(stmt_total)
        total = result_total.scalar_one()
    except SQLAlchemyError as e:
        raise HTTPException(
            detail=f"Database error: {str(e)}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
    return {"projects": projects, "total": total}


@router.get("/project/{project_id}")
async def get_project_by_id(progect_id: str):
    pass
