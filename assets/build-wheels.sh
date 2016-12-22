#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y tpm-tools opencryptoki-devel openCryptoki-devel trousers-devel openssl-devel python-pip python-devel

ls -las /io/
find /io/

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install -r /io/dev-requirements.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

pwd
ls -las wheelhouse/
#rm -rf wheelhouse/argparse-*whl
#rm -rf wheelhouse/six-*whl
#rm -rf wheelhouse/pycparser-*.whl
#rm -rf wheelhouse/funcsigs-*.whl
#rm -rf wheelhouse/mock-*.whl
#rm -rf wheelhouse/pbr-*.whl
#rm -rf wheelhouse/*-none-any.whl
#ls -las wheelhouse/

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    if [[ "$whl" == *"-none-any.whl" ]]; then
        continue
    fi

    echo "Audit wheel for $whl"
    auditwheel repair "$whl" -w /io/wheelhouse/
done

pwd
ls -las wheelhouse/

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install pytpmutils --no-index -f /io/wheelhouse
    # (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
done
