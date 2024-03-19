from flask import Flask
from website.app import create_app
from getpass import getpass
from website.app import dbconfig
import hashlib
import random
import string
import mysql.connector
import sys
from rich.console import Console


app=create_app()

if __name__ == "__main__":
    app.run(debug=True)



def generatedevicedecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase+string.digits,k=length))

def config():
    db=dbconfig()
    cursor=db.cursor()

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS pm")

    except Exception as e:
        print("An error occurred while trying to create db. Check if database with name 'pm' already exists - if it does, delete it and try again.")
        Console.print_exception(show_locals=True)
        sys.exit(0)
    print("databse created succesfully!!!")

    query ="CREATE TABLE pm.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    q=cursor.execute(query)
    print("Table 'secrets' created ")

    query = "CREATE TABLE pm.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)
    print("Table 'entries' created ")
    
    while 1:
        mp=getpass("choose a master password:")
        if mp==getpass("re type the password:") and mp!="":
            break 
        print("please try again")

    hashed_mp=hashlib.sha256(mp.encode()).hexdigest()
    print("generated hash")

    ds=generatedevicedecret()

    query="INSERT INTO pm.secrets (masterkey_hash,device_secret) values (%s,%s)"
    val=(hashed_mp,ds)
    cursor.execute(query,val)
    db.commit()

config()


