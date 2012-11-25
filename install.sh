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
#  FILE: install.sh
#
#  USAGE: ./install.sh
#
#  DESCRIPTION: installs the currect environment varibles
#				to ~/.bashrc and saves templates to the currect folder 
#
#  AUTHOR: Luke Southam <luke@devthe.com>
#
# 	COMPANY: DEVTHE.COM LIMITED
#  
#  VERSION: 1
# 	
# 	CREATED: November 4 2012
# 	
# 	REVISION: November 4 2012 - 1:04 pm
#
#=========================================================


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


sudo apt-get install make
sudo npm install -g less
sudo npm install -g coffee-script
sudo pip install coffeescript

read -p "Where do you want the development directory ?: "
DEV_PATH=$REPLY
PROJECTS_PATH=$DEV_PATH/projects
PROJECT_TEMPLATES=$DEV_PATH/projects_templates

mkdir $DEV_PATH
mkdir $DEV_PATH/lib
mkdir $DEV_PATH/projects
cp $DIR/templates/ $DEV_PATH/projects_templates -r
cp $DIR/lib $DEV_PATH -r

vars="export PROJECTS_PATH=\"$PROJECTS_PATH\" PROJECT_TEMPLATES=\"$PROJECT_TEMPLATES\"; #PROJECT SETUP"
functions='_activate(){ opts=$(cd $PROJECTS_PATH; for file in `find . -name "activate"`; do file=$(dirname $(dirname $file)); echo ${file:2}; done);local cur=${COMP_WORDS[COMP_CWORD]} ; COMPREPLY=( $(compgen -W "$opts" -- $cur) ); }; activate(){ if [[ -n $1 ]];then OLD_PWD=$(pwd);export OLD_PWD;cd $PROJECTS_PATH/$1;fi;source .scripts/activate; }; complete -F _activate activate; _newproject(){ opts=$(cd $PROJECT_TEMPLATES ; for file in `find . -name "generate.sh"`; do file=$(dirname $file); echo ${file:2}; done);local cur=${COMP_WORDS[COMP_CWORD]} ; COMPREPLY=( $(compgen -W "$opts" -- $cur) ); }; newproject(){ $PROJECT_TEMPLATES/$1/generate.sh ${@:2}; }; complete -F _newproject newproject;'

echo -e '\n\n#### Allows the use of project files\n'$vars'\n'$functions'\n####\n' >> $HOME/.bashrc