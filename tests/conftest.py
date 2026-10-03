"""Hermetic imports for the pure-function tests: stub heavy optional dependencies ONLY when they are not installed.

CI installs just ruff and pytest, so `import agent` (which imports google.adk, python-dotenv and pandas at module level) could
never succeed there. Where the real packages are installed they are used untouched."""
import importlib.util
import sys
import types


def _missing(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is None
    except (ImportError, ValueError):
        return True


if _missing("google.adk"):
    class _Stub:
        def __init__(self, *args, **kwargs):
            self.args, self.kwargs = args, kwargs

    google = sys.modules.setdefault("google", types.ModuleType("google"))
    adk, agents, tools = (types.ModuleType(n) for n in ("google.adk", "google.adk.agents", "google.adk.tools"))
    agents.LlmAgent = type("LlmAgent", (_Stub,), {})
    tools.FunctionTool = type("FunctionTool", (_Stub,), {})
    google.adk = adk
    sys.modules.update({"google.adk": adk, "google.adk.agents": agents, "google.adk.tools": tools})
if _missing("dotenv"):
    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda *a, **k: False
    sys.modules["dotenv"] = dotenv
if _missing("pandas"):
    sys.modules["pandas"] = types.ModuleType("pandas")
