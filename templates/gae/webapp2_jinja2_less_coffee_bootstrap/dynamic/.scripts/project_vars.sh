#!/usr/bin/env bash

## Where projects are stored
PROJECTS_PATH="{PROJECTS_PATH}"

## Name of this project
PROJECT_NAME="{PROJECT_NAME}"

## Location of project
PROJECT_PATH="$PROJECTS_PATH/$PROJECT_NAME"

## The path of custom scripts
SCRIPT_DIR="$PROJECT_PATH/.scripts"


# AppEngine vars

## Google App Engine appid fro the project
PROJECT_APP_ID="{PROJECT_APP_ID}"

## The app engine SDK's path.
APP_ENGINE="$PROJECT_PATH/app_engine_sdk"