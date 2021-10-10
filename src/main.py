import importlib
import sys


if __name__ == "__main__":
    # target_module_name = input("module?:")
    # target_module_name = "series001.main"
    target_module_name = sys.argv[1]

    target_module = importlib.import_module(target_module_name)

    target_module.main() #type:ignore



