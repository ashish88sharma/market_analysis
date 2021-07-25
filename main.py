''' this code downloads delivery data of today. it is assumed to be working on windows
so, downloaded file goes to downloaded. It then renames this file and move it to
our target folder for further processing'''

from download_required_data import *
from delivery_analysis import *

def main():
    date_value = create_dir()
    status = getfiles(date_value)
    if status == 0:
        print("exiting because file not downloaded")
    else:
        read_files(date_value)
    print("Exit")    
    
    
if __name__ == "__main__":
    main()
