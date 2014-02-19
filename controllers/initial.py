# coding=UTF-8

@auth.requires_login()
def principal():
	response.title = 'Padrão'
	teste = 'sim'
	
	return response.render("initial/principal.html", teste=teste)

##--Parte de Login e Usuários--##
def user():
	#	#if request.args(0) == 'register':
	#  	db.auth_user.bio.writable = db.auth_user.bio.readable = False
	print request.args(0)
	if request.args(0) == 'not_authorized':
		redirect (URL('initial', 'not_authorized'))

	if request.args(0) == 'login':
		redirect(URL('initial', 'login'))
	return response.render("initial/user.html", user=auth())

def register():
	form = auth.register()
	form.element(_name='email')['_class'] = "form-control"
	form.element(_name='first_name')['_class'] = "form-control"
	form.element(_name='last_name')['_class'] = "form-control"
	form.element(_name='password')['_class'] = "form-control"
	form.element(_name='password_two')['_class'] = "form-control"

	return response.render("initial/register.html", form=form)

def profile():
	response.title = 'Profile'
	form = auth.profile()
	form.element(_name='email')['_class'] = "form-control"
	form.element(_name='first_name')['_class'] = "form-control"
	form.element(_name='last_name')['_class'] = "form-control"

	return response.render("initial/profile.html", form=form)

def not_authorized():
	return response.render("initial/not_authorized.html")

def change_password():
	response.title = 'Alterar Senha'
	form = auth.change_password()
	form.element(_name='old_password')['_class'] = "form-control"
	form.element(_name='new_password')['_class'] = "form-control"
	form.element(_name='new_password2')['_class'] = "form-control"

	return response.render("initial/change_password.html", form=form)

def request_reset_password():
	form = auth.request_reset_password()
	form.element(_name='email')['_class'] = "form-control"

	return response.render("initial/request_reset_password.html", form=form)

def login():
	form = auth.login()
	form.element(_name='email')['_class'] = "form-control"
	form.element(_name='password')['_class'] = "form-control"

	return response.render("initial/login.html", form=form)

def users():
	grid 	= SQLFORM.grid(db.auth_user, user_signature=False, _class="dataTables_wrapper form-inline")
	editor = permissao()
	usuarios= db(db.auth_user).select()
	#print usuarios
	
	return response.render("initial/show_usuarios.html", 
				grid=grid,	editor=editor, usuarios=usuarios)

def form_users():
	response.title = 'Usuários'
	id_usuario = request.vars['id_usuario']
	
	if id_usuario is None:
		form 	=	SQLFORM(db.auth_user,  
				submit_button='Adicionar')
	else:
		form 	=	SQLFORM(db.auth_user, id_usuario, 
								submit_button='Editar')

	form.element(_name='first_name')['_class'] = "form-control"
	form.element(_name='last_name')['_class'] = "form-control"
	form.element(_name='email')['_class'] = "form-control"
	form.element(_name='ramal')['_class'] = "form-control"
	form.element(_name='password')['_class'] = "form-control"

	if form.process().accepted:
		nome = request.vars['first_name']
		id_user = db(db.auth_user.first_name == nome).select(db.auth_user.id)
		redirect(URL(a='admanager', c='initial', f='f_permissao_menu_form', 
										vars=dict(id_usuario=id_user[0].id)))

	return response.render("initial/form_usuarios.html", 
													form=form)

def groups():
    grid = SQLFORM.grid(db.auth_group)
    return response.render("initial/show_grid.html", grid=grid)

def membership():
    grid = SQLFORM.grid(db.auth_membership)
    return response.render("initial/show_grid.html", grid=grid)

def log():
	form = auth.user
	return response.render("initial/log.html", form=form)
	
def download():
	return response.download(request, db)


##--Parte de Menus e Submenus--##
def f_menu():
	response.title = 'Menu'
	editor 	= 	permissao()
	menu 	= 	db(db.f_menu).select()

	return response.render("initial/show_menu.html", 
							editor=editor, menu=menu)

def f_menu_form():
	response.title 	= 	'Menu'
	id_menu			= 	request.vars['id_menu']
	testa 			=	True
	
	if id_menu is None:
		form 	=	SQLFORM(db.f_menu,  
				submit_button='Adicionar')
	else:
		testa 	= 	False
		form 	=	SQLFORM(db.f_menu, id_menu, 
								submit_button='Editar')
		form.element(_name='nome')['_readonly'] = "readonly"

	form.element(_name='nome')['_class'] = "form-control"
	form.element(_name='icone')['_class'] = "form-control"
	form.element(_name='funcao')['_class'] = "form-control"
	form.element(_name='ordem')['_class'] = "form-control"
	form.element(_name='submenu')['_class'] = "form-control"
	
	if form.process().accepted:
		if testa == True: 
			auth.add_group(request.vars['nome'], '')
		redirect(URL('f_menu'))

	return response.render("initial/form_menu.html", form=form)

