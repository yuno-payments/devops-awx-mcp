import json

from services.base_service import BaseCRUDService
from utils.validators import validate_json


def register_schedule_tools(mcp, service: BaseCRUDService):
    @mcp.tool()
    def list_schedules(unified_job_template_id: int = None, limit: int = 100, offset: int = 0) -> str:
        """List schedules, optionally filtered by job template."""
        with service.client:
            kwargs = {}
            if unified_job_template_id:
                kwargs["unified_job_template"] = unified_job_template_id
            return json.dumps(service.list(limit=limit, offset=offset, **kwargs), indent=2)

    @mcp.tool()
    def get_schedule(schedule_id: int) -> str:
        """Get details about a specific schedule."""
        with service.client:
            return json.dumps(service.get(schedule_id), indent=2)

    @mcp.tool()
    def create_schedule(
        name: str,
        unified_job_template_id: int,
        rrule: str,
        description: str = "",
        extra_data: str = "{}",
    ) -> str:
        """Create a new schedule."""
        try:
            parsed_extra = validate_json(extra_data, "extra_data")
        except ValueError as e:
            return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            data = {
                "name": name,
                "unified_job_template": unified_job_template_id,
                "rrule": rrule,
                "description": description,
                "extra_data": parsed_extra,
            }
            return json.dumps(service.create(data), indent=2)

    @mcp.tool()
    def update_schedule(
        schedule_id: int,
        name: str = None,
        rrule: str = None,
        description: str = None,
        extra_data: str = None,
    ) -> str:
        """Update an existing schedule."""
        parsed_extra = None
        if extra_data:
            try:
                parsed_extra = validate_json(extra_data, "extra_data")
            except ValueError as e:
                return json.dumps({"status": "error", "message": str(e)})
        with service.client:
            data = {}
            if name:
                data["name"] = name
            if rrule:
                data["rrule"] = rrule
            if description:
                data["description"] = description
            if parsed_extra is not None:
                data["extra_data"] = parsed_extra
            return json.dumps(service.update(schedule_id, data), indent=2)

    @mcp.tool()
    def delete_schedule(schedule_id: int) -> str:
        """Delete a schedule."""
        with service.client:
            return json.dumps(service.delete(schedule_id), indent=2)
