import logging
def create_logger():
    try:
        
        with open(a:='cortexoa.log', 'x'):
            pass  
        
        logging.basicConfig(filename=a, level=logging.INFO)
    
    except OSError as e:
        logging.error(f"{e}: occurred while creating logger")
    return a 