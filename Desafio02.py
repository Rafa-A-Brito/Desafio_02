from customtkinter import *
from tkinter import *
from tkinter import messagebox
import sqlite3 as ra
from PIL import Image
# Configurações iniciais
azul = '#4aaced'

jan = CTk()
jan.title('Sistema de Cadastro e CRUD')
jan.iconbitmap("conta.ico")
jan.geometry('750x500')
jan.configure(fg_color=azul)
jan.resizable(False, False)

# Criando o Tabview para as diferentes abas de operação
tabview = CTkTabview(
   jan,
   height=700,
   width=700,
   corner_radius=10,
   fg_color='silver',
   segmented_button_fg_color='#010152',
   segmented_button_selected_color='dark blue'
)
tabview.pack(pady=10)

# Adicionando abas
tabview.add("Cadastro do Usuário")
tabview.add("Consulta")
tabview.add("Atualização")
tabview.add("Excluir/Apagar")


msg_font=CTkFont(family='Arial', size=18, weight='bold')
msg2_font=CTkFont(family='Arial', size=12, slant='italic')
nome_font=CTkFont(family='Arial', size=12, weight='bold')
sobr_font=CTkFont(family='Arial', size=12, weight='bold')
rg_font=CTkFont(family='Arial', size=12, weight='bold')
tel_font=CTkFont(family='Arial', size=12, weight='bold')
rua_font=CTkFont(family='Arial', size=12, weight='bold')
num_font=CTkFont(family='Arial', size=12, weight='bold')
bairro_font=CTkFont(family='Arial', size=12, weight='bold')


# Adicionando a imagem
img = CTkImage(light_image=Image.open('img_cad.png'), dark_image=Image.open('img_cad.png'), size=(500,248))
figura = CTkLabel(master=tabview.tab('Cadastro do Usuário'),text='',image=img)
figura.place(x=280,y=100)


lb_msg = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='Seja Bem-vindo(a) ao Cadastro', font=msg_font)
lb_msg.place(x=215, y=0)


lb_msg2 = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='Realize o cadastro abaixo!', font=msg2_font)
lb_msg2.place(x=270, y=20)


# Campos de entrada na aba "Cadastro do Usuário"
lb_nome = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='Nome', font=nome_font)
lb_nome.place(x=40, y=35)
ent_nome = CTkEntry(master=tabview.tab('Cadastro do Usuário'), width=150, placeholder_text='Digite seu nome')
ent_nome.place(x=40, y=60)


lb_sobrenome = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='Sobrenome', font=sobr_font)
lb_sobrenome.place(x=40, y=90)
ent_sobrenome = CTkEntry(master=tabview.tab('Cadastro do Usuário'), width=150, placeholder_text='Digite seu sobrenome')
ent_sobrenome.place(x=40, y=115)


lb_rg = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='RG', font=rg_font)
lb_rg.place(x=40, y=150)
ent_rg = CTkEntry(master=tabview.tab('Cadastro do Usuário'), width=150, placeholder_text='Informe seu RG')
ent_rg.place(x=40, y=175)


def aplicar_mascara(event):
   numero_tel = ent_telefone.get().replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
  
   # Limita o tamanho do número para 11 dígitos
   if len(numero_tel) > 11:
       numero_tel= numero_tel[:11]


   # Aplica o formato de telefone
   if len(numero_tel) > 6:
       numero_formatado = f"({numero_tel[:2]}) {numero_tel[2:7]}-{numero_tel[7:]}"
   elif len(numero_tel) > 2:
       numero_formatado = f"({numero_tel[:2]}) {numero_tel[2:]}"
   else:
       numero_formatado = f"({numero_tel}"

   # Atualiza o campo de entrada com o número formatado
   ent_telefone.delete(0, 'end')
   ent_telefone.insert(0, numero_formatado)

def verifica_numeros(event):
   # Pega o conteúdo atual da entrada
   conteudo = ent_telefone.get()
   # Filtra e deixa apenas os dígitos
   novo_conteudo = ''.join(filter(str.isdigit, conteudo))
   # Atualiza o campo com apenas os números
   ent_telefone.delete(0, 'end')
   ent_telefone.insert(0, novo_conteudo)

def juncao(event):
   verifica_numeros(event)
   aplicar_mascara(event)
  
lb_telefone = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='Telefone', font=tel_font)
lb_telefone.place(x=40, y=210)
ent_telefone = CTkEntry(master=tabview.tab('Cadastro do Usuário'), width=150, placeholder_text='Digite seu telefone')
ent_telefone.place(x=40, y=235)

#Vincula o evento de digitação ao campo de entrada
ent_telefone.bind("<KeyRelease>", juncao)

lb_rua = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='Rua', font=rua_font)
lb_rua.place(x=40, y=265)
ent_rua = CTkEntry(master=tabview.tab('Cadastro do Usuário'), width=150, placeholder_text='Digite a sua rua')
ent_rua.place(x=40, y=290)

