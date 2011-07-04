#!/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH="$(readlink -f "$(dirname "$0")")"
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0
SANDBOX=
for arg in "$@"
do
	if [ "$arg" = "-sandbox" ]; then
		SANDBOX=-sandbox
	fi
done
source local_hit_header.sh "$@"
