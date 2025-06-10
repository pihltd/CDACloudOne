import requests
import json
import pandas as pd
from crdclib import crdclib
import argparse
import pprint



def apiRequest(url):

    #headers = {'Content-Type: application/json'}
    
    try:
        result = requests.get(url = url)
        if result.status_code == 200:
            return result.json()
        else:
            print(f"Error: {result.status_code}")
            return result.content
    except requests.exceptions.HTTPError as e:
        return(f"HTTP Error: {e}")


def main(args):
    configs = crdclib.readYAML(args.configfile)
    
    #column query
    docsjson = apiRequest(configs['dev_url']+'columns')
    #pprint.pprint(docsjson)
    #columns = {'column', 'data'}
    resultlist = docsjson['result']
    #for result in resultlist:
    #    print(result)
    col_df = pd.DataFrame(resultlist)
    print(col_df.head())
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configfile", required=True,  help="Configuration file containing all the input info")
    parser.add_argument("-v", "--verbose", help="Verbose Output")

    args = parser.parse_args()

    main(args)
