# JIQUIAGROPECUÁRIA - Controle de Estoque

## Overview

Sistema completo de controle de estoque para a JIQUIAGROPECUÁRIA, empresa do setor agropecuário. O sistema permite gerenciar produtos com SKUs automáticos, rastrear entradas e saídas do estoque, monitorar níveis atuais de inventário e gerar relatórios PDF profissionais. Inclui autenticação segura, gestão completa de produtos com busca, controle abrangente de movimentações e relatórios personalizáveis com informações do engenheiro agrônomo responsável.

**Status**: ✅ SISTEMA COMPLETO E FUNCIONANDO

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 with Flask para renderização server-side
- **CSS Framework**: Tailwind CSS para design responsivo e estilização moderna
- **Icons**: Font Awesome para iconografia consistente
- **Layout Structure**: Template base com herança de blocos para navegação e marca consistentes
- **Mobile Support**: Design responsivo mobile-first com navegação lateral colapsável e overlay
- **Authentication**: Sistema de login integrado com proteção de rotas
- **User Interface**: Interface limpa sem logo, focada na funcionalidade

### Backend Architecture
- **Web Framework**: Flask com roteamento estruturado
- **ORM**: SQLAlchemy para operações de banco e relacionamentos
- **Data Models**: Três entidades principais (Produto, Entrada, Saida) com chaves estrangeiras
- **Business Logic**: Métodos de modelo para cálculo de estoque atual e movimentações por período
- **PDF Generation**: ReportLab para geração de relatórios responsivos com informações do engenheiro agrônomo
- **Authentication**: Sistema de sessão Flask com proteção @login_required em todas as rotas
- **Validação**: Sistema de validação de estoque antes de registrar saídas

### Data Storage
- **Database**: SQLite para persistência local de dados
- **Schema Design**: 
  - Tabela de produtos com SKU automático, nome, marca, formato/unidade
  - Tabelas de entradas e saídas vinculadas a produtos via chaves estrangeiras
  - Rastreamento de timestamps para todas as transações
  - Datas dinâmicas para registros corretos
- **Stock Calculation**: Cálculo dinâmico baseado no histórico de entradas/saídas

### Key Features Implemented
- **Authentication System**: ✅ Login seguro com credenciais igor/igor2025 e proteção de rotas
- **Product Management**: ✅ CRUD completo com SKUs automáticos (PRD0001...) e busca
- **Stock Movements**: ✅ Rastreamento de entradas e saídas com validação de estoque
- **Responsive Design**: ✅ Menu móvel colapsável que não sobrepõe o conteúdo
- **Professional Reporting**: ✅ PDFs responsivos com campos editáveis para engenheiro agrônomo
- **Stock Validation**: ✅ Verificação de estoque antes de registrar saídas
- **User Management**: ✅ Informações do usuário logado e logout no menu lateral

### Recent Changes
- **23/09/2025 - Final Update**: Todas as melhorias implementadas e testadas
- **Authentication**: Sistema de login completo com proteção de rotas e sessões Flask
- **Mobile Responsive**: Menu lateral corrigido para recolher sem sobrepor conteúdo
- **PDF Reports**: Rodapé editável para engenheiro agrônomo, logo removida
- **Product SKUs**: Códigos automáticos PRD0001 implementados
- **User Interface**: Interface limpa focada na funcionalidade sem elementos visuais desnecessários

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
- **Login Credentials**: Sistema configurado com usuário 'igor' e senha 'igor2025'

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
    ├── base.html         # Template base com navegação responsiva e login
    ├── login.html        # Página de autenticação
    ├── produtos.html     # Listagem de produtos com SKUs
    ├── produto_form.html # Formulário de produtos
    ├── entradas.html     # Listagem de entradas
    ├── entrada_form.html # Formulário de entradas
    ├── saidas.html       # Listagem de saídas
    ├── saida_form.html   # Formulário de saídas
    └── relatorios.html   # Página de relatórios com campos do engenheiro
```