# -*- coding: utf-8 -*-

import sqlite3
import sys
import os
import logging
import functools

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger.addHandler(sh)

database_name = '.save_commands.db'
database_path = os.path.join(os.getenv("HOME"), database_name)
params = {}


def verify_arguments(args):
    if len(args) < 2:
        logger.info("Missing action parameter ('help', 'add', 'remove', 'run' or 'list')")
        return None
    else:
        action = args[1]

        def print_wspace(string, slen):
            print(string.rjust(len(string) + slen))

        if action in ['help']:
            print('The tool save-command is a easy way for save and run shell commands. \n')           
    
            print('Options:')
            print_wspace("list", 5)
            print_wspace("List all keys and descriptions", 10)  
            print_wspace("Usage: save-commands list", 10)          
            print_wspace("add", 5)
            print_wspace("Add a new entry.", 10)
            print_wspace("Usage: save-commands add '<KEY>' '<VALUE>' '<DESC>'", 10)            
            print_wspace("remove", 5)
            print_wspace("Remove a entry based on a key.", 10)
            print_wspace("Usage: save-commands remove '<KEY>'", 10)
            print_wspace("run", 5)
            print_wspace("Run a command based on a key.", 10)
            print_wspace("Usage: save-commands run '<KEY>'", 10)

            return None
        if action in ['add']:
            if len(args) != 5:
                logger.info("Wrong parameter format - ADD action.")
                logger.info("Usage: save-commands add '<KEY>' '<VALUE>' '<DESC>'")
                return None
            else:
                params['key'] = args[2]
                params['value'] = args[3]
                params['desc'] = args[4]
        elif action in ['remove', 'run']:
            if len(args) != 3:
                logger.info("Wrong parameter format - REMOVE or RUN action.")
                logger.info("Usage: save-commands remove '<KEY>'")
                logger.info("Usage: save-commands run '<KEY>'")
                return None
            else:
                params['key'] = args[2]
        
        params['action'] = action
        return params


def get_connection():
    if not os.path.isfile(database_path):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE commands (
                cmd_id TEXT NOT NULL PRIMARY KEY,
                cmd_text TEXT NOT NULL,
                cmd_desc TEXT NOT NULL
        )
        """)
        cursor.close()
    
    conn = sqlite3.connect(database_path)
    conn.text_factory = str
    return conn


def action_add(params):
    if len(params['key']) > 400 or len(params['value']) > 400 or len(params['desc']) > 400:
        logger.warn("Parameters must be up to 400 characters.")
        return False

    conn = get_connection()
    cursor_act = conn.cursor()

    cursor_act.execute("SELECT cmd_id FROM commands where cmd_id = ?", [params['key']])
    if len(cursor_act.fetchall()) > 0:
        logger.info("Command key not found.")
        conn.close()
        return False  
    
    values = [params['key'], params['value'], params['desc']]
    cursor_act.execute("INSERT INTO commands (cmd_id, cmd_text, cmd_desc) values (?, ?, ?)", values)
    conn.commit()
    conn.close()
    return True


def action_remove(params):    
    if len(params['key']) > 400:
        logger.warn("Parameters must be up to 400 characters.")
        return False
    
    conn = get_connection()
    cursor_act = conn.cursor()
    
    v = '%' + params['key'] + '%'
    cursor_act.execute("SELECT cmd_id FROM commands where cmd_id like ?", [v])
    keys_val = cursor_act.fetchall() 

    if len(keys_val) == 0:
        logger.info("Command key not found.")
        conn.close()
        return False  

    logger.info("Keys found:")
    for k in keys_val:
        print(k[0])

    rem = ''
    while rem not in ['yes', 'no']:
        rem = input('You want remove all keys ? (yes or no) \n')
    
    if rem == 'yes':
        cursor_act.execute("DELETE FROM commands where cmd_id like ?", [v])
        conn.commit()
    
    conn.close()
    return True


def action_list():             
    conn = get_connection()
    cursor_act = conn.cursor()

    cursor_act.execute("SELECT cmd_id, cmd_desc FROM commands")
    keys_val = cursor_act.fetchall()

    if len(keys_val) == 0:
        logger.info("Database is empty.")
        return None
    
    col1_size = 15
    col2_size = 15

    itens = []

    for k in keys_val:
        if len(k[0]) > col1_size:
            col1_size = len(k[0]) + 2

        if len(k[1]) > col2_size:
            col2_size = len(k[1]) + 2

        itens.append((k[0], k[1]))

    c1_header = "+" + functools.reduce(lambda x, y: x + y, ["-" for _ in range(0, col1_size + col2_size +1)]) + "+"
    print(c1_header)
    ftm = "|{:" + str(col1_size) + "}|{:"+ str(col2_size) +"}|"

    print(ftm.format(" Command ", " Description "))
    for item in itens:
        print(ftm.format(" {} ".format(item[0]), " {} ".format(item[1])))
    print(c1_header)


def action_run(params):
    if len(params['key']) > 400:
        logger.warn("Parameters must be up to 400 characters.")
        return None
    
    conn = get_connection()
    cursor_act = conn.cursor()

    v = '%' + params['key'] + '%'
    cursor_act.execute("SELECT cmd_text, cmd_id FROM commands where cmd_id like ? limit 1", [v])

    result = cursor_act.fetchall()
    
    if len(result) == 0:
        conn.close()
        logger.info("Parameter key doesn't exists.")
        return None
    
    cmd = result[0][0]
    cmd_id = result[0][1]
    logger.info("Running {}".format(cmd_id))
    os.system(cmd)


def main(sys_args):
    format_args = verify_arguments(sys_args)
    if format_args is None:
        exit(0)

    if format_args['action'] == 'add':
        action_add(format_args)
    elif format_args['action'] == 'remove':
        action_remove(format_args)
    elif format_args['action'] == 'list':
        action_list()
    elif format_args['action'] == 'run':
        action_run(format_args)


if __name__ == "__main__":
    main(sys.argv)
