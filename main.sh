pkgcheck=`pip show colorama | grep 'Name: colorama'`
if [ "$pkgcheck" != "Name: colorama" ]; then
    poetry install
fi

peridot test.peri
