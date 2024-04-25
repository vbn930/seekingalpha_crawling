from Manager import DriverManager
from Utility import LoginModule
from Utility import Util
import atexit
import seekingalpha_crawler

#pyinstaller -n "SeekingAlpha Crawler ver1.0" --clean --onefile main.py

def main():
    logger = Util.Logger("Build")
    logger.log(log_level="Event", log_msg=f"=SeekingAlpha Crawler ver1.0=")
    crawler = seekingalpha_crawler.SeekingAlpha_Crawler(logger)
    #crawler.start_crawling()
    try:
        crawler.start_crawling()
        return
    except Exception as e:
        logger.log(log_level="Error", log_msg=e)
    finally:
        exit_program = input("Press enter key to exit the program")

main()