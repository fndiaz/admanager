##Controller parte funcional

######-TRONCOS
@auth.requires_login()  
def f_troncos():
	response.title = 'Troncos'
	editor = permissao()
	url = URL('admanager', 'funcional', 'f_troncos_form')
	print editor

	troncos = db(db.f_troncos).select(orderby=db.f_troncos.id)
	
	return response.render("funcional/show_troncos.html",  
					url=url, editor=editor, troncos=troncos)

@auth.requires(auth.has_membership('gerenciador') or auth.has_membership('administrador'))
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

	return response.render("funcional/form_troncos.html", form=form)

######-TRONCOS-FISICOS
@auth.requires_login()
def f_troncos_fisicos():
	response.title = 'Troncos Físicos'
	query 	=	(db.f_troncos.id == db.f_troncos_fisicos.id_tronco)
	editor 	= 	permissao()
	url = URL('admanager', 'funcional', 'f_troncos_fisicos_form')

	troncos_fisicos = db(query).select(db.f_troncos.tronco,
		db.f_troncos_fisicos.id, db.f_troncos_fisicos.dispositivo)	

	return response.render("funcional/show_troncos_fisicos.html", 
			url=url, editor=editor, troncos_fisicos=troncos_fisicos)

@auth.requires(auth.has_membership('gerenciador') or auth.has_membership('administrador'))
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

	return response.render("funcional/form_troncos_fisicos.html", 
													form=form)

######-DESTINOS
@auth.requires_login()
def f_destinos():
	response.title = 'Destinos'
	url = URL('admanager', 'funcional', 'f_destinos_form')
	editor 	= 	permissao()
	destinos 	= 	db(db.f_destinos).select(orderby=db.f_destinos.id)

	return response.render("funcional/show_destinos.html", 
				url=url, editor=editor, destinos=destinos)

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

	return response.render("funcional/form_destinos.html", form=form)

######-EMPRESA
@auth.requires_login()
def f_empresa():
	response.title = 'Empresa'
	editor 	= 	permissao()
	url 	=	URL('admanager', 'funcional', 'f_empresa_form')
	empresa	= 	db(db.f_empresa).select(orderby=db.f_empresa.id)

	return response.render("funcional/show_empresa.html", 
				url=url, editor=editor, empresa=empresa)

@auth.requires_login()
def f_empresa_form():
	response.title = 'Empresa'
	id_empresa	= 	request.vars['id_empresa']
	print id_empresa
	
	if id_empresa is None:
		form 	=	SQLFORM(db.f_empresa,  
				submit_button='Adicionar')
	else:
		form 	=	SQLFORM(db.f_empresa, id_empresa, 
								submit_button='Editar')

	form.element(_name='empresa')['_class'] = "form-control"
	#form.element(_name='faixa_ramal')['_class'] = "form-control"
	if form.process().accepted:
		redirect(URL('f_empresa'))

	return response.render("funcional/form_empresa.html", form=form)

######-TARIFACAO
@auth.requires_login()
def f_tarifacao():
	response.title = 'Tarifação'
	editor 	= 	permissao()
	url 	=	URL('admanager', 'funcional', 'f_tarifacao_form')
	tarifacao 	=	db(db.f_tarifacao).select(orderby=db.f_tarifacao.id)

	return response.render("funcional/show_tarifacao.html", 
				editor=editor, url=url, tarifacao=tarifacao)

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

	return response.render("funcional/form_tarifacao.html", form=form)

######-ROTAS
@auth.requires_login()
def f_rotas():
	response.title = 'Rotas'
	editor 	= 	permissao()
	url 	=	URL('admanager', 'funcional', 'f_rotas_form')
	rota = db(db.f_rotas).select()	 
	
	return response.render("funcional/show_rotas.html", 
						editor=editor, url=url, rota=rota)

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
	form.element(_name='id_horario')['_class'] = "form-control"
	form.element(_name='add_csp')['_class'] = "form-control"
	if form.process().accepted:
		redirect(URL('f_rotas'))

	return response.render("funcional/form_rotas.html", form=form)

