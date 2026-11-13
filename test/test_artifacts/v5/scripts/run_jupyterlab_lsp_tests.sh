#!/bin/bash

#imports test
python -c "import jupyter_lsp" || { echo "jupyter_lsp import test failed"; exit 1; }
python -c "import jupyterlab_lsp" || { echo "jupyterlab_lsp import test failed"; exit 1; }

TEST_DIR=$(mktemp -d)
cd "$TEST_DIR"

python - <<EOF
import json
from jupyter_lsp import LanguageServerManager 
from jupyter_lsp.specs import SpecBase
from jupyter_lsp.types import KeyedLanguageServerSpecs

# Test LanguageServerManager
manager = LanguageServerManager()

# Test spec registration
class TestSpec(SpecBase):
    python_like = True
    languages = ["python"]
    display_name = "Test Python LSP"
    
    def is_installed(self):
        return True

# Register the test spec
manager.register(TestSpec)

# Get available languages
available_languages = manager.language_servers
assert "python" in available_languages, "Python language server not found"

# Test spec retrieval
specs = manager.get_language_server_specs()
assert isinstance(specs, KeyedLanguageServerSpecs), "Invalid specs type"

# Test configuration
config = manager.get_configuration({})
assert isinstance(config, dict), "Invalid configuration type"
EOF

# Python file creation and LSP detection
cat << EOF > test.py
def hello_world():
    print("Hello, World!")
    return None
EOF

# LSP functionality with the created file
python - <<EOF
import os
from jupyter_lsp import LanguageServerManager

manager = LanguageServerManager()

# Test file detection
current_dir = os.getcwd()
test_file = os.path.join(current_dir, "test.py")
assert os.path.exists(test_file), "Test file not created"

# Test language detection
file_types = manager.file_types_for_document(test_file)
assert "python" in file_types, "Python file type not detected"
EOF

rm -rf "$TEST_DIR"

