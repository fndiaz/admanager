#gravacao_lg = db.define_table("gravacao_lg",
#      Field("datetime"),
#      Field("acao"),
#      Field("pastas"))


db.define_table('f_troncos',
	Field("id"),
	Field("tronco", "string", length="20"),
	Field("dispositivo", "string", length="30"),
	Field("chamadas_simultaneas", "integer"),
	Field("qtde_max_minutos", "integer"),
	Field("transbordo", "integer"),
	Field("csp", "integer"),
	Field("ddd", "integer"),
	Field("prefixo", "integer"),
	Field("chave", "integer"),
	Field("habilitado", "boolean"),
	Field("ciclo_conta", "integer"),
	Field("ramal_principal", "string", length="10"),
	Field("ura", "boolean"),
	Field("add_zero", "boolean"),
	format="%(tronco)s",
	migrate=False
	)

db.define_table('f_troncos_fisicos',
	Field("id"),
	Field("id_tronco", db.f_troncos),
	Field("dispositivo", "string", length="30"),
	migrate=False
	)

db.define_table('f_destinos',
	Field("id"),
	Field("tipo_chamada", "string"),
	Field("expressao", "string"),
	Field("destino", "string"),
	Field("tamanho_max", "integer"),
	Field("tarifado", "boolean"),
	format="%(tipo_chamada)s",
	migrate=False
	)

db.define_table('f_empresa',
	Field("id"),
	Field("empresa"),
	####Field("faixa_ramal"),
	format="%(empresa)s",
	migrate=False
	)

db.define_table('f_tarifacao',
	Field("id"),
	Field("tarifacao", "string", length="30"),
	Field("passo", "string", length="30"),
	Field("valor", "double"),
	format="%(tarifacao)s",
	migrate=False
	)

db.define_table("f_horario",
    Field("id"),
    Field("dia_semana", "string", length="30"),
    Field("horario"),
    Field("acao_negativa", "string", length="100"),
    Field("descricao", "string", length="50"),
    format="%(horario)s",
    migrate=False)

db.define_table('f_rotas',
	Field("id"),
	Field("rota", "string", length="1"),
	Field("id_tronco", db.f_troncos),
	Field("prioridade", "integer"),
	Field("id_destino", "list:reference db.f_destinos"),
	Field("exclui_antes", "integer"),
	Field("adiciona_antes", "string"),
	Field("adiciona_depois", "string"),
	Field("id_empresa", "list:reference db.f_empresa"),
	Field("id_tarifacao", db.f_tarifacao),
	Field("id_horario", db.f_horario),
	Field("add_csp", "boolean"),
	format="%(rota)s",
	migrate=True
	)

db.define_table("f_parametros",
    Field("empresa", "string", length="100"),
    Field("tempo_chamada_externa", "integer"),
    Field("tempo_chamada_interna", "integer"),
    Field("gravacao_geral", "boolean"),
    Field("endereco_smtp", "string", length="100"),
    Field("usuario_smtp", "string", length="100"),
    Field("senha_smtp", "string", length="100"),
    Field("porta_smtp", "integer", default=0),
    Field("ssl_smtp", "boolean"),
    Field("email_admin", "string", length="100"),
    Field("faixa_ip_interna", "text"),
    Field("endereco_ip_externo", "string", length="20"),
    Field("endereco_host_externo", "string", length="100"),
    Field("toque_diferenciado", "boolean"),
    Field("toque_diff_sipheader", "string", length="100"),
    Field("spy_senha", "string", length="4"),
	Field("spy_ramal_proibe_monitora", "text"),
	Field("spy_ramal_espiao", "text"),
    Field("tamanho_pin", "integer", default=0),
    Field("fuso_horario", "string", length="3"),
	Field("credito_dia", "string", length="2"),
	Field("ura_antes_horario", "boolean"),
	Field("bloqueio_chamadacobrar", "boolean"),
	Field("tempo_chamada_transf", "integer"),
	Field("rechamada", "boolean"),
	Field("pin_temporario", "string", length="4"),
    format="%(empresa)s",
    migrate=False)

