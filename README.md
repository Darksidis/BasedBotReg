# BasedBotReg

Description
-------

This program is intended for re-registration of members of a political organization.


How it works
-------

The user goes through several questions through the telegram bot, and depending on how he answered, he stays in the organization or leaves it. And the received data (status, nickname, id, time to answer) are entered into the database.


Used technologies
-------

API telegram (I used the aiogram library to work with it), postgres (to work with databases), Heroku as hosting.


Navigation
-------

-- LprBasedReg.py - the main file, it works with the telegram api, and also receives data that is then entered into the database.

-- sqlighterReg.py - file for working with the postgres database. With the help of the functions in this file, the received data is entered into the database, there are also functions that retrieve this data.
