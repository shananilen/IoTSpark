import argparse
import os
import core.ip
import importlib

MODULES_DIR = "toolkit"


def fancy_header():
    print(r"""------------------------------------------------------------------------------


██  ██████  ████████     ███████ ██████   █████  ██████  ██   ██ 
██ ██    ██    ██        ██      ██   ██ ██   ██ ██   ██ ██  ██  
██ ██    ██    ██        ███████ ██████  ███████ ██████  █████  
██ ██    ██    ██             ██ ██      ██   ██ ██   ██ ██  ██ 
██  ██████     ██        ███████ ██      ██   ██ ██   ██ ██   ██ 
                                               

------------------------------------------------------------------------------
""")


def available_modules():
    blacklisted_files = ["__init__.py"]
    modules = [m[:-3] for m in os.listdir(MODULES_DIR)
               if m.endswith(".py") and m not in blacklisted_files]
    modules.sort()
    mod_str = "available modules:\n  "
    mod_str += ", ".join(modules)
    return mod_str


def parse_arguments():
    parser = argparse.ArgumentParser(description="Attacking framework for Smart Home Appliance ".format(
        fancy_header()), formatter_class=argparse.RawDescriptionHelpFormatter, epilog=available_modules())
    parser.add_argument("module", help="Name of the module to run")
    parser.add_argument("module_args", metavar="...",
                        nargs=argparse.REMAINDER, help="Arguments to module")
    parser.add_argument("-ip", dest="ip_addres", default=None,
                        help="Destination IP address", type=str)

    args = parser.parse_args()
    return args


def load_module(module_name):
    clean_mod_name = os.path.basename(module_name)
    package = "{0}.{1}".format(MODULES_DIR, clean_mod_name)
    try:
        py_mod = importlib.import_module(package)
        return py_mod
    except ImportError as e:
        print(str(e))
        return None


def main():
    args = parse_arguments()
    if args.ip_addres:
        core.ip.DEFAULT_IP = args.ip_addres

    #load_module(args.module)
    mod = load_module(args.module)
    if mod is not None:
        func_name = "module_main"
        func_exists = func_name in dir(mod) and callable(getattr(mod, func_name))
        if func_exists:
            # Run module, passing any remaining arguments
            mod.module_main(args.module_args)
        else:
            # Print error message if module_main is missing
            print("ERROR: Module '{0}' does not contain a '{1}' function.".format(args.module, func_name))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n stoped!")

    finally:
        print("")
        print("\n")
        print("To View each modules' Help instructions use -h along with the module")
        print("Example: pyhon3 frame.py <module_name> -h")
        print("\n\n")
