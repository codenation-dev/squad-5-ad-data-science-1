from os import path

import final_project_squad5

base_path = path.dirname(path.dirname(final_project_squad5.__file__))
workspace_path = path.join(base_path, 'workspace')
data_path = path.join(workspace_path, 'data')
models_path = path.join(workspace_path, 'models')
