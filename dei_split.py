#! /usr/bin/python2
""" Utility to split the electricity bill.
    Usage:
        python2 dei.py --help
"""

import argparse
import sys

MAX_ROOMMATES = 10
RECEIPT_COLWIDTH = 40

art = """
                zeeeeee-
                z$$$$$$"
               d$$$$$$"
              d$$$$$P
             d$$$$$P
            $$$$$$"
          .$$$$$$"
         .$$$$$$"
        4$$$$$$$$$$$$$"
       z$$$$$$$$$$$$$"
       """""""3$$$$$"
             z$$$$P
            d$$$$"
          .$$$$$"
         z$$$$$"
        z$$$$P
       d$$$$$$$$$$"
      *******$$$"
           .$$$"
          .$$"
         4$P"
        z$"
       zP
      z"
     /
    ^
"""

def init_parser():
    """ Set up arguement parser """
    _description = ("Utility to split the electricity bill among 2 or more "
                    "roommates, using non equal multipliers")

    parser = argparse.ArgumentParser(description=_description)

    parser.add_argument('-r', '--roommates', dest='n_roommates', type=int,
                        default=2, help="number of roommates (default: 2)")

    parser.add_argument('-d' '--deal', nargs='+', dest="deal", type=float,
                        default=[0.67, 0.33],
                        help="how the bill shall be split, in float numbers "
                             "adding up to 1 i.e. 0.6, 0.4. If a value is not "
                             "given, it will be filled in automatically "
                             "(default: 0.67 0.33)")
    parser.add_argument('-s' '--save', action='store_true', dest='save',
                        default=False, help="save a receipt.txt file")
    return parser


def process_input(args):
    """ Check input for errors and return the proceessed args"""

    # min roommates check
    if args.n_roommates < 2:
        raise Exception("n_roommates is (%d), we need at least 2" %
                        args.n_roommates)

    # global MAX_ROOMMATES check
    if args.n_roommates > MAX_ROOMMATES:
        raise Exception("n_roommates (%d) bigger than maximum allowed (%d)" %
                        (args.n_roommates, MAX_ROOMMATES))

    # n_roommates should match the length of deal or be one less
    if len(args.deal) == args.n_roommates:
        # ok, check if deal adds up to 1.0
        if round(sum(args.deal), 1) == 1.0:
            deal = args.deal
        else:
            raise Exception("deal (%.1f) must add up to 1.0" % sum(args.deal))

    # if one value is missing, we will fill it automatically
    elif len(args.deal) == args.n_roommates - 1:
        # Check that it has at least 0.01 overhead'
        if sum(args.deal) <= .99:
            deal = args.deal
            deal.append(1.0 - sum(deal))
        else:
            raise Exception("sum of deal (%.1f) is too high, cannot fill" %
                            sum(args.deal))

    else:
        raise Exception("n_roommates (%d) and deal values (%d) do not "
                        "match" % (args.n_roommates, len(args.deal)))

    return args.n_roommates, deal


def test():
    """ Simple tests for the utility """
    # pylint: disable-all
    import random

    # test correct input is ok where n_roommates == len(deal)
    n_rand = random.randrange(2, MAX_ROOMMATES + 1)
    deal = [str(1.0/n_rand) for i in range(n_rand)]    # equal distribution
    params = '-r %d -d %s' % (n_rand, ' '.join(deal))
    args = init_parser().parse_args(params.split())
    try:
        process_input(args)
    except Exception as e:
        raise Exception("Failed for correct input, msg: %s" % str(e))

    # test automatic fill of deal
    n_rand = random.randrange(2, MAX_ROOMMATES + 1)
    deal = [str(1.0/n_rand) for i in range(n_rand-1)]    # equal distribution
    params = '-r %d -d %s' % (n_rand, ' '.join(deal))
    args = init_parser().parse_args(params.split())
    try:
        process_input(args)
    except Exception as e:
        raise Exception("Failed to close deal, msg: %s" % str(e))

    # test n_roommates, deal mismatch
    n_rand = random.randrange(2, MAX_ROOMMATES + 1)
    deal = [str(1.0/n_rand) for i in range(n_rand-2)]    # equal distribution
    params = '-r %d -d %s' % (n_rand, ' '.join(deal))
    args = init_parser().parse_args(params.split())
    try:
        process_input(args)
    except Exception as e:
        msg = "do not match"
        assert msg in str(e), "'%s' not in '%s'" % (msg, str(e))
    else:
        raise Exception("incompatible n_roommates and len(deal) did not "
                        "raise an error")

    # test wrong deal sum, bigger
    n_rand = random.randrange(2, MAX_ROOMMATES + 1)
    deal = [str(1.0/n_rand) for i in range(n_rand)]    # equal distribution
    deal[-1] = str(float(deal[-1]) + 0.1)
    params = '-r %d -d %s' % (n_rand, ' '.join(deal))
    args = init_parser().parse_args(params.split())
    try:
        _, d = process_input(args)
        print(sum(d))
    except Exception as e:
        msg = "must add up to"
        assert msg in str(e), "'%s' not in '%s'" % (msg, str(e))
    else:
        raise Exception("sum bigger than 1.0 did not raise an error")

    # test wrong deal sum, lower
    n_rand = random.randrange(2, MAX_ROOMMATES + 1)
    deal = [str(1.0/n_rand) for i in range(n_rand)]    # equal distribution
    deal[-1] = str(float(deal[-1]) - 0.1)
    params = '-r %d -d %s' % (n_rand, ' '.join(deal))
    args = init_parser().parse_args(params.split())
    try:
        _, d = process_input(args)
        print(sum(d))
    except Exception as e:
        msg = "must add up to"
        assert msg in str(e), "'%s' not in '%s'" % (msg, str(e))
    else:
        raise Exception("sum lower than 1.0 did not raise an error")

    # test wrong deal sum, in autofill
    n_rand = random.randrange(2, MAX_ROOMMATES + 1)
    deal = [str(1.0/n_rand) for i in range(n_rand-1)]    # equal distribution
    deal[-1] = str(float(deal[-1]) * 2)
    params = '-r %d -d %s' % (n_rand, ' '.join(deal))
    args = init_parser().parse_args(params.split())
    try:
        _, d = process_input(args)
        print(sum(d))
    except Exception as e:
        msg = "too high"
        assert msg in str(e), "'%s' not in '%s'" % (msg, str(e))
    else:
        raise Exception("Wrong deal sum in autofill did not raise an error")

    # pylint: enable-all


