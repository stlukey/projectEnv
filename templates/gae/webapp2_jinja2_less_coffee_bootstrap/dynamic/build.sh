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
#  FILE: build.sh
#
#  USAGE: ./build.sh [PROJECTS_PATH] [PROJECT_NAME] [APPID]
#
# DESCRIPTION: This creates a project framework from a template.
#
# PARAMETER 1: The dir for projects
# PARAMETER 2: The projects name.
# PARAMETER 3: Google appengine's for the project.
#
#  AUTHOR: Luke Southam <luke@devthe.com>
#
# 	COMPANY: DEVTHE.COM LIMITED
#  
#  VERSION: 1
# 	
# 	CREATED: ~ September 2012
# 	
# 	REVISION: October 23 2012 - 7:17 pm
#
#=========================================================

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

PROJECTS_PATH=$1
PROJECT_NAME=$2
PROJECT_PATH="$PROJECTS_PATH/$PROJECT_NAME"
PROJECT_APP_ID=$3

PROJECT_VARS="PROJECTS_PATH=$PROJECTS_PATH PROJECT_NAME=$PROJECT_NAME PROJECT_APP_ID=$PROJECT_APP_ID"

#=== FUNCTION =====================================
# NAME: build
# USAGE: build [file] [key]=[value]
# DESCRIPTION: Builds the dynamic files and returns them.
# PARAMETER 1: template
# PARAMETER 2+: template vars: key=value.
# OUTPUT: rendered template.
#===============================================
build(){
python <<END
print file("$1").read().format(**{kw.split("=")[0]:kw.split("=")[1] for kw in """${@:2}""".split(" ")})
END
}

##############################################
#BUILD COMMANDS HERE

build .scripts/project_vars.sh $PROJECT_VARS > $PROJECT_PATH/.scripts/project_vars.sh
build app/app.yaml $PROJECT_VARS > $PROJECT_PATH/app/app.yaml
build app/main.py $PROJECT_VARS > $PROJECT_PATH/app/main.py
