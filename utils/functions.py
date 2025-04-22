# Importando o módulo bcrypt para realizar operações de criptografia de senhas
import bcrypt

# Função para gerar o hash de uma senha
def gerar_hash(password):
    # Converte a senha para bytes usando a codificação UTF-8
    password_bytes = password.encode('utf-8')
    
    # Gera um "sal" (salt) aleatório, usado para aumentar a segurança da criptografia
    salt = bcrypt.gensalt()
    
    # Cria o hash da senha com o "sal", utilizando bcrypt. O resultado é um hash criptografado
    # e o método .decode('utf-8') converte o hash gerado para uma string UTF-8
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

# Função para verificar se a senha fornecida corresponde ao hash armazenado
def verificar_senha(password, hashed):
    # Compara a senha fornecida (convertida para bytes) com o hash armazenado (também convertido para bytes)
    # bcrypt.checkpw retorna True se as senhas coincidirem, e False caso contrário
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
