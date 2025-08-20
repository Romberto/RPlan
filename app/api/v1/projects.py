from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Query
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from app.api.utils.jwt_utils import get_current_user
from app.core.models import Projects, Users
from app.core.models.db_helper import DataBaseHelper
from app.shemas.products import ProjectReadAll, ProjectRead, ProjectCreate
from app.shemas.user import Role
from app.tests.conftest import init_db

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


@router.get("/project/{project_name}", response_model=ProjectRead)
async def get_project_by_project_name(
    project_name: str, session: AsyncSession = Depends(DataBaseHelper.session_getter)
):
    try:
        stmt = (
            select(Projects)
            .where(Projects.project_name == project_name)
            .options(selectinload(Projects.photos))
        )
        result = await session.execute(stmt)
        project = result.scalars().first()
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
    return project


@router.post("/add_project", response_model=ProjectRead)
async def add_project(
    data: ProjectCreate,
    session: AsyncSession = Depends(DataBaseHelper.session_getter),
    current_user: Users = Depends(get_current_user),
):
    if current_user.role == Role.admin:
        try:
            project = Projects(
                project_name=data.project_name,
                comments=data.comments,
                user_id=current_user.id,
                photos=data.photos,
            )
            session.add(project)
            await session.commit()
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
    else:
        raise HTTPException(
            detail="You don't have permission to access this resource.",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return project