lb_num = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='Número', font=num_font)
lb_num.place(x=215, y=35)
ent_num = CTkEntry(master=tabview.tab('Cadastro do Usuário'), width=110, placeholder_text='Digite o número')
ent_num.place(x=215, y=60)

lb_bairro = CTkLabel(master=tabview.tab('Cadastro do Usuário'), text='Bairro', font=bairro_font)
lb_bairro.place(x=215, y=90)
ent_bairro = CTkEntry(master=tabview.tab('Cadastro do Usuário'), width=150, placeholder_text='Digite o seu bairro')
ent_bairro.place(x=215, y=115)

# Função para conectar ao banco de dados e criar a tabela
def conectar():
   tab_morador = '''
       CREATE TABLE IF NOT EXISTS morador(
       ID_morador INTEGER PRIMARY KEY AUTOINCREMENT,
       RG VARCHAR(12) NOT NULL,
       Nome_morador VARCHAR(30) NOT NULL,
       Sobrenome_morador VARCHAR(40),
       Telefone VARCHAR(12),
       Rua VARCHAR(40),
       Numero INTEGER,
       Bairro VARCHAR(25)
       );
   '''
   try:
       conexao = ra.connect('cadastro.db')
       cursor = conexao.cursor()
       cursor.execute(tab_morador)
       conexao.commit()
       return conexao  # Retorna a conexão ativa


   except ra.DatabaseError as e:
       print('Erro no banco de dados!!', e)
       return None  # Retorna None em caso de erro


# Função para cadastrar morador com dados dos campos
def inserir_dados():
   conectar()
   rg = ent_rg.get()
   nome = ent_nome.get()
   sobrenome = ent_sobrenome.get()
   telefone = ent_telefone.get()
   rua = ent_rua.get()
   numero = ent_num.get()
   bairro = ent_bairro.get()
  
   # Verifica se todos os campos estão preenchidos
   if not all([rg, nome, sobrenome, telefone, rua, numero, bairro]):
       messagebox.showerror("Cadastro", "Por favor, preencha todos os campos!")
       return None
   #Converte string para int
   try:
       numero = int(ent_num.get())
   except ValueError:
       messagebox.showerror("Cadastro", "O campo 'Número' deve ser preenchido com um valor inteiro!")
       return
  
   try:
       conexao = ra.connect('cadastro.db')
       cursor = conexao.cursor()
       cursor.execute('''INSERT INTO morador (RG, Nome_morador, Sobrenome_morador, Telefone, Rua, Numero, Bairro)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''', (rg, nome, sobrenome, telefone, rua, numero, bairro))
       conexao.commit()
       messagebox.showinfo("Cadastro", "Morador cadastrado com sucesso!")
   except ra.DatabaseError as e:
       messagebox.showerror("Erro no banco de dados", e)
   finally:
       if conexao:
           conexao.close()
  
   limpar_campos()

# Função para limpar os campos de entrada
def limpar_campos():
   ent_rg.delete(0,'end')
   ent_rg.configure(placeholder_text='Informe seu RG')


   ent_nome.configure(placeholder_text='Digite seu nome')
   ent_nome.delete(0,'end')


   ent_sobrenome.delete(0,'end')
   ent_sobrenome.configure(placeholder_text='Digite seu sobrenome')


   ent_telefone.delete(0,'end')
   ent_telefone.configure(placeholder_text='Digite seu telefone')


   ent_rua.delete(0,'end')
   ent_rua.configure(placeholder_text='Digite a sua rua')


   ent_num.delete(0,'end')
   ent_num.configure(placeholder_text='Digite o número')
  
   ent_bairro.delete(0,'end')
   ent_bairro.configure(placeholder_text='Digite o seu bairro')


# Chamar a função para criar a tabela ao iniciar a aplicação
conectar()
botao_env = CTkButton(master=tabview.tab('Cadastro do Usuário'),
       text='Enviar Dados',
       border_width=2,
       border_color='dark blue',
       corner_radius=10,
       font=('Arial', 14),
       command=inserir_dados)


#Botão que realiza o envia de dados
botao_env.place(x=235, y=350)


def mostrar(event):
   if ent_sql_cons.get():  # Verifica se a Entry foi preenchida
       lb_sql_opc2.place(x=40, y=100)
       lb_sql_cons2.place(x=350, y=100)
       ent_sql.place(x=340, y=130)
       box_cons2.place(x=40, y=130)
#Fonte da label SQL
sql_font = CTkFont(family='Arial', size=14, weight='bold')


#Declaração das características de cada aba da janela
lb_sql_msg = CTkLabel(master=tabview.tab('Consulta'), text='Faça a sua consulta!', font=sql_font)
lb_sql_msg.place(x=235, y=0)


