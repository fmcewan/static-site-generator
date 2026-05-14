import os
import shutil

from copy import copy_directory 

dir_path_static = "static"
dir_path_public = "public"

def main():

    copy_directory(dir_path_static, dir_path_public)

main()
