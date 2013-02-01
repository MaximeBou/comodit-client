#!/bin/bash

usage()
{
    echo $0 "-e EMAIL f FULLNAME -m MESSAGE [-d]"
}

DEBEMAIL=
DEBFULLNAME=
MESSAGE=
FIELDS="2"

while getopts "de:f:m:" opt
do
    case $opt in
        d)
            FIELDS="2-3"
            ;;
        e)
            DEBEMAIL=$OPTARG
            ;;
        f)
            DEBFULLNAME=$OPTARG
            ;;
        m)
            MESSAGE=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" 1>&2
            exit 1
            ;;
    esac
done

if [ "$DEBEMAIL" = "" ]
then
    echo "Missing email"
    usage
    exit 1
fi

if [ "$DEBFULLNAME" = "" ]
then
    echo "Missing full name"
    usage
    exit 1
fi

if [ "$MESSAGE" = "" ]
then
    echo "Missing message"
    usage
    exit 1
fi

VERSION=$(git describe | cut -d- -f $FIELDS)

export DEBEMAIL
export DEBFULLNAME

debchange --newversion $VERSION "$MESSAGE"

unset DEBEMAIL
unset DEBFULLNAME
