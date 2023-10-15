#!/bin/sh

# create the var directory if there isn't
if [ ! -d "var" ]; then
  mkdir var
fi

# install required modules
pip install -r requirements.txt

# build database with mock data
sqlite3 ./var/mock.db < ./share/db.sql
