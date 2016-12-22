import argparse
import sys
import pytss


class App(object):
    def __init__(self, *args, **kwargs):
        self.args = None
        self.bs = 1024
        self.count = -1

    def main(self):
        """
        Main entry point - argument parsing
        :return:
        """
        parser = argparse.ArgumentParser(description='TPM util for generating random data')
        parser.add_argument('--bs', dest='bs', type=int, default=1024,
                            help='Length of the chunk to generate in TPM in bytes (max 4096B)')
        parser.add_argument('--count', dest='count', type=int, default=-1,
                            help='Number of chunks to generate. If negative, chunks are generated forever')

        self.args = parser.parse_args()
        self.bs = self.args.bs
        self.count = self.args.count
        self.generate()

    def generate(self):
        """
        Generates required amount of random bytes to standard output
        :return:
        """
        ctx = pytss.TspiContext()
        ctx.connect()

        tpm = ctx.get_tpm_object()
        cur = 0
        while self.count < 0 or cur < self.count:
            data = tpm.generate_random_data(self.bs)
            sys.stdout.write(data)
            sys.stdout.flush()
            cur += 1


def main():
    app = App()
    app.main()


if __name__ == '__main__':
    main()



