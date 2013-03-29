# coding: utf-8

def merge_escaped(args):
    new_args = []
    i = 0
    merge = False
    while i < len(args):
        if args[i].startswith('"'):
            merged = args[i][1:]
            merge = True
        elif args[i].endswith('\\'):
            merged = args[i][0:-1]
            merge = True

        if not merge:
            new_args.append(args[i])
            i += 1
        else:
            i += 1
            while merge and i < len(args):
                if args[i].endswith('"'):
                    next_arg = args[i][0:-1]
                    merge = False
                elif args[i].endswith('\\'):
                    next_arg = args[i][0:-1]
                elif not args[i].endswith('\\'):
                    next_arg = args[i]
                    merge = False
                else:
                    next_arg = args[i]

                merged += ' '
                merged += next_arg
                i += 1

            new_args.append(merged)

    return new_args