def f_submenu():
	response.title = 'Submenu'
	editor 	= 	permissao()
	query 	= 	(db.f_menu.id == db.f_submenu.menu_ref)
	var	= 	db(query).select(orderby=db.f_submenu.menu_ref)

	return response.render("initial/show_submenu.html", 
								editor=editor, var=var)

def f_submenu_form():
	response.title 	= 	'Submenu'
	id_submenu		= 	request.vars['id_submenu']
	testa 			= 	True
	
	if id_submenu is None:
		form 	=	SQLFORM(db.f_submenu,  
				submit_button='Adicionar')
	else:
		testa 	=	False
		form 	=	SQLFORM(db.f_submenu, id_submenu, 
								submit_button='Editar')
		form.element(_name='nome')['_readonly'] = "readonly"

	form.element(_name='nome')['_class'] = "form-control"
	form.element(_name='menu_ref')['_class'] = "form-control"
	form.element(_name='icone')['_class'] = "form-control"
	form.element(_name='funcao')['_class'] = "form-control"
	form.element(_name='ordem')['_class'] = "form-control"
	
	if form.process().accepted:
		if testa == True: 
			auth.add_group(request.vars['nome'], '')
		redirect(URL('f_submenu'))

	return response.render("initial/form_submenu.html", form=form)

def f_permissao_menu_form():
	response.title = 'Permissao menu'
	id_usuario = request.vars['id_usuario']

	return response.render("initial/form_permissao_menu.html",
		id_usuario=id_usuario)

def insert_permissao_menu():
	id_usuario = request.vars['id_usuario']

	menu 	= 	db(db.f_menu).select()
	for dado in menu:
		query = (db.auth_group.role == dado.nome)
		id_grupo = db(query).select()
		id_grupo = id_grupo[0].id
		print id_grupo

		var = request.vars['%s' %(dado.nome)]
		if var == 'on':
			auth.add_membership(id_grupo, id_usuario)
		else:
			auth.del_membership(id_grupo, id_usuario)

	submenu = 	db(db.f_submenu).select()
	for dado in submenu:
		query = (db.auth_group.role == dado.nome)
		id_grupo = db(query).select()
		id_grupo = id_grupo[0].id
		print id_grupo

		var = request.vars['%s' %(dado.nome)]
		if var == 'on':
			auth.add_membership(id_grupo, id_usuario)
		else:
			auth.del_membership(id_grupo, id_usuario)
	redirect(URL('users'))


#def posts():
#	response.title += ' | Posts'
#	if not request.var.page:
#		redirect(URL(vars={'page':1}))
#	else:
#		page = int(request.vars.page)
#	start = (page-1)*10
#	end = page*10
#	posts = db(db.post).select(orderby=db.post.created_on, limitby=(start,end))
#	return response.render("initial/post.html", posts=posts)


def posts():
	response.title += ' | Posts'
	paginate=10
	if not request.vars.page:
		redirect(URL(vars={'page':1}))
	else:
		page = int(request.vars.page)
	start = (page-1)*paginate
	end = page*paginate
	registros = db(db.post).count()
	x=1
	if registros%paginate == 0:
		x=0
	posts = db(db.post).select(orderby=db.post.id, limitby=(start,end))
	return response.render("initial/post.html", posts=posts, end=end, 
					registros=registros, paginate=paginate, x=x)


##Parte de Troncos e rotas admanager
@auth.requires_login()  
def f_troncos():
	response.title = 'Troncos'
	grid 	= SQLFORM.grid(db.f_troncos)
	
	editor = permissao()
	#print editor
	troncos = db(db.f_troncos).select(orderby=db.f_troncos.id)
	
	return response.render("initial/show_troncos.html", grid=grid, 
									editor=editor, troncos=troncos)

@auth.requires_membership('gerenciador' or 'administrador')
def f_troncos_form():
	response.title = 'Troncos'
	id_tronco	= request.vars['id_tronco']
	
	if id_tronco is None:
		form 	=	SQLFORM(db.f_troncos,  
				submit_button='Adicionar')
	else:
		form 	=	SQLFORM(db.f_troncos, id_tronco, 
								submit_button='Editar')

	form.element(_name='tronco')['_class'] = "form-control"
	form.element(_name='dispositivo')['_class'] = "form-control"
	form.element(_name='chamadas_simultaneas')['_class'] = "form-control"
	form.element(_name='qtde_max_minutos')['_class'] = "form-control"
	form.element(_name='transbordo')['_class'] = "form-control"
	form.element(_name='csp')['_class'] = "form-control"
	form.element(_name='ddd')['_class'] = "form-control"
	form.element(_name='prefixo')['_class'] = "form-control"
	form.element(_name='chave')['_class'] = "form-control"
	form.element(_name='habilitado')['_class'] = "checkbox"
	form.element(_name='ciclo_conta')['_class'] = "form-control"
	#form.element(_name='ciclo_conta')['_value'] = "teste"
	if form.process().accepted:
		redirect(URL('f_troncos'))

	return response.render("initial/form_troncos.html", form=form)

