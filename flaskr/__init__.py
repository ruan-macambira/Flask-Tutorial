"""Factory da Aplicação"""
import os
from flask import Flask

def create_app(test_config=None):
    """Criar e Configurar App"""
    # instance_relative_config=True -> arquivos de configuracao são
    # referenciados relativamente ao diretório de instâncias
    # diretório de instâncias(instance folders) ->
    #   https://flask.palletsprojects.com/en/1.1.x/config/#instance-folders
    app = Flask(__name__, instance_relative_config=True)
    # Define configurações padrões usada pelo App
    app.config.from_mapping(
        # Usado para manter dados seguros, em produção deve conter uma string
        # aleatória
        # mais: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY
        SECRET_KEY='dev',
        # Caminho em que o DB SQLite será salvo
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///db.sqlite'

    # app.config.from_pyfile() -> Sobrescreve as configurações padrões com
    # valores de config.py presente no diretório de instância, caso esteja
    # presente.
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Garantir que o diretório de instância existe
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import schema
    from .schema import user, post
    schema.init_app(app)

    from .blueprints import auth, blog, author
    # app.register_blueprint -> Inserir Blueprint à Aplicação. <ais em:
    # https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.register_blueprint
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(author.bp)
    # Definir um enpoint para blog.index, de modo que tanto 'index' quanto
    # 'blog.index' funcionem, gerando a mesma URL
    app.add_url_rule('/', endpoint='index')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        """Hello, World"""
        return 'Hello, World!'

    return app
