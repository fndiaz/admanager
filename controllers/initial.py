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
	print 'user'
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
	print 'login'
	form = auth.login()
	form.element(_name='email')['_class'] = "form-control"
	form.element(_name='password')['_class'] = "form-control"

	return response.render("initial/login.html", form=form)

def users():
	grid 	= SQLFORM.grid(db.auth_user, user_signature=False, _class="dataTables_wrapper form-inline")
	editor = permissao()
	usuarios= db(db.auth_user).select()
	logger.debug("acesso a usuarios")
	
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
	form.element(_name='controller')['_class'] = "form-control"
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
	check_ger = ""

	if auth.has_membership('gerenciador', id_usuario):
		check_ger = "checked"

	return response.render("initial/form_permissao_menu.html",
		id_usuario=id_usuario, check_ger=check_ger)

def insert_permissao_menu():
	print request.vars
	id_usuario = request.vars['id_usuario']

	if request.vars.gerenciador == 'on':
		print 'adicionando gerenciador'
		auth.add_membership(auth.id_group('gerenciador'), id_usuario)
		auth.del_membership(auth.id_group('comum'), id_usuario)
	else:
		print 'del gerenciador'
		auth.del_membership(auth.id_group('gerenciador'), id_usuario)
		auth.add_membership(auth.id_group('comum'), id_usuario)

	menu 	= 	db(db.f_menu).select()
	##Faz o loop retornando menus
	for dado in menu:
		query = (db.auth_group.role == dado.nome)
		id_grupo = db(query).select()
		id_grupo = id_grupo[0].id
		print id_grupo

		##verifica se menu está ticado e adiciona no membership
		var = request.vars['%s' %(dado.nome)]
		if var == 'on':
			auth.add_membership(id_grupo, id_usuario)
		else:
			auth.del_membership(id_grupo, id_usuario)

	##Faz o loop retornando submenus
	submenu = 	db(db.f_submenu).select()
	for dado in submenu:
		query = (db.auth_group.role == dado.nome)
		id_grupo = db(query).select()
		id_grupo = id_grupo[0].id
		#print id_grupo

		##verifica se submenu está ticado e adiciona no membership
		var = request.vars['%s' %(dado.nome)]
		if var == 'on':
			auth.add_membership(id_grupo, id_usuario)
		else:
			auth.del_membership(id_grupo, id_usuario)
	redirect(URL('users'))


##-- Extras --##
def permissao():
	editor = False
	for row in session.auth.user_groups:
		grupo = session.auth.user_groups[row]
		if (grupo == "gerenciador") or (grupo == "administrador"):
			editor = True
	return editor

@auth.requires_login()
def delete():
	print request.vars
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