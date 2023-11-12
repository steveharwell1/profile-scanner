def main() -> None:
    """
    Should only run from the command line
    Will read from the command line and start the scraper in the
    user selected mode.
    """
    # read command line controls implemented with [argparse]
	  
    # https://docs.python.org/3/library/argparse.html
    print('Hello from __main__.py')
	
def automatic():
    ## todo setup resources
    #crawler.scanprofiles()
    pass

def search_text(text):
    #crawler.fromSearch(text)
    pass

def add_names(file):
    ## todo setup resources
    # for id in ids:
    #     storage.save_blank_profile_if_unknown(id)
    pass

def update_profile(id):
    ## todo setup resources
    #crawler.scanprofile(id)
    pass

def get_person(id, filename):
    ## todo setup resources
    #storage.to_xlsx(id, filename)
    pass

def get_profiles(filename):
    ## todo setup resources
    #storage.to_xlsx(None, filename)
    pass

if __name__ == '__main__':
    main()