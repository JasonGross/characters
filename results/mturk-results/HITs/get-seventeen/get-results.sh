#/bin/bash
export JAVA_HOME=/usr
SCRIPTPATH=`dirname $(readlink -f $0)`
export MTURK_CMD_HOME=~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0
for file in HIT-results-17.txt*
do
    mv $file ${file}2.bak
done
pushd ~/web_scripts/alphabets/results/mturk-results/aws-mturk-clt-1.3.0/bin
# from http://fritzthomas.com/open-source/linux/384-how-to-get-the-absolute-path-within-the-running-bash-script/
echo $SCRIPTPATH
./getResults.sh -successfile $SCRIPTPATH/characterrequest.input.success -namevaluepairs -outputfile $SCRIPTPATH/HIT-results-17.txt
popd
pushd $SCRIPTPATH
cp HIT-results-17.txt ../../
popd
