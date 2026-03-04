import json

from src.services.system_service import SystemService


def register_system_tools(mcp, system_ops: SystemService):
    @mcp.tool()
    def get_ansible_version() -> str:
        """Get Ansible Tower/AWX version information."""
        with system_ops.client:
            return json.dumps(system_ops.get_version(), indent=2)

    @mcp.tool()
    def get_dashboard_stats() -> str:
        """Get dashboard statistics."""
        with system_ops.client:
            return json.dumps(system_ops.get_dashboard(), indent=2)

    @mcp.tool()
    def get_metrics() -> str:
        """Get system metrics."""
        with system_ops.client:
            try:
                return json.dumps(system_ops.get_metrics(), indent=2)
            except Exception as e:
                return json.dumps({"status": "error", "message": str(e)})
