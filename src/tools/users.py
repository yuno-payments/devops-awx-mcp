import json

from src.services.base_service import BaseCRUDService


def register_user_tools(mcp, service: BaseCRUDService):
    @mcp.tool()
    def list_users(limit: int = 100, offset: int = 0) -> str:
        """List all users."""
        with service.client:
            return json.dumps(service.list(limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_user(user_id: int) -> str:
        """Get details about a specific user."""
        with service.client:
            return json.dumps(service.get(user_id), indent=2)

    @mcp.tool()
    def create_user(
        username: str,
        password: str,
        first_name: str = "",
        last_name: str = "",
        email: str = "",
        is_superuser: bool = False,
        is_system_auditor: bool = False,
    ) -> str:
        """Create a new user."""
        with service.client:
            data = {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "is_superuser": is_superuser,
                "is_system_auditor": is_system_auditor,
            }
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_user(
        user_id: int,
        username: str = None,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        is_superuser: bool = None,
        is_system_auditor: bool = None,
    ) -> str:
        """Update an existing user."""
        with service.client:
            data = {}
            if username:
                data["username"] = username
            if password:
                data["password"] = password
            if first_name is not None:
                data["first_name"] = first_name
            if last_name is not None:
                data["last_name"] = last_name
            if email:
                data["email"] = email
            if is_superuser is not None:
                data["is_superuser"] = is_superuser
            if is_system_auditor is not None:
                data["is_system_auditor"] = is_system_auditor
            return json.dumps(service.update(user_id, data), indent=2)

    @mcp.tool()
    def delete_user(user_id: int) -> str:
        """Delete a user."""
        with service.client:
            return json.dumps(service.delete(user_id), indent=2)
