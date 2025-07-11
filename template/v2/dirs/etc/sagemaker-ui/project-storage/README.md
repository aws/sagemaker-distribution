## SageMaker Unified Studio Space

Welcome to your project space
This is the root folder for your project files. It contains:
- A shared folder for collaborative work
- Your personal local folder for private development

### Personal local folder
Your personal local folder:
- Includes this root folder and any subfolders (except shared)
- Allows you to work on files privately
- Ideal for frequent file access and modification
- Is visible only in this space

### Shared folder
The shared folder:
- Contains files visible to all project members
- Is accessible across all your tools
- Updates immediately when any member adds or modifies files
- Not well-suited for heavy file read/write workloads due to remote Amazon S3 origin of this folder and potential additional costs associated with frequent Amazon S3 access
- If two individuals are modifying the same file in this folder at the same time that might result in losing some changes


To share your files with other project members, copy or move them to the shared folder when ready.