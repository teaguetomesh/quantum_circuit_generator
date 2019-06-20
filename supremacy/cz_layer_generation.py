import numpy as np
import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r','--rows',type=int,default=None,help='Number of rows')
    parser.add_argument('-c','--cols',type=int,default=None,help='Number of columns')
    args = parser.parse_args()
    return args


def cz_layer(nrow, ncol, starting_idx):
    # Store the qubit locations for this layer's CZs as an array of strings
    cz_list = []
    if starting_idx == 0 or starting_idx == 1:
        for row in range(0, nrow, 2):
            for col in range(0, ncol, 4):
                if col + starting_idx + 1 < ncol:
                    cz_list += ['{0},{1} {0},{2}'.format(row, col+starting_idx, col+starting_idx+1)]
                if col + starting_idx + 2 + 1 < ncol and row+1<nrow:
                    cz_list += ['{0},{1} {0},{2}'.format(row+1, col+starting_idx+2, col+starting_idx+3)]

    elif starting_idx == 2 or starting_idx == 3:
        for row in range(0, nrow, 2):
            for col in range(0, ncol, 4):
                if col + starting_idx - 2 + 1 < ncol and row+1<nrow:
                    cz_list += ['{0},{1} {0},{2}'.format(row+1, col+starting_idx-2, col+starting_idx-1)]
                if col + starting_idx + 1 < ncol:
                    cz_list += ['{0},{1} {0},{2}'.format(row, col+starting_idx, col+starting_idx+1)]

    elif starting_idx == 4 or starting_idx == 5:
        for col in range(0, ncol, 2):
            for row in range(0, nrow, 4):
                if row + starting_idx - 4 + 1 < nrow:
                    cz_list += ['{0},{1} {2},{1}'.format(row+starting_idx-4, col, row+starting_idx-3)]
                if row + starting_idx - 4 + 2 + 1 < nrow and col+1<ncol:
                    cz_list += ['{0},{1} {2},{1}'.format(row+starting_idx-2, col+1, row+starting_idx-1)]

    elif starting_idx == 6 or starting_idx == 7:
        for col in range(0, ncol, 2):
            for row in range(0, nrow, 4):
                if row + starting_idx - 4 - 2 + 1 < nrow and col+1<ncol:
                    cz_list += ['{0},{1} {2},{1}'.format(row+starting_idx-6, col+1, row+starting_idx-5)]
                if row + starting_idx - 4 + 1 < nrow:
                    cz_list += ['{0},{1} {2},{1}'.format(row+starting_idx-4, col, row+starting_idx-3)]

    return cz_list


def main():

    args = parse_args()

    with open('CZs_{}x{}.txt'.format(args.rows,args.cols), 'w') as fn:
        for i in range(8):
            cur_layer = cz_layer(args.rows, args.cols, i)

            print('A{}'.format(i))
            fn.write('A{}\n'.format(i))
            for layer in cur_layer:
                print(layer)
                fn.write(layer + '\n')
            print()
            fn.write('\n')


if __name__ == '__main__':
    main()
