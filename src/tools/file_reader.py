from pathlib import Path

class FileReader:
    
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent.parent

    def read(self, file_path):
        path = Path(file_path)
        path = path.resolve()
        
        if not path.is_relative_to(self.project_root):
            return "Acesso ao arquivo não permitido."
        
        try:
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
            
        except FileNotFoundError:
            return f"Arquivo não encontrado: {file_path}"