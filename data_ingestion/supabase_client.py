from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_KEY

def get_supabase_client() -> Client:
    """Cria e retorna um cliente Supabase."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("As credenciais do SUPABASE_URL e SUPABASE_KEY não estão definidas")

    return create_client(SUPABASE_URL, SUPABASE_KEY)

if __name__ == "__main__":
    client = get_supabase_client()
    print("Conectado ao Supabase:", client)