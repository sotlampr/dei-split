#! /usr/bin/python2
""" Utility to split the electricity bill.
    Usage:
        python2 dei.py --help
"""

import argparse
import sys

MAX_ROOMMATES = 10

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


def report(values_eq, values_dl, n_roommates, deal):
    print "========== PAYMENT REPORT =========="
    print("Total amount to be paid: %.2f" % (sum(values_eq) + sum(values_dl)))
    to_pay_eq = sum(values_eq) / float(n_roommates)
    sum_values_dl = sum(values_dl)
    for i, ratio in enumerate(deal):
        to_pay = sum_values_dl * ratio
        total = to_pay_eq + to_pay
        msg = "Roomie n.%d with deal ratio %.2f will pay:\n"
        msg += "%.2f for the equal share and "
        msg += "%.2f according to the deal.\n"
        msg += "\tTOTAL: %.2f\n"
        print msg %(i+1, ratio, to_pay_eq, to_pay, total)


def main():
    """ Main loop """
    args = init_parser().parse_args()
    n_roommates, deal = process_input(args)
    print "Welcome to the electricity bill splitter."
    print(art)
    sys.stdout.write("First, ")
    while True:
        print "enter the values that should be split equally:"
        opcode, values_eq = loop()
        if opcode == 1:
            continue
        print "enter the values that should be split according to the deal"
        opcode, values_dl = loop()
        if opcode == 1:
            continue

        report(values_eq, values_dl, n_roommates, deal)

        more = raw_input("Do you want to continue? [y, n]")
        if more.lower() =='y':
            continue
        else:
            print "Bye!!!"
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
