=====================
TPM utils for Python
=====================

Simple Trusted Platform Module utils (and example codes) for Python using *pytss* library.

Installation
-------------

.. code-block:: bash

    pip install pytpmutils

Dependencies
------------

* Debian / Ubuntu
.. code-block:: bash

    sudo apt-get install tpm-tools libtspi-dev libopencryptoki-dev libssl-dev python-pip python-dev build-essential

* Redhat / Fedora
.. code-block:: bash

    sudo yum install tpm-tools opencryptoki-devel trousers-devel openssl-devel python-pip python-devel

======
Usage
======

Generating random data
----------------------

Generate 2x 128 bytes and pass it to hexdump:

.. code-block:: bash

    tpm-rndgen --bs=128 --count=2 | hexdump


Generate RSA Key:
-----------------

.. code-block:: bash

    tpm-rsagen --keysize 512


Output:

.. code-block:: json

    {"exponent": "010001", "modulus": "8aed2c4c971011b94560f0f88236e5decafe64140e097deac70cccfc94c8b97ab6a082544f881137ccc7d0b9ddaf79acfd2d5bddb7fbe223cea1e2f3312091a5", "blob": "010100000010000000040000000001000100020000000c00000200000000020000000000000000000000408aed2c4c971011b94560f0f88236e5decafe64140e097deac70cccfc94c8b97ab6a082544f881137ccc7d0b9ddaf79acfd2d5bddb7fbe223cea1e2f3312091a5000001004b9302a95dfdd81c46e3a439bd5d1d663f6405f60c64a0f455f6fdae3f18ff0fddf7e16e2d47468603bc424126478b069ba3d2749bfc258b42c46e0a860f95f697abdb98da204255685f36b86e58690c6377fda049b80e2c7a9b2acfb37e232dfe16a6651ce1d83162693ca6eecf589aa686ec7bf06db19b76c03877206004d11490e1651a71d79928d763fdd4427ecb912be1a1936a66c097b8b3f8b0174270e8765a2e07c279e663955ae5310a6c7378096a166ba155852bffe7c3bc09f484d242b2742d3165f5423722ae88b6299ab07168711baaecee8e566430ea3072b4cdbd95440ed269c6e0488dc8b9ed19448a9d42d6c0f77ff6f5a66dcad3e5f79f"}

