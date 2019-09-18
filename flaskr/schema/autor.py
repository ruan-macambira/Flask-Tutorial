from . import DB

class Autor(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    nome = DB.Column(DB.String(100), nullable=False)
    email = DB.Column(DB.String(255), nullable=False)

    artigos = DB.relationship('Artigo', lazy=False)

    def __repr__(self):
        return '< Autor %s>' % self.nome

    def __str__(self):
        return self.nome
