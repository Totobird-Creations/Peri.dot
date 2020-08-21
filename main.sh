pkgcheck=`pip show colorama | grep 'Name: colorama >&-'`
if [ "$pkgcheck" != "Name: colorama" ]; then
    poetry install
fi

python peridot test.peri
