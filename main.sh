if [ ! -f poetry.lock ]; then
    poetry install
fi

python peridot test.peri
