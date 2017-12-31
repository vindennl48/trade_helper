# Create Table in Terminal


def st_bar(size):
    result = "";
    for x in range(size-1):
        result += "="
    result += '\n'
    return result

# Spaces: [8,5,5,4]
#  |--------|-----|-----|----|
#
def st_divide(spaces):
    result = "|-"
    for x in range(len(spaces)):
        for y in range(spaces[x]):
            result += "-"
        result += "-|-"
    result = result[:-1]
    result += '\n'
    return result

def st_width(spaces, value, align='left'):
    if align == 'left':
        result = " "
        for x in range(spaces):
            if value[x:(x+1)] != '':
                result += value[x:(x+1)]
            else:
                result += " "
        result += " "
    elif align == 'right':
        result  = ""
        padding = " "
        for x in range(spaces):
            if value[x:(x+1)] != '':
                result += value[x:(x+1)]
            else:
                padding += " "
        result = padding + result + " "
    return result

# Content: [[8,val1,align],[5,val2,align],[5,val3,align],[4,val4,align]]
#  | val    | val | val | va |
def st_row(content):
    result = "|"
    for x in range(len(content)):
        spaces = content[x][0]
        value  = content[x][1]
        try:
            align = content[x][2]
        except:
            align = 'left'
        result += st_width(spaces,value,align)
        result += "|"
    result += '\n'
    return result

# Widths: [4,6,5,7]
# Content: [ ['Bank', balance0], ['Coins', balance1, 'right'] ]
def st_build(w, content):
    rows = []
    row_count = 0
    result = ""

    for x in range(len(content)):         # row
        row = ""
        rdata = []
        for y in range(len(content[x])):  # column
            cdata = [w[y]]
            cdata.append(content[x][y][0])
            try:
                cdata.append(content[x][y][1])
            except:
                cdata.append('left')
            rdata.append(cdata)
        row += st_row(rdata)
        row_count = len(row)
        rows.append(row)

    bar = st_bar(row_count)
    div = st_divide(w)

    result += bar
    for x in range(len(rows)):
        result += rows[x]
        if x != (len(rows)-1):
            result += div
    result += bar
    print(result.rstrip())


if __name__ == "__main__":
    st_build(
        [8,8,8,8],
        [[ ['Bank',  'left'], ['97.23',  'right'], [''],    ['']               ],
         [ ['Coins', 'left'], ['147.12', 'right'], [''],    ['']               ],
         [ ['Start', 'left'], ['96.23',  'right'], ['End'], ['98.23', 'right'] ]]
    )


