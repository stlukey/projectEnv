#!/usr/bin/env bash
#
#  Copyright (c) 2012, Luke Southam <luke@devthe.com>
#  All rights reserved.
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
# 
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
# 
#  - Neither the name of the DEVTHE.COM LIMITED nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
# 
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
#  CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
#  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
#  TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
#  TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
#  THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  SUCH DAMAGE.
#
#
#
#=========================================================
#
#  FILE: generate.sh
#
#  USAGE: ./generate.sh [PROJECTS_PATH] [PROJECT_NAME] [PROJECT_APP_ID]
#
#  DESCRIPTION: This creates a project framework from a template.
#
#  AUTHOR: Luke Southam <luke@devthe.com>
#
# 	COMPANY: DEVTHE.COM LIMITED
#  
#  VERSION: 1
# 	
# 	CREATED: September 2012
# 	
# 	REVISION: November 4 2012 - 1:04 pm
#
#=========================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

DYNAMIC="$DIR/dynamic"
STATIC="$DIR/static"

# Get the logger
source $DIR/pyio/logger.sh $0 $$

# the functions to use after created
functions='_activate(){ opts=$(cd $PROJECTS_PATH; for file in `find . -name "activate"`; do file=$(dirname $(dirname $file)); echo ${file:2}; done);local cur=${COMP_WORDS[COMP_CWORD]} ; COMPREPLY=( $(compgen -W "$opts" -- $cur) ); }; activate(){ if [[ -n $1 ]];then OLD_PWD=$(pwd);export OLD_PWD;cd $PROJECTS_PATH/$1;fi;source .scripts/activate; }; complete -F _activate activate; _newproject(){ opts=$(cd $PROJECT_TEMPLATES ; for file in `find . -name "generate.sh"`; do file=$(dirname $file); echo ${file:2}; done);local cur=${COMP_WORDS[COMP_CWORD]} ; COMPREPLY=( $(compgen -W "$opts" -- $cur) ); }; newproject(){ $PROJECT_TEMPLATES/$1/generate.sh ${@:2}; }; complete -F _newproject newproject;'

installFunctions(){
	while read line;do         
		if [ "$line" == "$functions" ]; then
			return 1
		fi
	done < $HOME/.bashrc
	echo -e '\n\n# Allows the use of project files\n'$functions'\n' >> $HOME/.bashrc
}

#=== FUNCTION =====================================
# NAME: main
# DESCRIPTION: This creates a project framework from a template.
# PARAMETER 1: The dir for projects
# PARAMETER 2: The projects name.
# PARAMETER 3: Google appengine's appid for the project.
#===============================================
main(){
	PROJECTS_PATH=$1
	PROJECT_NAME=$2
	PROJECT_PATH="$PROJECTS_PATH/$PROJECT_NAME"
	PROJECT_APP_ID=$3
	if [ -d "$PROJECT_PATH" ]; then
		log ERROR "'$PROJECT_PATH' already exists"
		exit 1
	fi
	log DEBUG "Begining to copy static PROJECT_PATH files"
	mkdir $PROJECT_PATH
	cp -r $STATIC/* $PROJECT_PATH
	cp -r $STATIC/.[a-zA-Z0-9]* $PROJECT_PATH
	log DEBUG "Begining to build dynamic project files"
	$DYNAMIC/build.sh $PROJECTS_PATH $PROJECT_NAME $PROJECT_APP_ID
	log DEBUG "finishing off"
	finish $@
}

#=== FUNCTION =====================================
# NAME: checkArgs
# DESCRIPTION: Makes sure script is run with the current arguments
# PARAMETER 1: The dir for projects
# PARAMETER 2: The projects name.
# PARAMETER 3: Google appengine's appid for the project.
#===============================================
checkArgs(){
	if ! [ -z "$1" ];then
		if [ -z "$1" ] | [ -z "$2" ];then
			echo "INVALID ARGUMENTS"
			echo
			echo "USAGE: $0
#or#
USAGE: $0 [PROJECT_NAME] [PROJECT_APP_ID]
#or#
USAGE: $0 [PROJECT_NAME] [PROJECT_APP_ID] [PROJECTS_PATH]

	PROJECTS_PATH: The dir for projects.
	PROJECT_NAME: The projects name.
	PROJECT_APP_ID: Google appengine's appid for the project."
			return 1
		elif ! [ -z "$3" ];then
			main $@
		else
			if [ -z "$PROJECTS_PATH" ]; then
				read -p "Where are your projects stored? "
				PROJECTS_PATH=$REPLY
				read -p "----Do you want to save this (y/n)? "
				[ "$REPLY" == "y" ] || export PROJECTS_PATH;echo -e "export PROJECTS_PATH=\"$PROJECTS_PATH\" PROJECT_TEMPLATES=\"$(dirname $(dirname $(dirname $DIR)))\"\n; #PROJECT SETUP" >> $HOME/.bashrc
			fi
			main $PROJECTS_PATH $@
		fi
	else
		echo `wizard`
	fi
}

wizard(){
	if [ -z "$PROJECTS_PATH" ]; then
		read -p "Where are your projects stored? "
		PROJECTS_PATH=$REPLY
		read -p "----Do you want to save this (y/n)? "
		[ "$REPLY" == "y" ] || export PROJECTS_PATH;echo -e "export PROJECTS_PATH=\"$PROJECTS_PATH\" PROJECT_TEMPLATES=\"$(dirname $(dirname $(dirname $DIR)))\"\n; #PROJECT SETUP" >> $HOME/.bashrc
	fi
	read -p "What is the projects name? "
	PROJECT_NAME=$REPLY
	read -p "What is the appid for appengine for the project? "
	PROJECT_APP_ID=$REPLY
	echo `main $PROJECTS_PATH $PROJECT_NAME $PROJECT_APP_ID`
}

finish(){
	cd $1/$2;
	git init . > /dev/null
	git add . > /dev/null
	git commit -a -m "initial commit for $2" > /dev/null
}


installFunctions

checkArgs $@