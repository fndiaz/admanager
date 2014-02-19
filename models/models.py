#gravacao_lg = db.define_table("gravacao_lg",
#      Field("datetime"),
#      Field("acao"),
#      Field("pastas"))

if not "post" in db.tables:
	db.define_table('post',
		Field("titulo", "string", length=128, default=""),
		Field("conteudo", "text", length=512, default=""),
		Field("criado", "date", default=None)
		)

if not db(db.post).count():
	from gluon.contrib.populate import populate
	populate(db.post,49)

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
	Field("tipo_chamada", "string", length="30"),
	Field("expressao", "string", length="30"),
	Field("destino", "string", length="30"),
	Field("tamanho_max", "integer"),
	format="%(tipo_chamada)s",
	migrate=False
	)

db.define_table('f_empresa',
	Field("id"),
	Field("empresa"),
	Field("faixa_ramal"),
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

db.define_table('f_rotas',
	Field("id"),
	Field("rota", "string", length="30"),
	Field("id_tronco", db.f_troncos),
	Field("prioridade", "integer"),
	Field("id_destino", db.f_destinos),
	Field("exclui_antes", "integer"),
	Field("adiciona_antes", "string"),
	Field("adiciona_depois", "string"),
	Field("id_empresa", db.f_empresa),
	Field("id_tarifacao", db.f_tarifacao),
	format="%(rota)s",
	migrate=False
	)

db.define_table('f_menu',
	Field("id"),
	Field("nome"),
	Field("icone"),
	Field("funcao"),
	Field("ordem", "integer"),
	Field("submenu", "boolean", default=False),
	format="%(nome)s",
	migrate=False
	)

db.define_table('f_submenu',
	Field("id"),
	Field("menu_ref", db.f_menu),
	Field("nome"),
	Field("icone"),
	Field("ordem", "integer"),
	Field("funcao"),
	format="%(nome)s",
	migrate=False
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