@auth.requires_login()
def f_troncos_fisicos():
	response.title = 'Troncos Físicos'
	query 	=	(db.f_troncos.id == db.f_troncos_fisicos.id_tronco)
	editor 	= 	permissao()

	troncos_fisicos = db(query).select(db.f_troncos.tronco,
		db.f_troncos_fisicos.id, db.f_troncos_fisicos.dispositivo)	

	grid = SQLFORM.grid(db.f_troncos_fisicos)
	return response.render("initial/show_troncos_fisicos.html", 
		editor=editor, troncos_fisicos=troncos_fisicos, grid=grid)

@auth.requires_membership('gerenciador' or 'administrador')
def f_troncos_fisicos_form():
	response.title = 'Troncos Físicos'
	id_tronco_fisico = request.vars['id_tronco_fisico']
	
	if id_tronco_fisico is None:
		form 	=	SQLFORM(db.f_troncos_fisicos,  
				submit_button='Adicionar')
	else:
		form 	=	SQLFORM(db.f_troncos_fisicos, id_tronco_fisico, 
								submit_button='Editar')

	form.element(_name='id_tronco')['_class'] = "form-control"
	form.element(_name='dispositivo')['_class'] = "form-control"

	if form.process().accepted:
		redirect(URL('f_troncos_fisicos'))

	return response.render("initial/form_troncos_fisicos.html", 
													form=form)

@auth.requires_login()
def f_destinos():
	response.title = 'Destinos'
	destinos 	= 	db(db.f_destinos).select(orderby=db.f_destinos.id)
	editor 	= 	permissao()

	return response.render("initial/show_destinos.html", 
						editor=editor, destinos=destinos)

@auth.requires_login()
def f_destinos_form():
	response.title = 'Destinos'
	id_destino	= 	request.vars['id_destino']
	
	if id_destino is None:
		form 	=	SQLFORM(db.f_destinos,  
				submit_button='Adicionar')
	else:
		form 	=	SQLFORM(db.f_destinos, id_destino, 
								submit_button='Editar')

	form.element(_name='tipo_chamada')['_class'] = "form-control"
	form.element(_name='expressao')['_class'] = "form-control"
	form.element(_name='destino')['_class'] = "form-control"
	form.element(_name='tamanho_max')['_class'] = "form-control"
	if form.process().accepted:
		redirect(URL('f_destinos'))

	return response.render("initial/form_destinos.html", form=form)

@auth.requires_login()
def f_empresa():
	response.title = 'Empresa'
	empresa		= 	db(db.f_empresa).select(orderby=db.f_empresa.id)

	return response.render("initial/show_empresa.html", 
										empresa=empresa)

@auth.requires_login()
def f_empresa_form():
	response.title = 'Empresa'
	id_empresa	= 	request.vars['id_empresa']
	
	if id_empresa is None:
		form 	=	SQLFORM(db.f_empresa,  
				submit_button='Adicionar')
	else:
		form 	=	SQLFORM(db.f_empresa, id_empresa, 
								submit_button='Editar')

	form.element(_name='empresa')['_class'] = "form-control"
	form.element(_name='faixa_ramal')['_class'] = "form-control"
	if form.process().accepted:
		redirect(URL('f_empresa'))

	return response.render("initial/form_empresa.html", form=form)

@auth.requires_login()
def f_tarifacao():
	response.title = 'Tarifação'
	tarifacao 	=	db(db.f_tarifacao).select(orderby=db.f_tarifacao.id)

	return response.render("initial/show_tarifacao.html", 
										tarifacao=tarifacao)

@auth.requires_login()
def f_tarifacao_form():
	response.title = 'Tarifação'
	id_tarifacao=	request.vars['id_tarifacao']
	
	if id_tarifacao is None:
		form 	=	SQLFORM(db.f_tarifacao,  
				submit_button='Adicionar')
	else:
		form 	=	SQLFORM(db.f_tarifacao, id_tarifacao, 
								submit_button='Editar')

	form.element(_name='tarifacao')['_class'] = "form-control"
	form.element(_name='passo')['_class'] = "form-control"
	form.element(_name='valor')['_class'] = "form-control"
	if form.process().accepted:
		redirect(URL('f_tarifacao'))

	return response.render("initial/form_tarifacao.html", form=form)

