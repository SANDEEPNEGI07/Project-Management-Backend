from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.api.routes import auth, users, tasks, organizations, projects, user_profiles

router = APIRouter()

_protected = {"dependencies": [Depends(get_current_user)]}

router.include_router(auth.router, prefix="/auth")
router.include_router(users.router, prefix="/users", **_protected)
router.include_router(tasks.router, prefix="/tasks", **_protected)
router.include_router(organizations.router, prefix="/organizations", **_protected)
router.include_router(projects.router, prefix="/projects", **_protected)
router.include_router(user_profiles.router, prefix="/user-profiles", **_protected)
