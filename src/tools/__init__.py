from client.ansible_client import AnsibleClient
from config import Settings
from services import (
    AdHocService,
    BaseCRUDService,
    GroupService,
    JobService,
    ProjectService,
    SystemService,
    WorkflowService,
)
from tools.ad_hoc import register_ad_hoc_tools
from tools.credentials import register_credential_tools
from tools.groups import register_group_tools
from tools.hosts import register_host_tools
from tools.inventories import register_inventory_tools
from tools.job_templates import register_job_template_tools
from tools.jobs import register_job_tools
from tools.organizations import register_organization_tools
from tools.projects import register_project_tools
from tools.schedules import register_schedule_tools
from tools.system import register_system_tools
from tools.teams import register_team_tools
from tools.users import register_user_tools
from tools.workflows import register_workflow_tools


def register_all_tools(mcp, config: Settings):
    client = AnsibleClient(config)

    inventory_service = BaseCRUDService(client, "/api/v2/inventories/")
    host_service = BaseCRUDService(client, "/api/v2/hosts/")
    group_service = BaseCRUDService(client, "/api/v2/groups/")
    group_ops = GroupService(client)
    job_template_service = BaseCRUDService(client, "/api/v2/job_templates/")
    job_service = JobService(client)
    project_service = BaseCRUDService(client, "/api/v2/projects/")
    project_ops = ProjectService(client)
    credential_service = BaseCRUDService(client, "/api/v2/credentials/")
    credential_type_service = BaseCRUDService(client, "/api/v2/credential_types/")
    organization_service = BaseCRUDService(client, "/api/v2/organizations/")
    team_service = BaseCRUDService(client, "/api/v2/teams/")
    user_service = BaseCRUDService(client, "/api/v2/users/")
    workflow_template_service = BaseCRUDService(client, "/api/v2/workflow_job_templates/")
    workflow_ops = WorkflowService(client)
    schedule_service = BaseCRUDService(client, "/api/v2/schedules/")
    ad_hoc_ops = AdHocService(client)
    system_ops = SystemService(client)

    register_inventory_tools(mcp, inventory_service)
    register_host_tools(mcp, host_service, client)
    register_group_tools(mcp, group_service, group_ops)
    register_job_template_tools(mcp, job_template_service, job_service)
    register_job_tools(mcp, job_service)
    register_project_tools(mcp, project_service, project_ops)
    register_credential_tools(mcp, credential_service, credential_type_service)
    register_organization_tools(mcp, organization_service)
    register_team_tools(mcp, team_service, client)
    register_user_tools(mcp, user_service)
    register_workflow_tools(mcp, workflow_template_service, workflow_ops)
    register_schedule_tools(mcp, schedule_service)
    register_ad_hoc_tools(mcp, ad_hoc_ops)
    register_system_tools(mcp, system_ops)

    return client
