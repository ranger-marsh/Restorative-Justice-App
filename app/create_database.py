#!/usr/bin/env python3

"""
Functions for using the adding, manipulating and consuming data with
sqlite3. The table is created that does not allow duplicates or empty
empty strings in key columns. It also filters data based on user
specified values.
"""

import sqlite3


def create_case_table(cursor):

    cursor.execute('''
                    CREATE TABLE "cases" (
                    id integer PRIMARY KEY,
                    case_number text NOT NULL,
                    case_date datetime NOT NULL,
                    district text NOT NULL,
                    UNIQUE(case_number)
                    );
                    ''')
    return None


def create_status_table(cursor):

    cursor.execute('''
                    CREATE TABLE "status" (
                    id integer PRIMARY KEY,
                    case_id integer NOT NULL,
                    arrestee_id integer NOT NULL,
                    approved datetime NOT NULL,
                    status text NOT NULL,
                    completed datetime
                    );
                    ''')
    return None


def create_arrestee_table(cursor):

    cursor.execute('''
                    CREATE TABLE "arrestee" (
                    id integer PRIMARY KEY,
                    case_id integer NOT NULL,
                    name text NOT NULL,
                    sex text NOT NULL,
                    race text NOT NULL,
                    dob datetime NOT NULL,
                    age integer NOT NULL
                    );
                    ''')
    return None


def create_arrest_table(cursor):

    cursor.execute('''
                    CREATE TABLE "arrest" (
                    id integer PRIMARY KEY,
                    case_id integer NOT NULL,
                    arrestee_id integer NOT NULL,
                    incident_type text NOT NULL,
                    charge_type text NOT NULL
                    );
                    ''')
    return None


def create_contact_table(cursor):

    cursor.execute('''
                    CREATE TABLE "contact" (
                    id integer PRIMARY KEY,
                    case_id integer NOT NULL,
                    arrestee_id integer NOT NULL,
                    address text,
                    phone text,
                    email text
                    );
                    ''')
    return None


def create_tables(cursor):
    create_case_table(cursor)
    create_status_table(cursor)
    create_arrestee_table(cursor)
    create_arrest_table(cursor)
    create_contact_table(cursor)


def main():
    pass

if __name__ == '__main__':
    main()
