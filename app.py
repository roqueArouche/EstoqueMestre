from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from functools import wraps
from models import db, Produto, Entrada, Saida
from datetime import datetime, date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import os
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Credenciais de login
LOGIN_CREDENTIALS = {
    'username': 'igor',
    'password': 'igor2025'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if (username == LOGIN_CREDENTIALS['username'] and 
            password == LOGIN_CREDENTIALS['password']):
            session['logged_in'] = True
            session['username'] = username
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('produtos'))
        else:
            flash('Credenciais inválidas!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('login'))

@app.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring"""
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}, 200

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('produtos'))

@app.route('/produtos')
@login_required
def produtos():
    search = request.args.get('search', '')
    if search:
        produtos = Produto.query.filter(
            Produto.nome.contains(search) | 
            Produto.marca.contains(search)
        ).all()
    else:
        produtos = Produto.query.all()
    
    # Calcular estoque atual para cada produto
    produtos_com_estoque = []
    for produto in produtos:
        estoque_atual = produto.calcular_estoque_atual()
        produtos_com_estoque.append({
            'produto': produto,
            'estoque_atual': estoque_atual
        })
    
    return render_template('produtos.html', produtos=produtos_com_estoque, search=search)

@app.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def novo_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        marca = request.form['marca']
        formato = request.form['formato']
        
        # Gerar SKU automaticamente
        ultimo_produto = Produto.query.order_by(Produto.id.desc()).first()
        if ultimo_produto:
            proximo_numero = ultimo_produto.id + 1
        else:
            proximo_numero = 1
        sku = f"PRD{proximo_numero:04d}"
        
        produto = Produto(sku=sku, nome=nome, marca=marca, formato=formato)
        db.session.add(produto)
        db.session.commit()
        
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('produtos'))
    
    return render_template('produto_form.html')

@app.route('/produtos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.marca = request.form['marca']
        produto.formato = request.form['formato']
        # SKU não pode ser editado
        
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produtos'))
    
    return render_template('produto_form.html', produto=produto)

@app.route('/produtos/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('produtos'))

@app.route('/entradas')
@login_required
def entradas():
    entradas = Entrada.query.order_by(Entrada.data.desc()).all()
    return render_template('entradas.html', entradas=entradas)

@app.route('/entradas/nova', methods=['GET', 'POST'])
@login_required
def nova_entrada():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = float(request.form['quantidade'])
        data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        observacoes = request.form.get('observacoes', '')
        
        entrada = Entrada(
            produto_id=produto_id,
            quantidade=quantidade,
            data=data,
            observacoes=observacoes
        )
        db.session.add(entrada)
        db.session.commit()
        
        flash('Entrada registrada com sucesso!', 'success')
        return redirect(url_for('entradas'))
    
    produtos = Produto.query.all()
    return render_template('entrada_form.html', produtos=produtos)

@app.route('/entradas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_entrada(id):
    entrada = Entrada.query.get_or_404(id)
    
    if request.method == 'POST':
        entrada.produto_id = request.form['produto_id']
        entrada.quantidade = float(request.form['quantidade'])
        entrada.data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        entrada.observacoes = request.form.get('observacoes', '')
        
        db.session.commit()
        flash('Entrada atualizada com sucesso!', 'success')
        return redirect(url_for('entradas'))
    
    produtos = Produto.query.all()
    return render_template('entrada_form.html', produtos=produtos, entrada=entrada)

@app.route('/entradas/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_entrada(id):
    entrada = Entrada.query.get_or_404(id)
    db.session.delete(entrada)
    db.session.commit()
    flash('Entrada deletada com sucesso!', 'success')
    return redirect(url_for('entradas'))

@app.route('/saidas')
@login_required
def saidas():
    saidas = Saida.query.order_by(Saida.data.desc()).all()
    return render_template('saidas.html', saidas=saidas)

@app.route('/saidas/nova', methods=['GET', 'POST'])
@login_required
def nova_saida():
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = float(request.form['quantidade'])
        data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        observacoes = request.form.get('observacoes', '')
        
        # Verificar se há estoque suficiente
        produto = Produto.query.get(produto_id)
        if produto:
            estoque_atual = produto.calcular_estoque_atual()
            
            if quantidade > estoque_atual:
                flash(f'Estoque insuficiente! Disponível: {estoque_atual} {produto.formato}', 'error')
                produtos = Produto.query.all()
                return render_template('saida_form.html', produtos=produtos)
        
        saida = Saida(
            produto_id=produto_id,
            quantidade=quantidade,
            data=data,
            observacoes=observacoes
        )
        db.session.add(saida)
        db.session.commit()
        
        flash('Saída registrada com sucesso!', 'success')
        return redirect(url_for('saidas'))
    
    produtos = Produto.query.all()
    return render_template('saida_form.html', produtos=produtos)

@app.route('/saidas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_saida(id):
    saida = Saida.query.get_or_404(id)
    
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        nova_quantidade = float(request.form['quantidade'])
        data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        observacoes = request.form.get('observacoes', '')
        
        # Verificar se há estoque suficiente considerando a edição
        produto = Produto.query.get(produto_id)
        if produto:
            estoque_atual = produto.calcular_estoque_atual()
            
            # Se o produto mudou, calcular estoque sem adicionar quantidade antiga
            # Se o produto é o mesmo, adicionar a quantidade antiga de volta
            if int(produto_id) == saida.produto_id:
                estoque_disponivel = estoque_atual + saida.quantidade
            else:
                estoque_disponivel = estoque_atual
            
            if nova_quantidade > estoque_disponivel:
                flash(f'Estoque insuficiente! Disponível: {estoque_disponivel} {produto.formato}', 'error')
                produtos = Produto.query.all()
                return render_template('saida_form.html', produtos=produtos, saida=saida)
        
        saida.produto_id = produto_id
        saida.quantidade = nova_quantidade
        saida.data = data
        saida.observacoes = observacoes
        
        db.session.commit()
        flash('Saída atualizada com sucesso!', 'success')
        return redirect(url_for('saidas'))
    
    produtos = Produto.query.all()
    return render_template('saida_form.html', produtos=produtos, saida=saida)

@app.route('/saidas/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_saida(id):
    saida = Saida.query.get_or_404(id)
    db.session.delete(saida)
    db.session.commit()
    flash('Saída deletada com sucesso!', 'success')
    return redirect(url_for('saidas'))

@app.route('/relatorios')
@login_required
def relatorios():
    return render_template('relatorios.html')

@app.route('/relatorio/pdf')
@login_required
def gerar_relatorio_pdf():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    nome_engenheiro = request.args.get('nome_engenheiro', '')
    registro_engenheiro = request.args.get('registro_engenheiro', '')
    
    if not data_inicio or not data_fim:
        flash('Por favor, informe o período para o relatório', 'error')
        return redirect(url_for('relatorios'))
    
    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    
    # Criar PDF em memória
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Cabeçalho da empresa
    empresa_info = [
        "EMPRESA: JIQUIAGROPECUÁRIA",
        "ENDEREÇO: AV. PRESIDENTE VARGAS Nº 201",
        "CIDADE: JIQUIRIÇÁ - ESTADO: BAHIA",
        f"PERÍODO: {data_inicio.strftime('%d/%m/%Y')} até {data_fim.strftime('%d/%m/%Y')}",
        f"DATA DE EXTRAÇÃO: {date.today().strftime('%d/%m/%Y')}"
    ]
    
    for info in empresa_info:
        p = Paragraph(info, styles['Normal'])
        story.append(p)
    
    story.append(Spacer(1, 20))
    
    # Título do relatório
    titulo = Paragraph("RELATÓRIO DE CONTROLE DE ESTOQUE", styles['Title'])
    story.append(titulo)
    story.append(Spacer(1, 20))
    
    # Dados da tabela
    produtos = Produto.query.all()
    data = [['SKU', 'Produto', 'Estoque Inicial', 'Entradas', 'Saídas', 'Estoque Atual']]
    
    for produto in produtos:
        estoque_inicial = produto.calcular_estoque_atual(data_inicio)
        entradas_periodo = produto.calcular_entradas_periodo(data_inicio, data_fim)
        saidas_periodo = produto.calcular_saidas_periodo(data_inicio, data_fim)
        estoque_atual = produto.calcular_estoque_atual(data_fim)
        
        # Limitar nome do produto a 25 caracteres para evitar quebra
        nome_produto = produto.nome[:25] + "..." if len(produto.nome) > 25 else produto.nome
        
        data.append([
            produto.sku or 'N/A',
            nome_produto,
            f"{estoque_inicial:.1f}",
            f"{entradas_periodo:.1f}",
            f"{saidas_periodo:.1f}",
            f"{estoque_atual:.1f}"
        ])
    
    # Criar tabela com larguras específicas para responsividade
    col_widths = [60, 120, 70, 60, 60, 70]  # Larguras em pontos
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Nome do produto à esquerda
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 50))
    
    # Assinatura com informações do engenheiro agrônomo
    if nome_engenheiro or registro_engenheiro:
        if nome_engenheiro and registro_engenheiro:
            assinatura_texto = f"_________________________________<br/>{nome_engenheiro}<br/>Engenheiro Agrônomo - {registro_engenheiro}<br/>Responsável Técnico"
        elif nome_engenheiro:
            assinatura_texto = f"_________________________________<br/>{nome_engenheiro}<br/>Engenheiro Agrônomo<br/>Responsável Técnico"
        else:
            assinatura_texto = f"_________________________________<br/>Engenheiro Agrônomo - {registro_engenheiro}<br/>Responsável Técnico"
    else:
        assinatura_texto = "_________________________________<br/>Assinatura do Responsável Técnico"
    
    assinatura = Paragraph(assinatura_texto, styles['Normal'])
    story.append(assinatura)
    
    # Construir PDF
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'relatorio_estoque_{data_inicio.strftime("%Y%m%d")}_{data_fim.strftime("%Y%m%d")}.pdf',
        mimetype='application/pdf'
    )

def create_app():
    """Application factory for deployment"""
    with app.app_context():
        db.create_all()
    return app

if __name__ == '__main__':
    # Development mode only - for production use gunicorn
    port = int(os.environ.get('PORT', 5000))
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=port, debug=False)