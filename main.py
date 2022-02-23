from re import split
import datetime
from classes.webBot import Webbot
from utils.myListsFuncs import countItems
from utils.myargsParser import myArgs
import validators

# Main
if __name__ == "__main__":
    # Default main method to begin the web scrapper
    def main(m, d, inp):
        try:
            # Check the input urls
            for j in inp:
                if not validators.url(j):
                    raise ValueError(
                        'Please check the urls.')
            print("\n -- Web Bot Started -- \n")
            # Input Url or Urls
            input = inp
            # set Depth - how far from original url
            depth = d
            # Algorithm to use
            method = m
            # Create our bots and begin web crawler
            begin_time = datetime.datetime.now()
            for i in input:
                if method == "bfs":
                    bot = Webbot()
                    bot.bfs(i, depth)
                    bot.botCompletedStatus()
                    if bot.errors:
                        #print("db errorss")
                        #print(bot.errors)
                        bot.saveErrorsToDbLog()
                elif method == 'dfs':
                    bot = Webbot()
                    print("\n -- DFS Started -- \n")
                    print(f"Starting from: {i} \n")
                    bot.dfs(i, depth)
                    print("\n -- DFS Completed -- \n")
                    bot.closeDriver()
                    bot.botCompletedStatus()
                    print(countItems(bot.dfs_depth_summary))
                    print()
                    if bot.errors:
                        #print(bot.errors)
                        bot.saveErrorsToDbLog()
                else:
                    raise ValueError(
                        'Must specify proper method ["bfs" or "dfs"].')
            print(
                f" -- Execution time: {datetime.datetime.now() - begin_time} --")
            print("\n -- Web Bot Completed -- \n")
        except Exception as ex:
            #bot.saveErrorsToDbLog(ex)
            print(f"Exception from main: {ex}")
            

    # Check if passed valid args and start the right command
    try:
        args = myArgs()
        if ((args.method is not None) and (args.depth is not None and args.depth > 0) and (args.urls is not None)):
            urls = []
            for i in args.urls:
                urls = i.split(',')
            main(args.method, args.depth, urls)
        else:
            raise ValueError(
                'Please check your args. Check --help for help.')
    except Exception as ex:
        print(ex)
