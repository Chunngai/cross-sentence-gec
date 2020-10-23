import sys
import matplotlib.pyplot as plt
import argparse

from get_losses import get_losses

def compare_losses(losses_list, from_epoch, to_epoch, texts):
    for y, text in zip(losses_list, texts):
        x = [i for i in range(len(y))][from_epoch:to_epoch+1]
        y = y[from_epoch:to_epoch+1]
        
        plt.plot(x, y, label=text)
        plt.legend()
        for x_, y_ in zip(x, y):
            if x_ % 3 == 0:
                plt.text(x_, y_, f"{y_:.2f}", ha="center", va="bottom", fontsize=8)
        #plt.text(x_, y_, text, ha="center", va="bottom", fontsize=8)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--from-epoch", default=0, type=int)
    parser.add_argument("-t", "--to-epoch", default=100, type=int)
    parser.add_argument("-l", "--logs", nargs="+")

    args = parser.parse_args()

    train_n_valid_losses_list = [get_losses(log_file) for log_file in args.logs]

    plt.subplot(1, 2, 1)
    compare_losses([t[0] for t in train_n_valid_losses_list], args.from_epoch, args.to_epoch, args.logs)
    plt.subplot(1, 2, 2)
    compare_losses([t[1] for t in train_n_valid_losses_list], args.from_epoch, args.to_epoch, args.logs)
    plt.show()
