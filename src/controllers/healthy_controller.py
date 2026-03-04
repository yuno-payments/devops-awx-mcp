import os


def get_root():
    return {
        "service": os.environ.get("DD_SERVICE", "devops-awx-mcp"),
        "version": os.environ.get("DD_VERSION", "1.0.0"),
    }


def get_health():
    return {
        "status": "healthy",
        "service": os.environ.get("DD_SERVICE", "devops-awx-mcp"),
        "version": os.environ.get("DD_VERSION", "1.0.0"),
        "environment": os.environ.get("DD_ENV", "development"),
    }


def get_liveness():
    return {"status": "alive"}
