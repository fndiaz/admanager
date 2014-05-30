##Extras

def permissao():
	editor = False
	for row in session.auth.user_groups:
		grupo = session.auth.user_groups[row]
		if (grupo == "gerenciador") or (grupo == "administrador"):
			editor = True
	return editor