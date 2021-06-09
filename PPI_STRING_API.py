
# https://string-db.org/help/api/

######## first get the mapping IDs in order for the server to understand query
import requests

import csv

my_genes = ["HRAS", "BRAF", "KRAS", "MAP2K1"]
##string_api_url = "https://string-db.org/api"
##output_format = "tsv-no-header"
##method = "get_string_ids"
##
##params = {
##
##    # top five genes curated for association with five specific RASopathy conditions
##    # that were found to be definitive 
##    "identifiers" : "\r".join(my_genes), # your protein list
##    "species" : 9606, # species NCBI identifier: human 
##    "limit" : 1, # only one (best) identifier per input protein
##    "echo_query" : 1, # see your input identifiers in the output
##    "caller_identity" : "Sara Zhang - regular uwer" # your app name
##    }
### request method requires data to be dictionary that stores some keys and some values to be sent to the spcific URL
### what is caller identity for though?? 
### what happens if I commented out that line?? 
##
##request_url = "/".join([string_api_url, output_format, method])
##results = requests.post(request_url, data = params)
##
##my_genes_id = []
##for line in results.text.strip().split("\n"):
##	l = line.split("\t")
##	input_identifier, string_identifier = l[0],l[2]
##	print("input", input_identifier, "string", string_identifier, sep = "\t")
##	my_genes_id.append(l[2])

######## then get their interactions
##string_api_url = "https://string-db.org/api"
##output_format = "tsv-no-header"
##method = "network"
##request_url = "/".join([string_api_url, output_format, method])
##
##
##params1 = {
##
##    "identifiers" : "%0d".join(my_genes), # your protein
##    "species" : 9606, # species NCBI identifier 
##    "caller_identity" : "Sara Zhang - regular user" # your app name
##
##}
##
##response = requests.post(request_url, data=params1)
##
##for line in response.text.strip().split("\n"):
##
##    l = line.strip().split("\t")
##    p1, p2 = l[2], l[3]
##
##    ## filter the interaction according to experimental score
##    experimental_score = float(l[10])
##    if experimental_score > 0.4:
##        ## print 
##        print("\t".join([p1, p2, "experimentally confirmed (prob. %.3f)" % experimental_score]))
##
### this outputs all the probabilities between each pair of genes that I selected


###################### get all the STRING interaction partners of the protein set (not just in between, but theri neighbors)

string_api_url = "https://string-db.org/api"
output_format = "tsv-no-header"
method = "interaction_partners"


##
## Construct the request
##

request_url = "/".join([string_api_url, output_format, method])

##
## Set parameters
##

params = {

    "identifiers" : "%0d".join(my_genes), # your protein
    "species" : 9606, # species NCBI identifier 
    "limit" : 5,
    "caller_identity" : "www.awesome_app.org" # your app name

}

##
## Call STRING
##

response = requests.post(request_url, data=params)

##
## Read and parse the results
##

with open('replies.csv', 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=('query', 'partner','score'))
        csv_writer.writeheader()
        for line in response.text.strip().split("\n"):

            l = line.strip().split("\t")
            query_ensp = l[0]
            query_name = l[2]
            partner_ensp = l[1]
            partner_name = l[3]
            combined_score = l[5]

            ## print

            print("\t".join([query_ensp, query_name, partner_name, combined_score]))
            row = {'query': query_name, 'partner': partner_name, 'score': combined_score}
            csv_writer.writerow(row)
    


