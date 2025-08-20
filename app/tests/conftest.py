import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool.impl import NullPool

from app.api.utils.jwt_utils import get_current_user
from app.core.config import settings
from app.core.models import Projects
from app.core.models.base import Base
from app.core.models.db_helper import DataBaseHelper
from app.core.models.projects import PhotoProjects
from app.core.models.users import Users
from app.main import my_app
from app.shemas.user import Role

from httpx import AsyncClient, ASGITransport


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


@pytest.fixture(autouse=True)
async def override_dependencies(session: AsyncSession):
    async def _get_db_override():
        yield session

    my_app.dependency_overrides[DataBaseHelper.session_getter] = _get_db_override
    yield
    my_app.dependency_overrides.clear()


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
async def create_projects(session: AsyncSession, create_users):
    user, admin = create_users
    project1 = Projects(project_name="project1", user_id=admin.id)
    project2 = Projects(project_name="project2", user_id=admin.id)
    session.add_all([project1, project2])
    await session.commit()
    # чтобы можно было использовать в тестах
    yield project1, project2, admin
    for obj in (project1, project2, admin):
        await session.delete(obj)
    await session.commit()


@pytest.fixture
async def create_photo_projects(session: AsyncSession, create_projects):
    project1, project2, admin = create_projects
    photo_proj1 = PhotoProjects(link="https://1...", project_id=project1.id)
    photo_proj2 = PhotoProjects(link="https://2...", project_id=project1.id)
    photo_proj3 = PhotoProjects(link="https://3...", project_id=project1.id)
    photo_proj4 = PhotoProjects(link="https://3...", project_id=project2.id)
    photo_proj5 = PhotoProjects(link="https://3...", project_id=project2.id)
    session.add_all([photo_proj1, photo_proj2, photo_proj3, photo_proj4, photo_proj5])
    await session.commit()
    yield photo_proj1, photo_proj2, photo_proj3, photo_proj4, photo_proj5, project1, project2
    for obj in (photo_proj1, photo_proj2, photo_proj3, photo_proj4, photo_proj5):
        await session.delete(obj)
    await session.commit()


@pytest.fixture()
async def init_db(session: AsyncSession):
    user = Users(username="test_user_init", role=Role.user)
    admin = Users(username="test_admin_init", role=Role.admin)
    session.add_all([user, admin])
    await session.flush()

    # Добавляем проекты
    projects = [
        Projects(project_name="project1_init", user_id=admin.id),
        Projects(project_name="project2_init", user_id=admin.id),
    ]
    session.add_all(projects)
    await session.flush()

    # Добавляем фотографии
    photos = [
        PhotoProjects(link="https://1..._init", project_id=projects[0].id),
        PhotoProjects(link="https://2..._init", project_id=projects[0].id),
        PhotoProjects(link="https://3..._init", project_id=projects[0].id),
        PhotoProjects(link="https://4..._init", project_id=projects[1].id),
        PhotoProjects(link="https://5..._init", project_id=projects[1].id),
    ]
    session.add_all(photos)

    await session.commit()
    yield {
        "users": {"user": user, "admin": admin},
        "projects": projects,
        "photos": photos,
    }

    for obj in photos + [*projects, user, admin]:
        await session.delete(obj)
    await session.commit()


BASE_URL_DISH = "http://test/api/v1"


@pytest.fixture()
async def client():
    async with AsyncClient(
        transport=ASGITransport(my_app), base_url=BASE_URL_DISH
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
async def override_current_user(session: AsyncSession):
    async def _override():
        user = Users(username="test_admin_init23", role=Role.admin)
        session.add(user)
        await session.commit()
        return user

    my_app.dependency_overrides[get_current_user] = _override
    yield
    my_app.dependency_overrides.clear()
