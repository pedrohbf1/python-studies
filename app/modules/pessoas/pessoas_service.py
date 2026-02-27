from app.modules.pessoas.pessoas_repository import PessoasRepository

class PessoasService:
    def __init__(self, repo: PessoasRepository):
        self.repo = repo

    def listar_pessoas(self):
        return self.repo.listar()