######-HORARIO
@auth.requires_login()
def f_horario():
	response.title = 'Horário'
	editor 	= 	permissao()
	url 	=	URL('admanager', 'funcional', 'f_horario_form')
	horario = db(db.f_horario).select()
	
	return response.render("funcional/show_horario.html", 
					editor=editor, url=url, horario=horario)

@auth.requires_login()
def f_horario_form():
	response.title = 'Horário'
	id_rota 	= 	request.vars['id_horario']

	if id_horario is None:
		form 	=	SQLFORM(db.f_horario)
	else:
		form 	=	SQLFORM(db.f_rotas, id_horario)

	form.element(_name='dia_semana')['_class'] = "form-control"
	form.element(_name='horario')['_class'] = "form-control"
	form.element(_name='acao_negativa')['_class'] = "form-control"
	form.element(_name='descricao')['_class'] = "form-control"
	if form.process().accepted:
		redirect(URL('f_horario'))

	return response.render("funcional/form_rotas.html", form=form)

######-BILHETES-CHAMADAS
@auth.requires_login()
def f_bilhetes_chamadas():
	response.title = 'Bilhetes'
	editor 	= 	permissao()
	url 	=	URL('admanager', 'funcional', 'f_bilhetes_chamadas_form')
	query 	=  	(db.f_bilhetes_chamadas.id_tronco == db.f_troncos.id)&\
				(db.f_bilhetes_chamadas.id_empresa == db.f_empresa.id)&\
				(db.f_bilhetes_chamadas.id_destino == db.f_destinos.id)
	bilhetes = db(query).select()
	print bilhetes
	
	return response.render("funcional/show_bilhetes_chamadas.html", 
					editor=editor, url=url, bilhetes=bilhetes)

######-PARAMETROS
@auth.requires_login()
def f_parametros_form():
	response.title = 'Parâmetros'
	id_parametro=	request.vars['id_parametro']
	
	form 	=	SQLFORM(db.f_parametros, 1)
	
	form.element(_name='empresa')['_class'] = "form-control"
	form.element(_name='tempo_chamada_externa')['_class'] = "form-control"
	form.element(_name='tempo_chamada_interna')['_class'] = "form-control"
	form.element(_name='gravacao_geral')['_class'] = "form-control"
	form.element(_name='endereco_smtp')['_class'] = "form-control"
	form.element(_name='usuario_smtp')['_class'] = "form-control"
	form.element(_name='senha_smtp')['_class'] = "form-control"
	form.element(_name='ssl_smtp')['_class'] = "form-control"
	form.element(_name='porta_smtp')['_class'] = "form-control"
	form.element(_name='email_admin')['_class'] = "form-control"
	form.element(_name='faixa_ip_interna')['_class'] = "form-control"
	form.element(_name='faixa_ip_interna')['_rows'] = "4"
	form.element(_name='endereco_ip_externo')['_class'] = "form-control"
	form.element(_name='endereco_host_externo')['_class'] = "form-control"
	form.element(_name='toque_diferenciado')['_class'] = "form-control"
	form.element(_name='toque_diff_sipheader')['_class'] = "form-control"
	form.element(_name='spy_senha')['_class'] = "form-control"
	form.element(_name='spy_ramal_proibe_monitora')['_class'] = "form-control"
	form.element(_name='spy_ramal_proibe_monitora')['_rows'] = "4"
	form.element(_name='spy_ramal_espiao')['_class'] = "form-control"
	form.element(_name='spy_ramal_espiao')['_rows'] = "4"
	form.element(_name='tamanho_pin')['_class'] = "form-control"
	form.element(_name='fuso_horario')['_class'] = "form-control"
	form.element(_name='credito_dia')['_class'] = "form-control"
	form.element(_name='ura_antes_horario')['_class'] = "form-control"
	form.element(_name='bloqueio_chamadacobrar')['_class'] = "form-control"
	form.element(_name='tempo_chamada_transf')['_class'] = "form-control"
	form.element(_name='rechamada')['_class'] = "form-control"
	form.element(_name='pin_temporario')['_class'] = "form-control"

	if form.process().accepted:
		redirect(URL('f_parametros_form'))

	return response.render("funcional/form_parametros.html", form=form)