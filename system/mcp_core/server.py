
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INTERNAL MCP CORE (Model Context Protocol)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Allows the AI to "discover" and "use" tools dynamically.
# This makes the system self-sustainable as new tools are added.

import inspect
from typing import Callable, Dict, Any, List
import json

class MCPTool:
    """Standard definition of a Tool in our OS."""
    def __init__(self, name: str, func: Callable, description: str, usage_schema: Dict):
        self.name = name
        self.func = func
        self.description = description
        self.usage_schema = usage_schema

    def execute(self, **kwargs):
        return self.func(**kwargs)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "schema": self.usage_schema
        }

class MCPServer:
    """
    The Local Server that manages all available tools.
    The Brain queries this server to know what it can do.
    """
    def __init__(self):
        self.registry: Dict[str, MCPTool] = {}

    def register_tool(self, tool: MCPTool):
        self.registry[tool.name] = tool

    def list_tools(self) -> List[Dict]:
        return [t.to_dict() for t in self.registry.values()]

    def get_tool(self, name: str) -> MCPTool:
        return self.registry.get(name)

    def auto_discover(self, module):
        """
        Intelligently scans a Python module for functions and converts them to MCP Tools.
        """
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if not name.startswith("_"):
                # Create a simple schema based on inspection
                sig = inspect.signature(func)
                params = {k: "any" for k in sig.parameters.keys()}
                
                tool = MCPTool(
                    name=name,
                    func=func,
                    description=func.__doc__ or "No description provided.",
                    usage_schema=params
                )
                self.register_tool(tool)
