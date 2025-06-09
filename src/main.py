from copy_static import *
import sys

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    clear_directory("docs/")
    copy_directory("static/","docs/")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()