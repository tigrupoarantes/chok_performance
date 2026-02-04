#!/usr/bin/env python3
import argparse
from auth import criar_usuario_supabase, remover_usuario_supabase

parser = argparse.ArgumentParser(description='Manage application users (Supabase)')
subparsers = parser.add_subparsers(dest='cmd')

create = subparsers.add_parser('create', help='Create a user')
create.add_argument('--usuario', required=True)
create.add_argument('--senha', required=True)
create.add_argument('--perfil', default='vendedor')

delete = subparsers.add_parser('delete', help='Delete a user')
delete.add_argument('--usuario', required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    if args.cmd == 'create':
        res = criar_usuario_supabase(args.usuario, args.senha, perfil=args.perfil)
        print('created:', res)
    elif args.cmd == 'delete':
        res = remover_usuario_supabase(args.usuario)
        print('deleted:', res)
    else:
        parser.print_help()
