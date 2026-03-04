import json

from src.services.ad_hoc_service import AdHocService
from src.utils.validators import validate_verbosity


def register_ad_hoc_tools(mcp, ad_hoc_ops: AdHocService):
    @mcp.tool()
    def run_ad_hoc_command(
        inventory_id: int,
        credential_id: int,
        module_name: str,
        module_args: str,
        limit: str = "",
        verbosity: int = 0,
    ) -> str:
        """Run an ad hoc command."""
        try:
            validate_verbosity(verbosity)
        except ValueError as e:
            return json.dumps({"status": "error", "message": str(e)})
        with ad_hoc_ops.client:
            return json.dumps(
                ad_hoc_ops.run(inventory_id, credential_id, module_name, module_args, limit, verbosity),
                indent=2,
            )

    @mcp.tool()
    def get_ad_hoc_command(command_id: int) -> str:
        """Get details about a specific ad hoc command."""
        with ad_hoc_ops.client:
            return json.dumps(ad_hoc_ops.get(command_id), indent=2)

    @mcp.tool()
    def cancel_ad_hoc_command(command_id: int) -> str:
        """Cancel a running ad hoc command."""
        with ad_hoc_ops.client:
            try:
                return json.dumps(ad_hoc_ops.cancel(command_id), indent=2)
            except (ValueError, Exception) as e:
                return json.dumps({"status": "error", "message": str(e)})
