import re
import sys
import csv

if len(sys.argv) > 1:
# open input file
    input_file = sys.argv[1]
    f = open(input_file, "r")
    body = f.read()
else:
    print "usage: %s input_file" % sys.argv[0]
    sys.exit(1)

# remove KEY: .... source of the report
body_wo_key = re.sub("KEY:\s+.*?source of the report\.", "", body, flags=re.DOTALL)

# make pages by \x0c character
pages = re.findall("(.*?\x0c)", body_wo_key, flags=re.DOTALL)

# grab the Property Snapshot
property_snap = re.findall("[Pp]roperty\s+[Ss]napshot\n(.*?)\w+\'s\s+Auctions", pages[0], flags=re.DOTALL)
property_snap_value = re.findall("(.*)These auction results", pages[0], flags=re.S)

# remove unneccessary header text
pages[0] = re.sub(".*\'s Auctions", "", pages[0], flags=re.DOTALL)

re_end_words = "(?:\nType\n|\nPrice\n|\nResult\n|\nAgent\n|\x0c)"

m_address = re.compile("^[a-zA-Z]?\d.*?\s+\w{3,}.*$")

items = []
for p in pages:
    suburbs = []
    addresses = []
    section_suburb_address = re.findall("(?:[Ss]uburb\n[Aa]ddress|[Aa]ddress\n[Ss]uburb)\n(.*?)%s" % re_end_words, p, flags=re.DOTALL)

    for x in "".join(section_suburb_address).split("\n"):
        if m_address.match(x):
            addresses.append(x)
        else:
            if x:
                suburbs.append(x)

    section_type = re.findall("(?:[Tt]ype)\n(.*?)%s" % re_end_words, p, flags=re.DOTALL)
    section_price = re.findall("(?:[Pp]rice)\n(.*?)%s" % re_end_words, p, flags=re.DOTALL)
    section_result = re.findall("(?:[Rr]esult)\n(.*?)%s" % re_end_words, p, flags=re.DOTALL)
    section_agent = re.findall("(?:[Aa]gent)\n(.*?)%s" % re_end_words, p, flags=re.DOTALL)

    types = [ x for x in "".join(section_type).split("\n") if x ]
    prices = [ x for x in "".join(section_price).split("\n") if x ]
    results = [ x for x in "".join(section_result).split("\n") if x ]
    agents_1 = [ x for x in "".join(section_agent).split("\n") if x ]

    i_agents_1 = iter(agents_1)
    agents = []

    for a in i_agents_1:
        try:
            while a[-1] == " ":
                n = next(i_agents_1)
                a = a + n
        except: 
            pass
            
        agents.append(a)

    items.append([suburbs, addresses, types, prices, results, agents])


csv_items = [ m for i in items for m in map(None, i[0:6]) ]

# write to csv file
headers = ["Suburb", "Address", "Type", "Price", "Result", "Agent"]
with open(input_file+".csv","w") as f:
    writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(headers)

    for i in csv_items:
        writer.writerow(i)