lb_sql_opc = CTkLabel(master=tabview.tab('Consulta'), text='Opções:', font=sql_font)
lb_sql_opc.place(x=40, y=30)


lb_sql_opc2 = CTkLabel(master=tabview.tab('Consulta'), text='Mais Opções:', font=sql_font)
lb_sql_opc2.place_forget()


lb_sql_cons = CTkLabel(master=tabview.tab('Consulta'), text='Consulta:', font=sql_font)
lb_sql_cons.place(x=350, y=30)


lb_sql_cons2 = CTkLabel(master=tabview.tab('Consulta'), text='Outra Consulta:', font=sql_font)
lb_sql_cons2.place_forget()


ent_sql_cons= CTkEntry(master=tabview.tab('Consulta'), width=300, placeholder_text='Selecione alguma das escolhas ao lado')
ent_sql_cons.place(x=340, y=60)


ent_sql_cons.bind("<KeyRelease>", mostrar)


ent_sql = CTkEntry(master=tabview.tab('Consulta'), width=300, placeholder_text='Entre com uma segunda escolha(opcional)')
ent_sql.place_forget()


atr_cons = ['Selecione algum dos campos abaixo: ...', 'ID_morador', 'RG', 'Nome_morador',
           'Sobrenome_morador', 'Telefone', 'Rua', 'Número', 'Bairro', 'Tudo']


atr_cons2 = ['Selecione outro campo (opcional): ...', 'ID_morador', 'RG', 'Nome_morador',
           'Sobrenome_morador', 'Telefone', 'Rua', 'Número', 'Bairro']

def selec_cons(*args):
   ent_sql_cons.configure(state='normal')
   print("Evento disparado!")
   print(f"Item selecionado: {box_cons.get()}")


   if box_cons.get() == 'Selecione algum dos campos abaixo: ...':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Selecione alguma das escolhas ao lado')
   elif box_cons.get() == 'ID_morador':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Informe o ID do morador escolhido')
   elif box_cons.get() == 'RG':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Informe o RG escolhido')
   elif box_cons.get() == 'Nome_morador':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Informe o nome do morador escolhido')
   elif box_cons.get() == 'Sobrenome_morador':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Informe o sobrenome do morador escolhido')
   elif box_cons.get() == 'Telefone':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Informe o telefone escolhido')
   elif box_cons.get() == 'Número':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Informe o número do domicílio escolhido')
   elif box_cons.get() == 'Rua':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Informe a rua do domicílio escolhido')
   elif box_cons.get() == 'Bairro':
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Informe o bairro do domicílio escolhido')
   else:
       ent_sql_cons.delete(0,'end')
       ent_sql_cons.configure(placeholder_text='Não é necessário preencher')
       ent_sql_cons.configure(state='disabled')

def selec_cons2(*args):
   ent_sql_cons.configure(state='normal')
   print("Evento disparado!")
   print(f"Item selecionado: {box_cons2.get()}")

   if box_cons.get() =='Tudo': 
       box_cons2.configure(state='disabled')
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Não é necessário preencher')
       ent_sql.configure(state='disabled')
   elif box_cons2.get() == 'ID_morador':
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Informe o ID do morador escolhido')
   elif box_cons2.get() == 'RG':
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Informe o RG escolhido')
   elif box_cons2.get() == 'Nome_morador':
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Informe o nome do morador escolhido')
   elif box_cons2.get() == 'Sobrenome_morador':
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Informe o sobrenome do morador escolhido')
   elif box_cons2.get() == 'Telefone':
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Informe o telefone escolhido')
   elif box_cons2.get() == 'Número':
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Informe o número do domicílio escolhido')
   elif box_cons2.get() == 'Rua':
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Informe a rua do domicílio escolhido')
   elif box_cons2.get() == 'Selecione outro campo (opcional): ...':
       ent_sql.configure(placeholder_text='Selecione alguma das escolhas ao lado')
   else:
       ent_sql.delete(0,'end')
       ent_sql.configure(placeholder_text='Informe o bairro do domicílio escolhido')

atr_var = StringVar(value= 'Selecione algum dos campos abaixo: ...')
atr_var.trace_add('write', selec_cons)

box_cons = CTkComboBox(master=tabview.tab('Consulta'), state='readonly',
   values=atr_cons, variable=atr_var, width=250, height=26, border_color='gray',
   dropdown_font=('Arial', 12), dropdown_hover_color='light green')

box_cons.place(x=40, y=60)

# Combobox para outra opção
atr_var2 = StringVar(value= 'Selecione outro campo (opcional): ...')
atr_var2.trace_add('write', selec_cons2 )

box_cons2 = CTkComboBox(master=tabview.tab('Consulta'), state='readonly',
   values=atr_cons2, variable=atr_var2, width=250, height=26, border_color='gray',
   dropdown_font=('Arial', 12), dropdown_hover_color='light green')

box_cons2.place_forget()

