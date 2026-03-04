from unittest.mock import MagicMock

import pytest

from services.workflow_service import WorkflowService


@pytest.fixture
def workflow_service():
    client = MagicMock()
    return WorkflowService(client)


class TestWorkflowService:
    def test_launch(self, workflow_service):
        workflow_service.client.request.return_value = {"id": 10, "status": "pending"}

        result = workflow_service.launch(1, extra_vars='{"env": "prod"}')
        assert result["id"] == 10
        workflow_service.client.request.assert_called_with(
            "POST", "/api/v2/workflow_job_templates/1/launch/", data={"extra_vars": '{"env": "prod"}'}
        )

    def test_launch_no_extra_vars(self, workflow_service):
        workflow_service.client.request.return_value = {"id": 10}

        workflow_service.launch(1)
        workflow_service.client.request.assert_called_with(
            "POST", "/api/v2/workflow_job_templates/1/launch/", data={}
        )

    def test_list_jobs(self, workflow_service):
        workflow_service.client.request.return_value = {
            "count": 1,
            "results": [{"id": 1}],
            "next": None,
        }

        results = workflow_service.list_jobs(status="running")
        assert len(results) == 1

    def test_get_job(self, workflow_service):
        workflow_service.client.request.return_value = {"id": 1, "status": "successful"}

        result = workflow_service.get_job(1)
        assert result["status"] == "successful"

    def test_cancel_job(self, workflow_service):
        workflow_service.client.request.return_value = {"status": "success"}

        workflow_service.cancel_job(1)
        workflow_service.client.request.assert_called_with("POST", "/api/v2/workflow_jobs/1/cancel/")
