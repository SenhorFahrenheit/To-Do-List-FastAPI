# Importa a classe `datetime` e `timedelta` para manipulação de datas e tempos
from datetime import datetime, timedelta
# Importa as classes necessárias da biblioteca `jose` para trabalhar com JWT (JSON Web Tokens)
from jose import JWTError, jwt
# Importa o `Depends` e `HTTPException` do FastAPI para lidar com dependências e erros de autenticação
from fastapi import Depends, HTTPException
# Importa a classe `HTTPBearer` e `HTTPAuthorizationCredentials` para lidar com autenticação via token Bearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Define uma chave secreta usada para codificar e decodificar os tokens JWT. 
# Ela deve ser mantida em segurança e nunca exposta.
SECRET_KEY = "vFn3Kz!8j@Yq9$Lx%Nr4Ue#Wd^B1Cg&TzHs6Xp*Aq+Mk7RbVcJs2PfEo"
# Define o algoritmo de codificação do JWT (no caso, HS256, que é um algoritmo de chave simétrica)
ALGORITHM = "HS256"
# Define o tempo de expiração do token, no caso, 30 minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Função para criar um token JWT
def criar_token(dados: dict):
    # Faz uma cópia dos dados para evitar modificações inesperadas no dicionário original
    dados_para_codificar = dados.copy()
    
    # Define a data de expiração do token. O token vai expirar em 30 minutos a partir do momento atual
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Atualiza os dados com a chave 'exp', que representa o tempo de expiração
    dados_para_codificar.update({"exp": expira})
    
    # Codifica os dados com a chave secreta e o algoritmo definido (HS256), gerando o token JWT
    token_jwt = jwt.encode(dados_para_codificar, SECRET_KEY, algorithm=ALGORITHM)
    
    # Retorna o token JWT gerado
    return token_jwt

# Função para verificar e decodificar um token JWT
def verificar_token(token: str):
    try:
        # Tenta decodificar o token usando a chave secreta e o algoritmo configurado
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Se a decodificação for bem-sucedida, retorna o payload do token (dados do usuário)
        return payload
    except JWTError:
        # Se ocorrer um erro durante a decodificação (por exemplo, token inválido ou expirado),
        # retorna None para indicar falha na verificação
        return None
