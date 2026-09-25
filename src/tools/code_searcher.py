from pathlib import Path


class CodeSearcher:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent.parent

    def execute(self, pattern):
         # pastas que não queremos analisar, são arquivos de ambiente
        ignored_dirs = {".venv", ".git", "__pycache__"}

        # armazena os arquivos e linhas onde o padrão for encontrado
        results = []
        
        files = [
            file
            for file in self.project_root.rglob("*")
            if file.is_file()
            # percorre o projeto e pega apenas arquivos que não estão dentro das pastas ignoradas
            and not any(
                part in ignored_dirs
                for part in file.relative_to(self.project_root).parts
            )
        ]
        for file in files:
            try:
                with open(file, "r", encoding="utf-8") as f:
                    content = f.readlines()

                # percorre cada linha procurando o padrão informado
                for line_number, line in enumerate(content, start=1):
                    if pattern.lower() in line.lower():
                        results.append({
                            "file": str(file.relative_to(self.project_root)),
                            "line": line_number,
                            "content": line.strip()
                        })
                        
            except UnicodeDecodeError:
                continue
            
        return results
    