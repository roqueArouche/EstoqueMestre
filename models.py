from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    formato = db.Column(db.String(20), nullable=False)  # L, mg, ml, etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    entradas = db.relationship('Entrada', backref='produto', lazy=True)
    saidas = db.relationship('Saida', backref='produto', lazy=True)
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    def calcular_estoque_atual(self, data_limite=None):
        """Calcula o estoque atual baseado nas entradas e saídas"""
        query_entradas = Entrada.query.filter_by(produto_id=self.id)
        query_saidas = Saida.query.filter_by(produto_id=self.id)
        
        if data_limite:
            query_entradas = query_entradas.filter(Entrada.data <= data_limite)
            query_saidas = query_saidas.filter(Saida.data <= data_limite)
        
        total_entradas = sum([entrada.quantidade for entrada in query_entradas.all()])
        total_saidas = sum([saida.quantidade for saida in query_saidas.all()])
        
        return total_entradas - total_saidas
    
    def calcular_entradas_periodo(self, data_inicio, data_fim):
        """Calcula total de entradas em um período"""
        entradas = Entrada.query.filter_by(produto_id=self.id).filter(
            Entrada.data >= data_inicio,
            Entrada.data <= data_fim
        ).all()
        return sum([entrada.quantidade for entrada in entradas])
    
    def calcular_saidas_periodo(self, data_inicio, data_fim):
        """Calcula total de saídas em um período"""
        saidas = Saida.query.filter_by(produto_id=self.id).filter(
            Saida.data >= data_inicio,
            Saida.data <= data_fim
        ).all()
        return sum([saida.quantidade for saida in saidas])

class Entrada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False, default=lambda: date.today())
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Entrada {self.quantidade}>'

class Saida(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    quantidade = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False, default=lambda: date.today())
    observacoes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Saida {self.quantidade}>'