db.define_table("f_bilhetes_chamadas",
	Field("id_tronco", db.f_troncos),
	Field("origem"),
	Field("destino"),
	Field("linked_id"),
	Field("horario", "datetime"),
	Field("status"),
	Field("tarifacao", "double"),
	Field("tempo", "integer"),
	Field("id_empresa", db.f_empresa),
	Field("id_destino", db.f_destinos),
	Field("gravacao", "boolean"),
	Field("atendido", "string", length="10"),
	Field("nome_origem", "string", length="20"),
	Field("departamento", "string", length="50"),
	Field("transbordo", "string", length="5"),
    format="%(origem)s",
    migrate=False)


####--Menus Permissões
db.define_table('f_menu',
	Field("id"),
	Field("nome"),
	Field("icone"),
	Field("funcao"),
	Field("controller"),
	Field("ordem", "integer"),
	Field("submenu", "boolean", default=False),
	format="%(nome)s"
	#migrate=False
	)

db.define_table('f_submenu',
	Field("id"),
	Field("menu_ref", db.f_menu),
	Field("nome"),
	Field("icone"),
	Field("ordem", "integer"),
	Field("funcao"),
	format="%(nome)s"#
	#migrate=False
	)

db.define_table('f_permissao_menu',
	Field("id_user"),
	Field("menu", "boolean"),
	Field("submenu", "boolean"),
	#migrate=False
	)

db.define_table('f_permissao_menu2',
	Field("id_user", db.auth_user),
	Field("id_menu", db.f_menu),
	Field("id_submenu", db.f_submenu),
	Field("permissao", "boolean")
	)

if db(db.auth_group.role == 'administrador').isempty():
	db.auth_group.insert(role="administrador", description="admin do sistema")
if db(db.auth_group.role == 'gerenciador').isempty():
	db.auth_group.insert(role="gerenciador", description="gerenciador cliente")
if db(db.auth_group.role == 'comum').isempty():
	db.auth_group.insert(role="comum", description="usuario leitura")

if db(db.auth_user.email == 'root@forip.com.br').isempty():
	##Inserindo user root
	root = db.auth_user.insert(first_name="root",last_name="root",\
	email="root@forip.com.br", ramal="0000",\
	password=db.auth_user.password.validate("root123")[0])
	##Inserindo permissão de administrador
	group_admin = db(db.auth_group.role == 'administrador').select()
	auth.add_membership(group_admin[0].id, root)

if db(db.f_menu).isempty():
	db.f_menu.insert(nome="Menu", funcao="f_menu", icone="icon-list-alt", ordem="1", submenu=False)
	auth.add_group('Menu', '')
	db.f_menu.insert(nome="Submenu", funcao="f_submenu", icone="icon-list-alt", ordem="2", submenu=False)
	auth.add_group('Submenu', '')
	db.f_menu.insert(nome="Acessos", funcao="", icone="icon-list-alt", ordem="3", submenu=True)
	auth.add_group('Acessos', '')
	db.f_menu.insert(nome="Troncos", funcao="f_troncos", icone="icon-list-alt", ordem="4", submenu=False)
	auth.add_group('Troncos', '')
	db.commit()

if db(db.f_submenu).isempty():
	id_acessos = db(db.f_menu.nome == 'Acessos').select()[0].id
	db.f_submenu.insert(nome="Usuários", funcao="users", icone="icon-chevron-right", ordem="1", menu_ref=id_acessos)
	auth.add_group('Usuários', '')
	db.f_submenu.insert(nome="Grupos", funcao="groups", icone="icon-chevron-right", ordem="2", menu_ref=id_acessos)
	auth.add_group('Grupos', '')
	db.f_submenu.insert(nome="Permissões", funcao="membership", icone="icon-chevron-right", ordem="3", menu_ref=id_acessos)
	auth.add_group('Permissões', '')
	


