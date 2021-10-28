import importlib
import sys



def main():
    target_module_name = sys.argv[1]

    target_module = importlib.import_module(target_module_name)

    target_func = getattr(target_module,sys.argv[2])
    
    target_func(*sys.argv[3:]) #type:ignore

class ArgsNotFound(RuntimeError):
    
    def __str__(self) -> str:
        return """\n******\nargs=> python_module target_function *target_func_args\n******
Ex:
    pipenv run python main.py series002.ssvp_chaky.main main
    pipenv run python main.py series002.main            ssvp A06S01"""



if __name__ == "__main__":
    if(len(sys.argv)<=1 ):
        raise ArgsNotFound()
    main()
  