#Função que consulta o que usuário digitou na entry
def consulta():
   conectar()
   atribut_cons = box_cons.get()
   atribut_cons2 = box_cons2.get()
   comando_geral = ent_sql_cons.get()
   comando_nome = ent_sql.get()

  # Verifica se o campo comando geral está vazio ou no valor padrão
   atributo_vazio = atribut_cons =='Selecione algum dos campos abaixo: ...'
   atributo_vazio2 = atribut_cons2 =='Selecione outro campo (opcional): ...'
   comando_geral_vazio = not comando_geral or comando_geral.strip() == 'Selecione alguma das escolhas ao lado' or comando_geral.strip() =='Não é necessário preencher'
   comando_nome_vazio = not comando_nome or comando_nome.strip() == 'Entre com uma segunda escolha(opcional)'
  
# Verifica se todos os comandos estão vazios ou no valor padrão
   if atributo_vazio and atributo_vazio2 and comando_geral_vazio and comando_nome_vazio:
       messagebox.showerror("Cadastro", "Por favor, preencha pelo menos uma consulta!")
       return  # Interrompe a função se nenhum comando foi fornecido
   try:
       conexao = ra.connect('cadastro.db')
       cursor = conexao.cursor()
       resultado_sel.configure(state='normal')
       resultado_sel.delete("1.0", "end")  # Limpa o conteúdo
  
       try:
           if not comando_geral_vazio:
               if box_cons.get() == 'Nome_morador':
                   sql_query = "SELECT * FROM morador WHERE Nome_morador = ?"
                   res = cursor.execute(sql_query, (comando_geral,))
                   resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta Nome:\n{resultado_texto}")
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons.get() == 'Sobrenome_morador':
                   sql_query = "SELECT * FROM morador WHERE Sobrenome_morador = ?"
                   res = cursor.execute(sql_query, (comando_geral,))
                   resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta Sobrenome:\n{resultado_texto}")
                       print(resultado_texto)
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons.get() == 'RG':
                   sql_query = "SELECT * FROM morador WHERE RG = ?"
                   res = cursor.execute(sql_query, (comando_geral,))
                   resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta RG:\n{resultado_texto}")
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
              
               elif box_cons.get() == 'ID_morador':
                   sql_query = "SELECT * FROM morador WHERE ID_morador = ?"
                   res = cursor.execute(sql_query, (comando_geral,))
                   resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta ID:\n{resultado_texto}")
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons.get() == 'Telefone':
                   sql_query = "SELECT * FROM morador WHERE Telefone = ?"
                   res = cursor.execute(sql_query, (comando_geral,))
                   resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta Telefone:\n{resultado_texto}")
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons.get() == 'Número':
                   sql_query = "SELECT * FROM morador WHERE Numero = ?"
                   res = cursor.execute(sql_query, (comando_geral,))
                   resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta Número:\n{resultado_texto}")
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons.get() == 'Bairro':
                   sql_query = "SELECT * FROM morador WHERE Bairro = ?"
                   res = cursor.execute(sql_query, (comando_geral,))
                   resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta Bairro:\n{resultado_texto}")
                       print(resultado_texto)
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons.get() == 'Rua':
                   sql_query = "SELECT * FROM morador WHERE Rua = ?"
                   res = cursor.execute(sql_query, (comando_geral,))
                   resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta Rua:\n{resultado_texto}")
                       print(resultado_texto)
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")  

           elif box_cons.get() == 'Tudo':
                try:
                    # Executa a consulta SQL
                    sql_query = "SELECT * FROM morador;"
                    cursor.execute(sql_query)
                    resultado = cursor.fetchall()

                    if resultado:
                        # Formata o resultado em texto
                        resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                        messagebox.showinfo('Consulta', 'Comando realizado com sucesso!')
                        resultado_sel.insert("1.0", f"Resultado da consulta GERAL:\n{resultado_texto}")
                        print(resultado_texto)
                    else:
                        # Caso não haja resultados, exibe mensagem apropriada
                        resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
                except Exception as e:
                    # Tratamento de erros, exibindo mensagem em caso de falha
                    messagebox.showerror('Erro',"Ocorreu um erro ao executar a consulta:")
                    print(f'O erro é {e}')
           if not comando_nome_vazio:
               if box_cons2.get() == 'Nome_morador':
                   sql_query = "SELECT * FROM morador WHERE Nome_morador = ?"
                   res = cursor.execute(sql_query, (comando_nome,))
                   resultado = res.fetchall()
                   if resultado:
                         # Se o valor já existir, avisa o usuário
                       messagebox.showwarning(
                       "Valor Duplicado",
                       f"O nome '{comando_nome}' já está cadastrado. Por favor, insira um valor diferente ou verifique os dados."
                        )
                   else:
                       sql_query = "SELECT * FROM morador WHERE Nome_morador = ?"
                       res = cursor.execute(sql_query, (comando_nome,))
                       resultado = res.fetchall()
                       if resultado:
                           resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                           messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                           resultado_sel.insert("1.0", f"Resultado da consulta Nome:\n{resultado_texto}")
                           print(resultado_texto)
                       else:
                           resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons2.get() == 'Sobrenome_morador':
                   sql_query = "SELECT * FROM morador WHERE Sobrenome_morador = ?"
                   res = cursor.execute(sql_query, (comando_nome,))
                   resultado = res.fetchall()
                   if resultado:
                       messagebox.showwarning(
                       "Valor Duplicado",
                       f"O sobrenome '{comando_nome}' já está cadastrado. Por favor, insira um valor diferente ou verifique os dados."
                       )
                   else:
                       sql_query = "SELECT * FROM morador WHERE Sobrenome_morador = ?"
                       res = cursor.execute(sql_query, (comando_nome,))
                       resultado = res.fetchall()
                       if resultado:
                           resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                           messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                           resultado_sel.insert("1.0", f"Resultado da consulta Sobrenome:\n{resultado_texto}")
                           print(resultado_texto)
                       else:
                           resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons2.get() == 'RG':
                   sql_query = "SELECT * FROM morador WHERE RG = ?"
                   res = cursor.execute(sql_query, (comando_nome,))
                   resultado = res.fetchall()
                   if resultado:
                       messagebox.showwarning(
                   "Valor Duplicado",
                   f"O RG '{comando_nome}' já está cadastrado. Por favor, insira um valor diferente ou verifique os dados."
                   )
                   else:
                       sql_query = "SELECT * FROM morador WHERE RG = ?"
                       res = cursor.execute(sql_query, (comando_nome,))
                       resultado = res.fetchall()
                       if resultado:
                           resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                           messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                           resultado_sel.insert("1.0", f"Resultado da consulta RG:\n{resultado_texto}")
                           print(resultado_texto)                  
                       else:
                           resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
              
               elif box_cons2.get() == 'ID_morador':
                   if comando_nome != comando_geral:
                        sql_query = "SELECT * FROM morador WHERE ID_morador = ?"
                        res = cursor.execute(sql_query, (comando_nome,))
                        resultado = res.fetchall()
                        if resultado:
                            resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                            messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                            resultado_sel.insert("end", f"\n{resultado_texto}")
                            print(resultado_texto)
                        else:
                            resultado_sel.insert("end", "Consulta executada, sem resultados.")
                   else:
                    # Caso o ID seja o mesmo da primeira consulta, não gera duplicação ou alerta
                        messagebox.showwarning(
                            "Valor Duplicado",
                            f"O ID '{comando_nome}' já está cadastrado. Por favor, insira um valor diferente ou verifique os dados."
                            )
               elif box_cons2.get() == 'Telefone':
                   #comando_nome = numero_tel
                   verifica_numeros()
                   aplicar_mascara()
                   sql_query = "SELECT * FROM morador WHERE Telefone = ?"
                   res = cursor.execute(sql_query, (comando_nome,))
                   resultado = res.fetchall()
                   if resultado:
                       messagebox.showwarning(
                       "Valor Duplicado",
                       f"O Telefone '{comando_nome}' já está cadastrado. Por favor, insira um valor diferente ou verifique os dados."
                       )
                   else:
                       sql_query = "SELECT * FROM morador WHERE Telefone = ?"
                       res = cursor.execute(sql_query, (comando_nome,))
                       resultado = res.fetchall()
                       if resultado:
                           resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                           messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                           resultado_sel.insert("1.0", f"Resultado da consulta Telefone:\n{resultado_texto}")
                           print(resultado_texto)                  
                       else:
                           resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons2.get() == 'Número':
                   sql_query = "SELECT * FROM morador WHERE Numero = ?"
                   res = cursor.execute(sql_query, (comando_nome,))
                   resultado = res.fetchall()
                   if resultado:
                       messagebox.showwarning(
                       "Valor Duplicado",
                       f"O Número '{comando_nome}' já está cadastrado. Por favor, insira um valor diferente ou verifique os dados."
                       )
                   else:
                       sql_query = "SELECT * FROM morador WHERE Numero = ?"
                       res = cursor.execute(sql_query, (comando_nome,))
                       resultado = res.fetchall()
                   if resultado:
                       resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                       messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                       resultado_sel.insert("1.0", f"Resultado da consulta Número:\n{resultado_texto}")
                       print(resultado_texto)                   
                   else:
                       resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons2.get() == 'Bairro':
                   sql_query = "SELECT * FROM morador WHERE Bairro = ?"
                   res = cursor.execute(sql_query, (comando_nome,))
                   resultado = res.fetchall()
                   if resultado:
                       messagebox.showwarning(
                       "Valor Duplicado",
                       f"O Bairro '{comando_nome}' já está cadastrado. Por favor, insira um valor diferente ou verifique os dados."
                       )
                   else:
                       sql_query = "SELECT * FROM morador WHERE Bairro = ?"
                       res = cursor.execute(sql_query, (comando_nome,))
                       resultado = res.fetchall()
                       if resultado:
                           resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                           messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                           resultado_sel.insert("1.0", f"Resultado da consulta Bairro:\n{resultado_texto}")
                           print(resultado_texto)
                       else:
                           resultado_sel.insert("1.0", "Consulta executada, sem resultados.")
               elif box_cons2.get() == 'Rua':
                   sql_query = "SELECT * FROM morador WHERE Rua = ?"
                   res = cursor.execute(sql_query, (comando_nome,))
                   resultado = res.fetchall()
                   if resultado:
                       messagebox.showwarning(
                   "Valor Duplicado",
                   f"A Rua '{comando_nome}' já está cadastrado. Por favor, insira um valor diferente ou verifique os dados."
                   )
                   else:
                       sql_query = "SELECT * FROM morador WHERE Rua = ?"
                       res = cursor.execute(sql_query, (comando_nome,))
                       resultado = res.fetchall()
                       if resultado:
                           resultado_texto = '\n'.join(str(linhas) for linhas in resultado)
                           messagebox.showinfo('Consulta','Comando realizado com sucesso!')
                           resultado_sel.insert("1.0", f"Resultado da consulta Rua:\n{resultado_texto}")
                           print(resultado_texto)
                       else:
                           resultado_sel.insert("1.0", "Consulta executada, sem resultados.")  
       except Exception as erro:
           messagebox.showerror("Cadastro", f"Erro na consulta:")
           print(f'O erro foi {erro}')
   except ra.DatabaseError as e:
       messagebox.showerror("Consulta", "Erro no banco de dados!")
       print('Erro no banco de dados!!', e)
   finally:
       resultado_sel.configure(state='disabled')
       if conexao:
           conexao.close()

