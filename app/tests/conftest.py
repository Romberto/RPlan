import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool.impl import NullPool

from app.core.config import settings
from app.core.models import Projects
from app.core.models.base import Base
from app.core.models.projects import PhotoProjects
from app.core.models.users import Users
from app.shemas.user import Role


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# Создаём engine и session_factory внутри фикстуры
@pytest.fixture(scope="session")
async def engine():
    if settings.run.debug != 1:
        pytest.exit("❌ Тесты можно запускать только в режиме DEBUG", returncode=1)

    engine = create_async_engine(
        str(settings.db.test_url),
        echo=False,
        poolclass=NullPool,  # ВАЖНО: без пула, чтобы избежать конфликтов loop'ов
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
async def create_users(session: AsyncSession):
    user = Users(username="test_user", role=Role.user)
    admin = Users(username="test_admin", role=Role.admin)
    session.add_all([user, admin])
    await session.commit()
    # чтобы можно было использовать в тестах
    yield user, admin

    await session.delete(user)
    await session.delete(admin)
    await session.commit()

@pytest.fixture
async def create_projects(session: AsyncSession, create_users ):
    user, admin = create_users
    project1 = Projects(project_name="project1", user_id= admin.id)
    project2 = Projects(project_name="project2", user_id= admin.id)
    session.add_all([project1, project2])
    await session.commit()
    # чтобы можно было использовать в тестах
    yield project1, project2, admin
    for obj in (project1, project2, admin):
        await session.delete(obj)
    await session.commit()


@pytest.fixture
async def create_photo_projects(session:AsyncSession, create_projects):
    project1, project2, admin = create_projects
    photo_proj1 = PhotoProjects(link="https://1...", project_id=project1.id)
    photo_proj2 = PhotoProjects(link="https://2...", project_id=project1.id)
    photo_proj3 = PhotoProjects(link="https://3...", project_id=project1.id)
    photo_proj4 = PhotoProjects(link="https://3...", project_id=project2.id)
    photo_proj5 = PhotoProjects(link="https://3...", project_id=project2.id)
    session.add_all([photo_proj1,photo_proj2,photo_proj3, photo_proj4,photo_proj5])
    await session.commit()
    yield photo_proj1, photo_proj2, photo_proj3,photo_proj4,photo_proj5, project1, project2
    for obj in (photo_proj1, photo_proj2, photo_proj3,photo_proj4,photo_proj5):
        await session.delete(obj)
    await session.commit()

