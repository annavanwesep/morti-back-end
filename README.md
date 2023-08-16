# Morti Web App: Back-end Layer

This scaffold includes the following:

## `app/__init__.py`

Models:

- User
- Messages

## `app/routes.py`

Routes for users:

As a user, I want to be able to register for an account.
As a user, I want to be able to login to my account.

CRUD routes for messages:

As a user, I want to be able to click a Create Farewell Message button to display a form to create a new message
As a user I want to be able to click a Farewell Messages button to display all my farewell messages to see them
As a user I want to be able to see a list of my saved messages so that I know they exist.
As a user I want to be able to see the title, recipient name, if text, if audio.
If message has audio, i want to be able to play it, pause it
As a user i want to be able to click on a button to delete the whole farewell message 
 
Routes for trusted Person:
As a user i want to be able to click on Trusted person button to display create new trusted person and all my trusted people
As a user i want to be able to create a new trusted person by inputting name and email 
As a user I want to be able to see a list of trusted people to see their name and email.
As a user I want to able able to click a button to delete one trusted person 
As a user, if one of my trusted persons also adds me (accounts linked), I want to see a button that allows me to declare their death
I should see a message that confirms I want to declare my trusted person dead

## `requirements.txt`

This file lists the dependencies we anticipate are needed for the project.