#TextBox onde é mostrado o resultado do SELECT
resultado_sel = CTkTextbox(master=tabview.tab('Consulta'), state='disabled',
        width=450,
        height=150,
        corner_radius=15,
        border_width=5,
        border_color='#3d403d',
        border_spacing=10)

resultado_sel.place(x=100, y=225)

#Botão que realiza a consulta
botao_cons = CTkButton(master=tabview.tab('Consulta'),
       text='Realizar consulta',
       border_width=2,
       border_color='dark blue',
       corner_radius=10,
       font=('Arial', 14),
       command=consulta)


#Função que limpa os campos da consulta
def limpar_cons():
   # Verifica se algum dos campos não está no valor padrão
   if (ent_sql_cons.get() != 'Selecione alguma das escolhas ao lado' or
       ent_sql.get() != 'Entre com uma segunda escolha' or box_cons.get() != 'Selecione algum dos campos abaixo: ...' or
       box_cons2.get() != 'Selecione outro campo (opcional): ...'):


       # Limpa os campos de entrada
       atr_var.set(value='Selecione algum dos campos abaixo: ...')
       atr_var2.set(value='Selecione outro campo (opcional): ...')
       ent_sql.delete(0, 'end')
       ent_sql.configure(placeholder_text='Entre com uma segunda escolha(opcional)')
       ent_sql_cons.delete(0, 'end')
       ent_sql_cons.configure(placeholder_text='Selecione alguma das escolhas ao lado')
       ent_sql.configure(state='normal')
       ent_sql.place_forget()
       ent_sql_cons.configure(state='normal')
       box_cons2.configure(state='normal')
       box_cons2.place_forget()
       resultado_sel.configure(state='normal')
       resultado_sel.delete(1.0, 'end')
       resultado_sel.configure(state='disabled')
       lb_sql_cons2.place_forget()
       lb_sql_opc2.place_forget()

