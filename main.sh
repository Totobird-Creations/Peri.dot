click=`pip show click | grep 'Name: click'`
if [ "$click" != "Name: click" ]; then
    poetry install
fi

python peridot test.peri
