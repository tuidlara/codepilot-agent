from pathlib import Path


class ProjectExplorer:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent.parent

    def execute(self):
        ignored_dirs = {".venv", ".git", "__pycache__"}
        
        # acessa subpastas também
        #files contem só arquivos
        files = [
            file
            for file in self.project_root.rglob("*")
            if file.is_file()
            and not any(
                part in ignored_dirs
                for part in file.relative_to(self.project_root).parts
            )
            
        ]
        return [str(file.relative_to(self.project_root)) for file in files]