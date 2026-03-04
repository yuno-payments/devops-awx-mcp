from unittest.mock import MagicMock

import pytest

from services.job_service import JobService


@pytest.fixture
def job_service():
    client = MagicMock()
    return JobService(client)


class TestJobService:
    def test_list_jobs(self, job_service):
        job_service.client.request.return_value = {
            "count": 1,
            "results": [{"id": 1, "status": "successful"}],
            "next": None,
        }

        results = job_service.list_jobs(status="successful")
        assert len(results) == 1

    def test_get_job(self, job_service):
        job_service.client.request.return_value = {"id": 1, "status": "running"}

        result = job_service.get_job(1)
        assert result["status"] == "running"

    def test_cancel_job(self, job_service):
        job_service.client.request.return_value = {"status": "success"}

        job_service.cancel_job(1)
        job_service.client.request.assert_called_with("POST", "/api/v2/jobs/1/cancel/")

    def test_get_events(self, job_service):
        job_service.client.request.return_value = {
            "count": 2,
            "results": [{"id": 1, "event": "runner_on_ok"}, {"id": 2, "event": "playbook_on_stats"}],
            "next": None,
        }

        results = job_service.get_events(1)
        assert len(results) == 2

    def test_get_stdout_txt(self, job_service):
        mock_resp = MagicMock()
        mock_resp.text = "PLAY [all] ****"
        job_service.client.raw_get.return_value = mock_resp

        result = job_service.get_stdout(1, fmt="txt")
        assert result["stdout"] == "PLAY [all] ****"

    def test_get_stdout_json(self, job_service):
        job_service.client.request.return_value = {"content": "output"}

        result = job_service.get_stdout(1, fmt="json")
        assert result["content"] == "output"

    def test_get_stdout_invalid_format(self, job_service):
        with pytest.raises(ValueError, match="Invalid format"):
            job_service.get_stdout(1, fmt="xml")

    def test_launch_job(self, job_service):
        job_service.client.request.return_value = {"id": 42, "status": "pending"}

        result = job_service.launch_job(1, extra_vars='{"key": "value"}')
        assert result["id"] == 42
        job_service.client.request.assert_called_with(
            "POST", "/api/v2/job_templates/1/launch/", data={"extra_vars": '{"key": "value"}'}
        )

    def test_launch_job_no_extra_vars(self, job_service):
        job_service.client.request.return_value = {"id": 42}

        job_service.launch_job(1)
        job_service.client.request.assert_called_with("POST", "/api/v2/job_templates/1/launch/", data={})
