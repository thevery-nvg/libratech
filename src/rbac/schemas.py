from pydantic import BaseModel
from typing import List, Optional


class PermissionBase(BaseModel):
    code: str
    description: Optional[str] = None


class PermissionRead(PermissionBase):
    id: int

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    permissions: List[str] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None


class RoleRead(RoleBase):
    id: int
    permissions: List[PermissionRead] = []

    class Config:
        from_attributes = True


class AssignRoleRequest(BaseModel):
    user_id: int
    role_id: int


class AssignRoleResponse(BaseModel):
    status: str
    user_id: int
    role: str
