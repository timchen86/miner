import re
import sys

# open input file
f = open("1.txt", "r")
body = f.read()

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

for i in items:
    for s,adr,t,p,r,ag in map(None, i[0],i[1],i[2],i[3],i[4],i[5]):
        print "%s,%s,%s,%s,%s,%s" % (s,adr,t,p,r,ag)

