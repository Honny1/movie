import argparse
import json
import sqlite3
import pprint
from moviedb import db
from moviedb import sqla


def parse_arguments():
    parser = argparse.ArgumentParser(description='Movie db client')
   
    parser.add_argument("filename")

    subparsers = parser.add_subparsers(help='opration')

    parser_add = subparsers.add_parser('add', help='a help')
    parser_add.add_argument('title',help='film title')
    parser_add.add_argument('duration',type=int,help='film duration')
    parser_add.add_argument('genre',help='Comma-separated list of genre')
    parser_add.add_argument('rating',type=float, nargs="?",help = "Film rating [0-5]")
    parser_add.set_defaults(func=add_film)
    
    parser_list = subparsers.add_parser('list', help='a help')
    parser_list.add_argument('title',nargs = "?",help='film title')
    parser_list.set_defaults(func=list_film)

    args = parser.parse_args()

    return args

def add_film(database, args):
    film=db.Film(args.title, args.duration, args.genre.split(","), args.rating)
    database.store(film)

def list_film(Database,args):
    pass

arg = parse_arguments()

backend=f"sqlite:///{arg.filename}"
database=sqla.SqlAlchemyFilmStorage(backend)

arg.func(database,arg)