# JIQUIAGROPECUÁRIA - Controle de Estoque

## Overview

Sistema completo de controle de estoque para a JIQUIAGROPECUÁRIA, empresa do setor agropecuário. O sistema permite gerenciar produtos, rastrear entradas e saídas do estoque, monitorar níveis atuais de inventário e gerar relatórios PDF profissionais. Inclui dashboard com métricas em tempo real, gestão completa de produtos com busca, e controle abrangente de movimentações com filtros por data e relatórios detalhados.

**Status**: ✅ SISTEMA COMPLETO E FUNCIONANDO

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 with Flask para renderização server-side
- **CSS Framework**: Tailwind CSS para design responsivo e estilização moderna
- **Icons**: Font Awesome para iconografia consistente
- **Layout Structure**: Template base com herança de blocos para navegação e marca consistentes
- **Mobile Support**: Design responsivo mobile-first com navegação lateral colapsável
- **Logo da Empresa**: Integrado no cabeçalho e relatórios PDF

### Backend Architecture
- **Web Framework**: Flask com roteamento estruturado
- **ORM**: SQLAlchemy para operações de banco e relacionamentos
- **Data Models**: Três entidades principais (Produto, Entrada, Saida) com chaves estrangeiras
- **Business Logic**: Métodos de modelo para cálculo de estoque atual e movimentações por período
- **PDF Generation**: ReportLab para geração de relatórios com tabelas e marca da empresa
- **Validação**: Sistema de validação de estoque antes de registrar saídas

### Data Storage
- **Database**: SQLite para persistência local de dados
- **Schema Design**: 
  - Tabela de produtos com nome, marca, formato/unidade
  - Tabelas de entradas e saídas vinculadas a produtos via chaves estrangeiras
  - Rastreamento de timestamps para todas as transações
  - Datas dinâmicas para registros corretos
- **Stock Calculation**: Cálculo dinâmico baseado no histórico de entradas/saídas

### Key Features Implemented
- **Dashboard**: ✅ Métricas em tempo real (total produtos, entradas/saídas diárias, estoque baixo)
- **Product Management**: ✅ CRUD completo com busca por nome e marca
- **Stock Movements**: ✅ Rastreamento de entradas e saídas com data e observações
- **Reporting**: ✅ Geração de PDF com filtro por período e análise detalhada
- **Responsive Design**: ✅ Abordagem mobile-first com barra lateral colapsável
- **Logo Integration**: ✅ Logo da JIQUIAGROPECUÁRIA em interfaces e relatórios
- **Stock Validation**: ✅ Verificação de estoque antes de registrar saídas

### Recent Changes
- **23/09/2025**: Sistema completo implementado e testado
- **Database Models**: Corrigidos defaults de data para uso dinâmico
- **PDF Reports**: Implementado com cabeçalho da empresa e logo
- **Interface**: Sistema responsivo completo com TailwindCSS
- **Validation**: Sistema de validação de estoque implementado

## External Dependencies

### Python Libraries
- **Flask**: Framework de aplicação web e roteamento
- **SQLAlchemy/Flask-SQLAlchemy**: ORM para gerenciamento de banco de dados
- **ReportLab**: Geração de documentos PDF com formatação
- **Pillow**: Processamento de imagens para o logo
- **Jinja2**: Motor de templates (incluído no Flask)

### Frontend Libraries
- **Tailwind CSS**: Framework CSS utility-first via CDN
- **Font Awesome**: Biblioteca de ícones para elementos UI via CDN

### Database
- **SQLite**: Banco de dados embarcado para persistência (arquivo: estoque.db)

### Environment Configuration
- **SESSION_SECRET**: Variável de ambiente para segurança da sessão Flask
- **Database URI**: Caminho configurável do banco SQLite
- **Logo**: Armazenado em static/img/logo.jpeg

## Project Structure

```
/
├── app.py                 # Aplicação Flask principal
├── models.py              # Modelos de banco de dados
├── estoque.db            # Banco de dados SQLite (criado automaticamente)
├── static/
│   ├── css/              # Estilos customizados (se necessário)
│   ├── js/               # Scripts JavaScript (se necessário)
│   └── img/
│       └── logo.jpeg     # Logo da empresa
└── templates/
    ├── base.html         # Template base com navegação
    ├── dashboard.html    # Dashboard principal
    ├── produtos.html     # Listagem de produtos
    ├── produto_form.html # Formulário de produtos
    ├── entradas.html     # Listagem de entradas
    ├── entrada_form.html # Formulário de entradas
    ├── saidas.html       # Listagem de saídas
    ├── saida_form.html   # Formulário de saídas
    └── relatorios.html   # Página de relatórios
```