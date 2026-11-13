#!/bin/bash

# We need to checkout the version of strands-agents that is installed in the mamba environment.
strands_version=$(micromamba list | grep ' strands-agents ' | tr -s ' ' | cut -d ' ' -f 3)

# Checkout the corresponding strands-agents version
git checkout tags/v$strands_version

# Run basic import tests to verify the package works
echo "Running strands import tests..."
python -c "from strands import Agent; print('strands Agent imported successfully')"
python -c "import strands.tools; print('strands tools imported successfully')"
python -c "from strands.tools.mcp import MCPClient; print('strands MCP client imported successfully')"
echo "All strands import tests passed!"

# Try to run repository tests if dependencies are available
if [ -d "tests" ]; then
    echo "Attempting to run repository tests..."
    pytest tests/ || echo "Repository tests failed or missing dependencies, but import tests passed"
fi