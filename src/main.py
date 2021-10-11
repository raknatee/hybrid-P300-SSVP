import importlib
import sys


if __name__ == "__main__":
    print("""******\nargs=> python_module target_function *target_func_args\n******\n\n""")

    target_module_name = sys.argv[1]

    target_module = importlib.import_module(target_module_name)

    target_func = getattr(target_module,sys.argv[2])
    
    target_func(*sys.argv[3:]) #type:ignore