#Botão que realiza a função acima
botao_limpar = CTkButton(master=tabview.tab('Consulta'),
       text='Limpar consulta(s)',
       border_width=2,
       border_color='dark blue',
       corner_radius=10,
       font=('Arial', 14),
       command=limpar_cons)

botao_limpar.place(x=330, y=385)
botao_cons.place(x=180, y=385)

# Configuração aba do Update

#Função que realiza a atualização de dados
def atualizar_dados():
    conexao = conectar()  # Conecta e recebe a conexão ativa
    if not conexao:
        messagebox.showerror("Atualização", "Erro ao conectar ao banco de dados!")
        return  # Sai da função se não houver conexão

    # Obtém a opção selecionada na combobox e os valores das entradas
    opcao_selecionada = box_upd.get()
    valor_antigo = ent_sql_upd2.get()
    valor_novo = ent_sql_upd_valor_novo.get()

    # Verifica se os campos estão vazios ou nos valores padrão
    valor_antigo_vazio = not valor_antigo or valor_antigo.strip() == 'Digite o valor antigo'
    valor_novo_vazio = not valor_novo or valor_novo.strip() == 'Digite o novo valor'

    if opcao_selecionada == 'Selecione uma opção...' or valor_antigo_vazio or valor_novo_vazio:
        messagebox.showerror("Atualização", "Por favor, selecione uma opção e preencha os valores antigos e novos!")
        return

    try:
        cursor = conexao.cursor()

        # Monta a query SQL dinamicamente com base na seleção
        sql_query = f"UPDATE morador SET {opcao_selecionada} = ? WHERE {opcao_selecionada} = ?"
        
        # Executa o comando e confirma a atualização
        cursor.execute(sql_query, (valor_novo, valor_antigo))
        conexao.commit()

        # Limpa e exibe a mensagem de sucesso
        resultado_sel2.configure(state='normal')
        resultado_sel2.delete("1.0", "end")
        resultado_sel2.insert("1.0", "Dados atualizados com sucesso!")
        messagebox.showinfo("Atualização", "Comando executado com sucesso!")

    except Exception as erro:
        messagebox.showerror("Atualização", f"Erro no comando SQL! {erro}")

    finally:
        resultado_sel2.configure(state='disabled')
        if conexao:
            conexao.close()

