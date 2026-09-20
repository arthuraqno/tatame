from sqlalchemy.orm import Session
from models.produto import Produto
from schemas.produto import ProdutoResponse
from database import engine

class ProdutoService: 
    def cadastrar_produto(self, nome, descricao, preco, categoria, tamanho, estoque, imagem_url):
        with Session(engine) as session:
            produto = Produto(
                nome = nome,
                descricao = descricao,
                preco = preco,
                categoria = categoria,
                tamanho = tamanho, 
                estoque = estoque,
                imagem_url = imagem_url)
            session.add(produto)
            session.commit()
            session.refresh(produto)
            return self._to_response(produto)
            

    def _to_response(self, produto: Produto) -> ProdutoResponse:
        return ProdutoResponse(
            id = produto.id,
            nome = produto.nome,
            descricao = produto.descricao,
            preco = produto.preco,
            categoria = produto.categoria,
            tamanho = produto.tamanho, 
            estoque = produto.estoque,
            imagem_url = produto.imagem_url,
            ativo= produto.ativo)

    def listar_produtos(self):
        with Session(engine) as session:
            produtos = session.query(Produto).all()
            return [self._to_response(produto) for produto in produtos]

    def buscar_produto(self, id):
        with Session(engine) as session:
            produto = session.query(Produto).filter(Produto.id == id).first()
            if produto is None:
                return None
            return self._to_response(produto)

    def atualizar_produto(self, id, nome = None, descricao = None, preco = None, categoria = None, tamanho = None, estoque = None, imagem_url = None):
        with Session(engine) as session:
            produto = session.get(Produto, id)
            if produto is None:
                return None
            if nome is not None:
                produto.nome = nome
            if descricao is not None:
                produto.descricao = descricao
            if preco is not None:
                produto.preco = preco
            if categoria is not None:
                produto.categoria = categoria
            if tamanho is not None:
                produto.tamanho = tamanho
            if estoque is not None:
                produto.estoque = estoque
            if imagem_url is not None:
                produto.imagem_url = imagem_url
            session.commit()
            return self._to_response(produto)

    def deletar_produto(self, id):
        with Session(engine) as session:
            produto = session.get(Produto, id)
            if produto is None:
                return None
            produto.ativo = False
            session.commit()
            return self._to_response(produto)
            
