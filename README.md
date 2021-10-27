# Postbot

## INDEX

- [Postbot] (#postbot)
  - [INDEX](#index)
    - [Introduction](#introduction)
    - [Installation](#installation)

### Introduction

A simple telegram bot which will publish your posts to multiple medium, like teelgram channels and groups, discord, instagram, twitter and more in future. **NOTE: This repo is in it's early and development stage, so we suggest others except developers not to use**

This bot was created using python version 3. This runs over the telegram as main source.

### Installation
While this bot is made up of you have to creat env to isolate this from other projects.

* clone the repo
  
  `git clone https://github.com/Code-Tamil/Post-bot.git`
* make secure env for this project using ven

     `python3 -m venv env`
* activate the env

    `source env/bin/activate`
* install all requirements

    `pip install -r requirements.txt`
* create `.env` file in the root directory and add required Tokens

    `touch .env`

* run the bot
  
    `python -m bot`
