# Directory Structure

This document outlines the key directory structure used in SageMaker Distribution images.

## Web Client Libraries

### `/etc/web-client/libs/`
Shared JavaScript libraries for all web applications in the container.

**Contents:**
- `jszip.min.js` - ZIP file handling library used by JupyterLab, VSCode, and other web clients

**Usage:**
Any web application can reference these shared libraries to avoid duplication.

## Amazon Q Integration

### `/etc/amazon-q/artifacts/`
Amazon Q specific artifacts organized by IDE type.

**Structure:**
```
/etc/amazon-q-agentic-chat/
└── artifacts/
    ├── jupyterlab/        # JupyterLab integration
    │   ├── servers/       # Server-side artifacts
    │   └── clients/       # Client-side artifacts
    └── vscode/            # Future VSCode integration
        ├── servers/
        └── clients/
```

## Benefits

1. **Reusability**: Shared libraries in `/etc/web-client/libs/` prevent duplication
2. **Modularity**: Each IDE has its own artifact directory under `/etc/amazon-q/artifacts/`
3. **Scalability**: Easy to add new IDEs or web applications
4. **Maintainability**: Clear separation between shared and application-specific resources