#Botão que realiza a atualização de dados
botao_updt = CTkButton(master=tabview.tab('Atualização'),
       text='Atualizar Dados',
       border_width=2,
       border_color='dark blue',
       corner_radius=10,
       font=('Arial', 14),
       command=atualizar_dados)

#Fonte da label SQL
sql_font = CTkFont(family='Arial', size=14, weight='bold')

#Declaração das características de cada aba da janela
atr_upd =  ['Selecione outro campo (opcional): ...', 'ID_morador', 'RG', 'Nome_morador',
           'Sobrenome_morador', 'Telefone', 'Rua', 'Número', 'Bairro']

atr_upd_var = StringVar(value='Selecione algum dos campos abaixo: ...')

box_upd = CTkComboBox(master=tabview.tab('Atualização'), state='readonly',
   values=atr_upd, variable=atr_upd_var, width=250, height=26, border_color='gray',
   dropdown_font=('Arial', 12), dropdown_hover_color='light green')
box_upd.place(x=40, y=60)

lb_sql_upd = CTkLabel(master=tabview.tab('Atualização'), text='Opções', font=sql_font)
lb_sql_upd.place(x=40, y=30)

lb_sql_upd2 = CTkLabel(master=tabview.tab('Atualização'), text='Valor Selecionado', font=sql_font)
lb_sql_upd2.place(x=340, y=30)

ent_sql_upd2 = CTkEntry(master=tabview.tab('Atualização'), width=300, placeholder_text='Informe o valor antigo (inserido anteriormente)' )
ent_sql_upd2.place(x=340, y=60)

ent_sql_upd_valor_novo = CTkEntry(master=tabview.tab('Atualização'), width=300, placeholder_text='Informe o valor novo ( a ser inserido)')
ent_sql_upd_valor_novo.place(x=340,y=110)

#TextBox onde é mostrado o resultado do Update
resultado_sel2 = CTkTextbox(master=tabview.tab('Atualização'), state='disabled',
        width=450,
        height=150,
        corner_radius=15,
        border_width=5,
        border_color='#3d403d',
        border_spacing=10)

resultado_sel2.place(x=100, y=175)

#Função que limpa os campos da consulta
def limpar_atual():
   # Verifica se algum dos campos não está no valor padrão
   if (box_upd.get() != 'Selecione algum dos campos abaixo: ...'):

        # Limpa os campos de entrada
       ent_sql_upd2.delete(0, 'end')
       ent_sql_upd2.configure(placeholder_text="Informe o valor antigo (inserido anteriormente)")
       ent_sql_upd_valor_novo.delete(0, 'end')
       ent_sql_upd_valor_novo.configure(placeholder_text="Informe o valor novo ( a ser inserido)")
       atr_upd_var.set('Selecione algum dos campos abaixo: ...')
       resultado_sel2.configure(state='normal')
       resultado_sel2.delete(1.0, 'end')
#Botão que realiza a função acima
botao_limpar_upd = CTkButton(master=tabview.tab('Atualização'),
       text='Limpar comando(s)',
       border_width=2,
       border_color='dark blue',
       corner_radius=10,
       font=('Arial', 14),
       command=limpar_atual)

botao_limpar_upd.place(x=330, y=340)
botao_updt.place(x=180, y=340)

# Configuração da aba DELETE

