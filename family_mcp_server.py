#!/usr/bin/env python3
"""
MCP Server for family data
"""

import asyncio
import sys
from typing import Any, Dict, List

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server


class FamilyDetails:
    """Simple family relationship database"""

    def __init__(self):
        # Family relationship data
        self.relationships = {
            "dave": {
                "mother": "angel",
                "father": "smith",
                "sister": "liss, joe",
                "spouse":""
            },
            "Ben": {
                "mother": "lenny",
                "father": "jimmy",
                "sister": "dan, gilchrist",
                "spouse": "jasmine"
            },
            "Siva": {
                "mother": "",
                "father": "",
                "son": "murugan, ayyapan, ganapathy",
                "spouse": "parvathy"
            }
        }

    def get_relationship(self, person: str, relationship_type: str) -> str:
        """Get relationship information"""
        person = person.lower().strip()
        relationship_type = relationship_type.lower().strip()

        if person in self.relationships:
            if relationship_type in self.relationships[person]:
                return self.relationships[person][relationship_type]

        return f"No {relationship_type} information found for {person}"

    def get_all_relationships(self, person: str) -> Dict[str, str]:
        """Get all relationships for a person"""
        person = person.lower().strip()
        if person in self.relationships:
            return self.relationships[person]
        return {}


# Create server instance
app = Server("family-data-server")
family_db = FamilyDetails()


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """Return list of available tools"""
    return [
        types.Tool(
            name="get_family_member",
            description="Get family member information (mother, father, etc.)",
            inputSchema={
                "type": "object",
                "properties": {
                    "person": {
                        "type": "string",
                        "description": "Name of the person"
                    },
                    "relationship": {
                        "type": "string",
                        "description": "Type of relationship (mother, father, etc.)"
                    }
                },
                "required": ["person", "relationship"]
            }
        ),
        types.Tool(
            name="get_all_family",
            description="Get all family relationships for a person",
            inputSchema={
                "type": "object",
                "properties": {
                    "person": {
                        "type": "string",
                        "description": "Name of the person"
                    }
                },
                "required": ["person"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Handle tool calls"""
    try:
        print(f"[DEBUG] Tool called: {name} with args: {arguments}", file=sys.stderr)

        if name == "get_family_member":
            person = arguments["person"]
            relationship = arguments["relationship"]
            result = family_db.get_relationship(person, relationship)

        elif name == "get_all_family":
            person = arguments["person"]
            relationships = family_db.get_all_relationships(person)
            if relationships:
                result = f"Family of {person}: " + ", ".join([f"{rel}: {name}" for rel, name in relationships.items()])
            else:
                result = f"No family information found for {person}"

        else:
            result = f"Unknown tool: {name}"

        print(f"[DEBUG] Result: {result}", file=sys.stderr)
        return [types.TextContent(type="text", text=result)]

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[ERROR] {error_msg}", file=sys.stderr)
        return [types.TextContent(type="text", text=error_msg)]


async def main():
    """Main entry point"""
    try:
        print("[INFO] Starting Family Data MCP Server...", file=sys.stderr)

        async with stdio_server() as (read_stream, write_stream):
            print("[INFO] Server ready and listening...", file=sys.stderr)
            await app.run(read_stream, write_stream, app.create_initialization_options())

    except Exception as e:
        print(f"[ERROR] Server failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())