def loop():
    values = []
    while True:
        targ = raw_input("(value), (n) for next mode, (r) to restart, "
                         "(q) to quit\n")
        if targ.lower() == 'q':
            print("Bye!!!")
            sys.exit(0)

        if targ.lower() == 'r':
            return 1, values

        if targ.lower() == 'n':
            return 0, values

        else:
            try:
                values.append(float(targ))
            except:
                print "Please give only numerical input the next time!"


def report(values_eq, values_dl, n_roommates, deal, verbose=False):
    if verbose:
        print "========== PAYMENT REPORT =========="
        print("Total amount to be paid: %.2f" % (sum(values_eq) +
                                                 sum(values_dl)))
    to_pay_eq = sum(values_eq) / float(n_roommates)
    sum_values_dl = sum(values_dl)
    msg_all = ''
    for i, ratio in enumerate(deal):
        to_pay = sum_values_dl * ratio
        total = to_pay_eq + to_pay
        msg = "Roomie n.%d with deal ratio %.2f will pay:\n"
        msg += "%.2f for the equal share and "
        msg += "%.2f according to the deal.\n"
        msg += "\tTOTAL: %.2f\n\n"
        if verbose:
            print msg %(i+1, ratio, to_pay_eq, to_pay, total)
        msg_all += msg %(i+1, ratio, to_pay_eq, to_pay, total)
    return msg_all


def main():
    """ Main loop """
    args = init_parser().parse_args()
    n_roommates, deal = process_input(args)
    print "Welcome to the electricity bill splitter."
    print(art)
    sys.stdout.write("First, ")
    bills = []
    while True:
        id = raw_input("please enter an ID for this bill\n")
        print "enter the values that should be split equally:"
        opcode, values_eq = loop()
        if opcode == 1:
            continue
        print "enter the values that should be split according to the deal"
        opcode, values_dl = loop()
        if opcode == 1:
            continue

        report(values_eq, values_dl, n_roommates, deal)

        bills.append((id, values_eq, values_dl))

        more = raw_input("Do you want to continue? [y, n]\n")
        if more.lower() =='y':
            continue
        else:
            print "Bye!!!"
            break

    # import pdb; pdb.set_trace()
    if bills and args.save:
        total_eq, total_dl = [], []
        out = "RECEIPT FOR ELECTRICITY BILL\n"
        out += ('=' * RECEIPT_COLWIDTH) + '\n\n'
        for id, values_eq, values_dl in bills:
            total_eq.extend(values_eq)
            total_dl.extend(values_dl)
            out += (RECEIPT_COLWIDTH * '-') + '\n'
            out += '--- %s ' % id
            out += (RECEIPT_COLWIDTH - 5 - len(id)) * '-'
            out += '\n'
            out += (RECEIPT_COLWIDTH * '-') + '\n'
            out += "equal splits "
            out += ((RECEIPT_COLWIDTH / 2) - 14) * '-'
            out += '|'
            out += "deal splits "
            out += ((RECEIPT_COLWIDTH / 2) - 12) * '-'
            out += '\n'

            # Fill with blanks so both arrays have the same length
            len_eq = len(values_eq)
            len_dl = len(values_dl)
            if len_eq > len_dl:
                values_dl.extend([0.0 for i in range(len_eq-len_dl)])
            elif len_eq < len_dl:
                values_eq.extend([0.0 for i in range(len_eq-len_dl)])

            for eq, dl in zip(values_eq, values_dl):
                if eq == 0.0:
                    eq = ''
                out += str(eq)
                out += ((RECEIPT_COLWIDTH / 2) - len(str(eq)) - 1) * ' '
                out += '|'
                if dl == 0.0:
                    dl = ''
                out += str(dl)
                out += ((RECEIPT_COLWIDTH  / 2) - len(str(dl))) * ' '
                out += '\n'

            out += ((RECEIPT_COLWIDTH / 2) - 6) * ' '
            out += 'total|'
            out += ((RECEIPT_COLWIDTH / 2) - 6) * ' '
            out += 'total\n'

            sum_eq, sum_dl = str(sum(values_eq)), str(sum(values_dl))
            out += ((RECEIPT_COLWIDTH / 2) - len(sum_eq) - 2) * ' '
            out +=  sum_eq + ' |'
            out += ((RECEIPT_COLWIDTH / 2) - len(sum_dl) - 1) * ' '
            out +=  sum_dl + '\n\n'

            out += "Payments:\n"
            out += report(values_eq, values_dl, n_roommates, deal, False)
            out += '\n\n'


        out += '\n SUM FOR %d BILLS:\n' % len(bills)
        out += report(total_eq, total_dl, n_roommates, deal, False)
        with open('receipt.txt', 'w') as file:
            file.write(out)


    return 0


if __name__ == "__main__":
    sys.exit(main())
