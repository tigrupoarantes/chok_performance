import os
from app import app
from auth import criar_usuario_supabase, remover_usuario_supabase


def setup_env():
    os.environ.setdefault('SUPABASE_URL', 'https://olgnzpfoqseecrrixxup.supabase.co')
    os.environ.setdefault('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sZ256cGZvcXNlZWNycml4eHVwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDIyMTQ1NSwiZXhwIjoyMDg1Nzk3NDU1fQ.HEnbeBlGQSk-KJPOt4Qgjthl2uj2uTBbmOKZvkqQ6m8')


def test_admin_create_and_delete_via_routes():
    setup_env()
    c = app.test_client()

    # login as gerencia
    r_login = c.post('/', data={'usuario': 'admin', 'senha': 'admin@2024'})
    assert r_login.status_code in (302,200)

    usuario = 'admin_test_user'
    senha = 'admin_test_pass'

    # create via admin route
    r_create = c.post('/admin/usuarios', data={'usuario': usuario, 'senha': senha, 'perfil': 'vendedor'})
    assert r_create.status_code == 201

    # verify can login with created user
    r_login2 = c.post('/', data={'usuario': usuario, 'senha': senha}, follow_redirects=False)
    assert r_login2.status_code in (302,200)

    # delete via admin route
    r_delete = c.delete(f'/admin/usuarios/{usuario}')
    assert r_delete.status_code == 200

    # cleanup attempt (in case delete didn't remove)
    try:
        remover_usuario_supabase(usuario)
    except Exception:
        pass