@auth.requires_login()
def f_rotas():
	response.title = 'Rotas'
	grid 	= 	SQLFORM.grid(db.f_rotas)

	query 	=	(db.f_rotas.id_tronco == db.f_troncos.id)\
	& (db.f_rotas.id_destino == db.f_destinos.id)\
	& (db.f_rotas.id_empresa == db.f_empresa.id)\
	& (db.f_rotas.id_tarifacao == db.f_tarifacao.id)

	rota = db(query).select(db.f_rotas.id, 
		db.f_rotas.rota, db.f_troncos.tronco,
		db.f_rotas.prioridade, db.f_destinos.tipo_chamada,
		db.f_rotas.exclui_antes, db.f_rotas.adiciona_antes,
		db.f_rotas.adiciona_depois, db.f_empresa.empresa,
		db.f_tarifacao.tarifacao)
	#print rota 	 
	
	return response.render("initial/show_rotas.html", 
											rota=rota)

@auth.requires_login()
def f_rotas_form():
	response.title = 'Rotas'
	id_rota 	= 	request.vars['id_rota']

	if id_rota is None:
		form 	=	SQLFORM(db.f_rotas,  
				submit_button='Adicionar')
	else:
		form 	=	SQLFORM(db.f_rotas, id_rota, 
								submit_button='Editar')

	form.element(_name='rota')['_class'] = "form-control"
	form.element(_name='id_tronco')['_class'] = "form-control"
	form.element(_name='prioridade')['_class'] = "form-control"
	form.element(_name='id_destino')['_class'] = "form-control"
	form.element(_name='exclui_antes')['_class'] = "form-control"
	form.element(_name='adiciona_antes')['_class'] = "form-control"
	form.element(_name='adiciona_depois')['_class'] = "form-control"
	form.element(_name='id_empresa')['_class'] = "form-control"
	form.element(_name='id_tarifacao')['_class'] = "form-control"
	if form.process().accepted:
		redirect(URL('f_rota'))

	return response.render("initial/form_rotas.html", form=form)

##-- Extras --##
def permissao():
	#print session
	#print session.auth.user.first_name
	#print session.auth.user_groups[2]
	editor = 0
	for row in session.auth.user_groups:
		grupo = session.auth.user_groups[row]
		#print grupo
		if grupo == "gerenciador" or "administrador":
			editor = 1
	return editor

@auth.requires_login()
def delete():
	funcao 	=	request.vars['tabela']
	id_tab	=	request.vars['id_tab']
	if funcao 	== "f_troncos":
		tabela 	=	 db.f_troncos.id
	if funcao 	==	"f_troncos_fisicos":
		tabela 	= 	db.f_troncos_fisicos.id
	if funcao 	== "f_tarifacao":
		tabela 	= 	db.f_tarifacao.id
	if funcao 	== "f_rotas":
		tabela 	= 	db.f_rotas.id
	if funcao 	== 	"f_tarifacao":
		tabela 	=	db.f_tarifacao.id
	if funcao 	== 	"f_empresa":
		tabela 	= db.f_empresa.id
	if funcao 	== 	"f_destinos":
		tabela 	= 	db.f_destinos.id
	if funcao 	== 	"auth_user":
		tabela 	= 	db.auth_user.id
		funcao 	=	"users"
	if funcao 	== 	"f_menu": 
		delete_role(request.vars['nome'], request.vars['tipo'])
		#role	= 	request.vars['nome']
		#id_role	= 	db(db.auth_group.role == role).select(db.auth_group.id) 
		#auth.del_group(id_role[0].id)
		tabela 	= 	db.f_menu.id
	if funcao 	== 	"f_submenu":
		delete_role(request.vars['nome'], request.vars['tipo'])
		#role	= 	request.vars['nome']
		#id_role	= 	db(db.auth_group.role == role).select(db.auth_group.id) 
		#auth.del_group(id_role[0].id)
		tabela 	= 	db.f_submenu.id

	db(tabela == id_tab).delete()	
	redirect(URL(funcao))

def delete_role(nome, tipo):
	print 'entrou'
	print nome
	print tipo
	id_role	= 	db(db.auth_group.role == nome).select(db.auth_group.id)
	auth.del_group(id_role[0].id)
	if tipo == "menu":
		menu = db(db.f_menu.nome == nome).select()
		if menu[0].submenu == True:
			var = db(db.f_submenu.menu_ref == menu[0].id).select()
			for dado in var:
				print dado
				id_role	= db(db.auth_group.role == dado.nome).select(db.auth_group.id)
				print id_role
				auth.del_group(id_role[0])