def deletar_dados():
    conexao = conectar()  # Conecta e recebe a conexão ativa
    if not conexao:
        messagebox.showerror("Excluir/Apagar", "Erro ao conectar ao banco de dados!")
        return  # Sai da função se não houver conexão

    try:
        cursor = conexao.cursor()
        coluna_escolhida = box_del.get()  # Obtém a opção escolhida na combobox
        valor_condicao = ent_sql_del2.get()  # Obtém o valor da condição para a exclusão
        campo = ent_sql_del.get()

        # Verifica se os campos estão vazios ou no valor padrão
        if coluna_escolhida == 'Selecione outro campo (opcional): ...' or not campo.strip():
            messagebox.showerror("Excluir/Apagar", "Por favor, selecione a coluna e preencha o valor de condição!")
            return

        # Criação do comando SQL com base na coluna e no valor fornecidos
        comando_deletar = f"DELETE FROM morador WHERE {coluna_escolhida} = {campo}"

        try:
            # Executa o comando e confirma a exclusão
            cursor.execute(comando_deletar)
            conexao.commit()

            # Verifica se algum registro foi realmente deletado
            if cursor.rowcount > 0:
                resultado_del2.configure(state='normal')
                resultado_del2.delete("1.0", "end")
                resultado_del2.insert("1.0", "Dados deletados com sucesso!")
                messagebox.showinfo("Excluir/Apagar", "Comando executado com sucesso!")
            else:
                messagebox.showinfo("Excluir/Apagar", "Nenhum registro encontrado para deletar.")

        except Exception as erro:
            messagebox.showerror("Excluir/Apagar", "Erro no comando SQL!")
            print(erro)
    except ra.DatabaseError as e:
        messagebox.showerror("Excluir/Apagar", "Erro no banco de dados!")
    finally:
        resultado_del2.configure(state='disabled')
        if conexao:
            conexao.close()
#Botão para Delete
botao_del = CTkButton(master=tabview.tab('Excluir/Apagar'),
       text='Deletar Dados',
       border_width=2,
       border_color='dark blue',
       corner_radius=10,
       font=('Arial', 14),
       command=deletar_dados)

#Fonte da label SQL
sql_font = CTkFont(family='Arial', size=14, weight='bold')

#Declaração das características de cada aba da janela

atr_del = ['Selecione outro campo (opcional): ...', 'ID_morador', 'RG', 'Nome_morador',
           'Sobrenome_morador', 'Telefone', 'Rua', 'Número', 'Bairro','Tudo']

atr_del_var = StringVar(value='Selecione algum dos campos abaixo: ...')

box_del = CTkComboBox(master=tabview.tab('Excluir/Apagar'),state='readonly',
   values=atr_del, variable=atr_del_var, width=250, height=26, border_color='gray',
   dropdown_font=('Arial', 12), dropdown_hover_color='light green')
box_del.place(x=40,y=60)

lb_sql_del = CTkLabel(master=tabview.tab('Excluir/Apagar'), text='Opções', font=sql_font)
lb_sql_del.place(x=40, y=30)

lb_sql_del = CTkLabel(master=tabview.tab('Excluir/Apagar'), text='Valor selecionado', font=sql_font)
lb_sql_del.place(x=340, y=30)

ent_sql_del = CTkEntry(master=tabview.tab('Excluir/Apagar'), width=250, placeholder_text='Informe o valor do campo escolhido')
ent_sql_del.place(x=340, y=60)  

ent_sql_del2 = CTkEntry(master=tabview.tab('Excluir/Apagar'), width=250, placeholder_text='Informe o valor do outro campo escolhido')
ent_sql_del2.place(x=340, y=130)   

lb_cm = CTkLabel(master=tabview.tab('Excluir/Apagar'), text='Condição (Opcional)', font=sql_font)
lb_cm.place(x=340, y=100)

#TextBox onde é mostrado o resultado do Update
resultado_del2 = CTkTextbox(master=tabview.tab('Excluir/Apagar'), state='disabled',
        width=450,
        height=150,
        corner_radius=15,
        border_width=5,
        border_color='#3d403d',
        border_spacing=10)

resultado_del2.place(x=100, y=210)

#Função que limpa os campos da consulta
def limpar_del():
   # Verifica se algum dos campos não está no valor padrão
   if (box_del.get() != 'Selecione outro campo (opcional): ...'):

        # Limpa os campos de entrada
       ent_sql_del2.delete(0, 'end')
       ent_sql_del2.configure(placeholder_text="Informe o valor do outro campo escolhido")
       ent_sql_del.delete(0, 'end')
       ent_sql_del.configure(placeholder_text="Informe o valor do campo escolhido")
       atr_upd_var.set('Selecione algum dos campos abaixo: ...')
       resultado_del2.configure(state='normal')
       resultado_del2.delete(1.0, 'end')

#Botão que realiza a função acima
botao_limpar_del = CTkButton(master=tabview.tab('Excluir/Apagar'),
       text='Limpar comando(s)',
       border_width=2,
       border_color='dark blue',
       corner_radius=10,
       font=('Arial', 14),
       command=limpar_del)

botao_limpar_del.place(x=330, y=370)
botao_del.place(x=180, y=370)

jan.mainloop()