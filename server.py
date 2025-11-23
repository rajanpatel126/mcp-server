from fastmcp import FastMCP
import json

mcp = FastMCP('Remote server')

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

@mcp.tool()
def generate_random_number(min_value: int=1, max_value: int=100) -> int:
    """Generate a random number between min_value and max_value."""
    import random
    return random.randint(min_value, max_value)

@mcp.resource("info://server")
def server_info() -> str:
    info = {
        'server_name': 'Simple FastMCP Remote Server',
        'version': '1.0.0',
        'tools': ['add_numbers', 'generate_random_number'],
        'resources': ['info://server'],
        'description': 'A simple FastMCP server providing basic tools.'
    }
    return json.dumps(info, indent=2)
    
if __name__ == "__main__":
    mcp.run(transport='http', host='0.0.0.0', port=8000)
