import fdb

def db_connection():
    """
    Estabelece conexão com o banco de dados Firebird.
    
    Args:
        host: Endereço do servidor do banco de dados
        database: Nome do banco de dados
        user: Nome de usuário para conexão
        password: Senha do usuário
        
    Returns:
        Tupla com a conexão e cursor do banco de dados
    """
    try:
        con = fdb.connect(host='localhost', 
                        database='employee',
                        user='sysdba', 
                        password='masterkey')
        cur = con.cursor()
        return con, cur
    except fdb.Error as e:
        raise ConnectionError(f"Erro ao conectar ao banco de dados: {str(e)}")