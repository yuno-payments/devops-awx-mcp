import json

from services.base_service import BaseCRUDService
from utils.validators import validate_json


def register_credential_tools(mcp, service: BaseCRUDService, type_service: BaseCRUDService):
    @mcp.tool()
    def list_credentials(limit: int = 100, offset: int = 0) -> str:
        """List all credentials."""
        with service.client:
            return json.dumps(service.list(limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def get_credential(credential_id: int) -> str:
        """Get details about a specific credential."""
        with service.client:
            return json.dumps(service.get(credential_id), indent=2)

    @mcp.tool()
    def list_credential_types(limit: int = 100, offset: int = 0) -> str:
        """List all credential types."""
        with service.client:
            return json.dumps(type_service.list(limit=limit, offset=offset), indent=2)

    @mcp.tool()
    def create_credential(
        name: str,
        credential_type_id: int,
        organization_id: int,
        inputs: str,
        description: str = "",
    ) -> str:
        """Create a new credential."""
        try:
            parsed_inputs = validate_json(inputs, "inputs")
        except ValueError as e:
            return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            data = {
                "name": name,
                "credential_type": credential_type_id,
                "organization": organization_id,
                "inputs": parsed_inputs,
                "description": description,
            }
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_credential(credential_id: int, name: str = None, inputs: str = None, description: str = None) -> str:
        """Update an existing credential."""
        parsed_inputs = None
        if inputs:
            try:
                parsed_inputs = validate_json(inputs, "inputs")
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            data = {}
            if name:
                data["name"] = name
            if parsed_inputs is not None:
                data["inputs"] = parsed_inputs
            if description:
                data["description"] = description
            return json.dumps(service.update(credential_id, data), indent=2)

    @mcp.tool()
    def delete_credential(credential_id: int) -> str:
        """Delete a credential."""
        with service.client:
            return json.dumps(service.delete(credential_id), indent=2)
