# Default Jupyter server config
# Note: those config can be overridden by user-level configs. 

c.ServerApp.terminado_settings = { 'shell_command': ['/bin/bash'] }
c.ServerApp.tornado_settings = { 'compress_response': True }

# Do not delete files to trash. Instead, permanently delete files. 
c.FileContentsManager.delete_to_trash = False

# Allow deleting non-empty directory via file browser
# Related documentation: https://github.com/jupyter-server/jupyter_server/blob/main/jupyter_server/services/contents/filemanager.py#L125-L129
c.FileContentsManager.always_delete_dir = True

# Enable `allow_hidden` by default, so hidden files are accessible via Jupyter server
# Related documentation: https://jupyterlab.readthedocs.io/en/stable/user/files.html#displaying-hidden-files
c.ContentsManager.allow_hidden = True
