from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server
    SERVER_MODE: str = "multi-worker"  # multi-worker | single-worker | stdio
    PORT: int = 3000
    HOST: str = "0.0.0.0"

    # Datadog
    DD_SERVICE: str = "devops-awx-mcp"
    DD_VERSION: str = "1.0.0"
    DD_ENV: str = "development"
    APM_INSTRUMENTATION: bool = False

    # API paths
    PREFIX_PATH: str = "/devops-awx-mcp"
    HEALTHY_PATH: str = "/healthy"
    LIVENESS_PATH: str = "/liveness"

    # AWX connection
    ANSIBLE_BASE_URL: str = "http://localhost"
    ANSIBLE_USERNAME: str = ""
    ANSIBLE_PASSWORD: str = ""
    ANSIBLE_TOKEN: str = ""
    ANSIBLE_VERIFY_SSL: bool = True
    ANSIBLE_TIMEOUT: int = 30

    model_config = {"env_file": ".env", "extra": "ignore"}


def load_config() -> Settings:
    return Settings()
