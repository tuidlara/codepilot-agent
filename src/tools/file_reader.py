class FileReader:

    def read(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            return f"Arquivo não encontrado: {file_path}"