from tqdm import tqdm


class TqdmStream:
    @staticmethod
    def write(msg):
        tqdm.write(msg, end="")

    @staticmethod
    def flush():
        return
