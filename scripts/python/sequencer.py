#!/usr/bin/python
from __future__ import with_statement
import os, sys
import re, random
#import sqlalchemy, sqlalchemy.ext.declarative
#from sqlalchemy import Table, Column, Integer, MetaData, ForeignKey
import MySQLdb
from alphabetspaths import LOG_FILE
from objectstorage import get_object, save_object

try:
    SCRIPT_PATH, SCRIPT_NAME = os.path.split(os.path.realpath(__file__))
except NameError:
    SCRIPT_PATH, SCRIPT_NAME = os.path.split(os.path.realpath(sys.argv[0]))

HOST = 'sql.mit.edu'
USER = 'jgross'
PASSWORD = 'sik15fix'

##Base = sqlalchemy.ext.declarative.declarative_base()

_info_reg = re.compile("""host=(.*?)
user=(.*?)
password=(.*?)""")
def update_info(from_file=os.path.expanduser('~/.my.cnf'), persist=True):
    global HOST, USER, PASSWORD
    with open(from_file, 'r') as f:
        new_info = f.read()
    host, user, password = _info_reg.search(new_info.strip()).groups()
    if persist:
        with open(os.path.join(SCRIPT_PATH, SCRIPT_NAME), 'r') as f:
            program = f.read()
        program = re.sub('HOST = ([^\n]+)', HOST, program)
        program = re.sub('USER = ([^\n]+)', USER, program)
        program = re.sub('PASSWORD = ([^\n]+)', PASSWORD, program)
        with open(os.path.join(SCRIPT_PATH, SCRIPT_NAME), 'w') as f:
            f.write(program)

##def setup():
##    db = sqlalchemy.create_engine('mysql://user:password@sql.mit.edu/user+db')
##    Base.metadata.create_all(db)
##    Session = sqlalchemy.orm.sessionmaker(bind=db)
##    ss = Session()
##    return (db, ss)

def connect_sql():
    return MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=USER + '+alphabets')

def get_random_sequence(tag, length=None, reset=False):
    _random = get_object('sequencer-random', (lambda: random.Random()))
    is_old = ((lambda x:reset) if reset else None)
    if length is not None:
        new_sequence = list(range(length))
        _random.shuffle(new_sequence)
    else: new_sequence = []
    sequence = get_object('sequences-%s' % tag, (lambda *args, **kargs: new_sequence), is_old=is_old)
    if length is not None:
        sequence = sequence[:length]
    return sequence

def reset_table(tag, length=None):
    if length is None: length = len(get_random_sequence(tag))
    with open(LOG_FILE, 'a') as f:
        f.write('Resetting table %s to length %s.' % (tag, length))
    sqldb = connect_sql()
    cursor = sqldb.cursor()
    try:
        cursor.execute('LOCK TABLES %s WRITE' % tag)
    except Exception:
        pass
    try:
        cursor.execute('DROP TABLE %s' % tag)
    except Exception:
        pass
    try:
        cursor.execute('CREATE TABLE %s(id INT)' % tag)
        cursor.executemany('INSERT INTO %s (id) VALUES (%%s)' % tag,
                           [(i,) for i in range(length)])
        try:
            cursor.execute('UNLOCK TABLES')
        except Exception:
            pass
    except Exception:
        sqldb.rollback()
        raise
    finally:
        sqldb.commit()
        sqldb.close()

def count_left(tag):
    sqldb = connect_sql()
    cursor = sqldb.cursor()
    cursor.execute('SELECT * FROM %s' % tag)
    rtn = cursor.rowcount
    sqldb.close()
    return rtn

def pop(tag, count=1, reset_sequence=False, reset_database=False, reset_on_run_out=False, length=None):
    if reset_database:
        reset_table(tag, length=length)
    
    sqldb = connect_sql()
    cursor = sqldb.cursor()

    try:
        try:
            cursor.execute('LOCK TABLES %s WRITE' % tag)
            cursor.execute('SELECT id FROM %s ORDER BY id LIMIT %d' % (tag, count))
            rtn = cursor.fetchmany(size=count)
            cursor.executemany('DELETE FROM %s WHERE id=%%s' % tag,
                               rtn)
            rtn = [int(i) for i, in rtn]
            cursor.execute('UNLOCK TABLES')
        except Exception:
            sqldb.rollback()
            raise
        finally:
            sqldb.commit()
            sqldb.close()
    except IndexError:
        if reset_on_run_out:
            reset_table(tag)
            return pop(tag, count=count, reset_sequence=reset_sequence, reset_on_run_out=False, length=length)
        else:
            raise
    random_sequence = get_random_sequence(tag, length=length, reset=reset_sequence)
    rtn = [random_sequence[i] for i in rtn]
    if len(rtn) == 1: rtn = rtn[0]
    return rtn
