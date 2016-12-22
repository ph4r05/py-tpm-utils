import argparse
import sys
import pytss
import pytss.tspi_defines as consts
import uuid
import json
import binascii
import collections


def get_key_size_flags(keysize):
    """
    Returns key size flag corresponding to numerical key size in bits
    :param keysize:
    :return:
    """
    if keysize == 512:
        return consts.TSS_KEY_SIZE_512
    elif keysize == 1024:
        return consts.TSS_KEY_SIZE_1024
    elif keysize == 2048:
        return consts.TSS_KEY_SIZE_2048
    elif keysize == 4096:
        return consts.TSS_KEY_SIZE_4096
    elif keysize == 8192:
        return consts.TSS_KEY_SIZE_8192
    elif keysize == 16384:
        return consts.TSS_KEY_SIZE_16384
    else:
        raise ValueError('Unrecognized key size: %s' % keysize)


class App(object):
    def __init__(self, *args, **kwargs):
        self.args = None
        self.keysize = 1024

    def main(self):
        """
        Main entry point - argument parsing
        :return:
        """
        parser = argparse.ArgumentParser(description='TPM util for generating RSA keys')
        parser.add_argument('--keysize', dest='keysize', type=int, default=1024,
                            help='RSA key size in bits')

        self.args = parser.parse_args()
        self.keysize = self.args.keysize
        self.generate()

    def generate(self):
        """
        Generates RSA key to standard output
        :return:
        """
        ctx = pytss.TspiContext()
        ctx.connect()

        srk_uuid = uuid.UUID('{00000000-0000-0000-0000-000000000001}')
        srk_secret = bytearray([0] * 20)

        srk = ctx.load_key_by_uuid(consts.TSS_PS_TYPE_SYSTEM, srk_uuid)

        flags = get_key_size_flags(self.keysize)
        flags |= consts.TSS_KEY_TYPE_SIGNING
        flags |= consts.TSS_KEY_VOLATILE
        flags |= consts.TSS_KEY_NO_AUTHORIZATION
        flags |= consts.TSS_KEY_NOT_MIGRATABLE

        srkpolicy = srk.get_policy_object(consts.TSS_POLICY_USAGE)
        srkpolicy.set_secret(consts.TSS_SECRET_MODE_SHA1, srk_secret)

        k = ctx.create_wrap_key(flags, srk.get_handle())
        k.load_key()

        e = k.get_attribute_data(consts.TSS_TSPATTRIB_RSAKEY_INFO, consts.TSS_TSPATTRIB_KEYINFO_RSA_EXPONENT)
        n = k.get_pubkey()
        blob = k.get_keyblob()

        js = collections.OrderedDict()
        js['exponent'] = binascii.hexlify(e)
        js['modulus'] = binascii.hexlify(n)
        js['blob'] = binascii.hexlify(blob)
        print(json.dumps(js))


def main():
    app = App()
    app.main()


if __name__ == '__main__':
    main()





