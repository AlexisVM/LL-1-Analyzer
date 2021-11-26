##
#Alexis Vázquez
#Compiladores
#Generador de tablas LL(1)
##

#Initialize arrays, variables, bools and sets to be used
productions = []
strings = []
productionsParsed = {}
headers = []
terminals = []
FIRST = {}
FOLLOW = {}
last = ''
isLL = True
includesEpsilon = False
TABLEINDEX = {}

#Function to get non terminals or headers
def getHeaders():
    for i in range(0, len(productions)):
        #split the array into it's elements to obtain separate productions
        prod = productions[i].split()
        #check if the first element in the production is already a header, if not, add it to the list
        if prod[0] not in headers:
            headers.append(prod[0])

#Function to get terminals
def getTerminals():
    for i in range(0, len(productions)):
        #split the array into it's elements to obtain separate productions
        prod = productions[i].split()
        #another for loop iterates over the separated productions to add unique values to the array, also ignoring the arrow
        for j in range(0, len(prod)):
            if prod[j] not in headers and prod[j] not in terminals and prod[j] != "->" and prod[j] != "'":
                terminals.append(prod[j])   

#Funtion to parse productions
def parseProductions():
    #create sets for every header
    for header in headers:
        productionsParsed[header] = []

    #fill the sets for every header with the possible outcomes based in the grammar
    for production in productions:
        splitProd = production.split(" -> ")
        #remove '\n' that appears when reading file
        withoutBr = splitProd[1].split("\n")
        productionsParsed[splitProd[0]].append(withoutBr[0])

#Function to get the "first" generations
def getFirst(prod, auxprod):
    global includesEpsilon
    #start the "first" variable
    f = set()

    if prod == auxprod:
        global isLL
        isLL = False
        
    #Check if the production is part of the headers or non-terminals
    elif prod in headers:
        #Chech productions parsed to obtain array of individual productions based on header
        prodOptions = productionsParsed[prod]

        #Iterate over the different individual productions
        for prodOption in prodOptions:
            #Recursive method to check the next option in the terminals
            if prodOption != "' '":
                sp = prodOption.split(' ')
                fAux = getFirst(sp[0], prod)
                f = f | fAux
            else:
                fAux = getFirst("' '", prod)
                f = f | fAux

    #Check if the production is part of the terminals, the case where it returns the terminal       
    elif prod in terminals:
        f = {prod}
    
    #Check if the production is epsilon, if it's the case, return it but don't include it in the terminals
    elif prod == "' '" or prod == '@':
        f = {"' '"}
        includesEpsilon = True

    #Else case to iterate in composed productions
    else:
        splitted = prod.split(' ')
        fAux = getFirst(splitted[0], "auxprod")
            #check if epsilon is in the composed production, else return the current production
        if "' '" in fAux:
            includesEpsilon = True
            i = 1
            #Start cycle to iterate over the productions
            while "' '" in fAux:
                #From te auxiliary first, check for epsilon
                f = f | (fAux - {"' '"})
                #Check if terminal or end of composed production
                if splitted[i:] in terminals:
                    f = f | {splitted[i:]}
                    break
                elif splitted[i:] == '':
                    f = f | {"' '"}
                    break
                #Recursive method to ceck again the remaining productions by the same header
                fAux = getFirst(splitted[i:], "auxprod")
                f = f | fAux - {"' '"}
                i += 1
        else:
            f = f | fAux  

    return f

#Function to get the "follow" generations
def getFollow(header):
    #start the "follow" variable
    f = set()
    #get the key-value dictionary items
    prods = productionsParsed.items()
    #RULE 1, apply the special character to the first element
    if header == firstHeader:
        f = f | {'$'}
    for head,production in prods:
        #divide the productins in individual elements
        for singProd in production:
            #transform epsilon in a different character
            #if singProd == "' '":
            #    singProd = '@'
            splitted = singProd.split(" ")
            #search in individual symbols or characters
            for symb in splitted:
                #search for the following item if it matches the desired header
                if symb==header:
                    following = splitted[splitted.index(symb) + 1:]
                    #search if there are no more productions
                    if not following:
                        #RULE 3, if the head and the header match, continues, otherwise it would iterate over and over again
                        if head==header:
                            continue
                        #RULE 3, if they don't match, it gets the follow of the head
                        else:
                            f = f | getFollow(head)
                    else:
                        #RULE 2
                        f2 = getFirst(following[0], "auxprod")
                        #RULE 2 if the first of the following element is epsilon, remove it
                        if "' '" in f2:
                            f = f | f2-{"' '"}
                            f = f | getFollow(head)
                        #RULE 2, iterate over the getFirst() function to obtain the first of a header or return the terminal if it's the case
                        else:
                            f = f | f2                        
    
    return f

#Function to define LL rules
def LLRules():
    global isLL
    for header in headers:
        aux = []
        if (len(productionsParsed[header]) >= 2):
            for prod in productionsParsed[header]:
                splitted = prod.split()
                if splitted[0] in aux:
                    isLL = False
                aux.append(splitted[0])

#Function to check if it is ll
def getLL():
    return "yes" if isLL else "no"
    
#Function to receive an input file if the option number 1 is selected
def lexicalAnalyzerConsoleFile():
    #input file name
    fileName = input("\nFilename: ")
    #open file and handle error if file doesn't exists
    try:
        OFile = open(fileName, "r")
    except:
        print("File not found")
    
    lines = str(OFile.readline()).split()

    #Append the productions to the array "productions"
    for i in range(0, int(lines[0])):
        productions.append(OFile.readline())

    #Append the productions to the array "strings"
    for i in range(0, int(lines[1])):
        strings.append(OFile.readline())
    
#Function to receive the productions from an input if option 2 is selected
def lexicalAnalyzerConsoleCMD():
    productionsAmount = int(input("\nHow many productions are?(write them after) "))
    
    #Appending the input to the productions while reading them
    for i in range(0, productionsAmount):
        productions.append(input())
    
    stringsAmount = int(input("\nHow many tests are?(write them after) "))

    #Appending the strings to the test strings while reading them
    for i in range(0, stringsAmount):
        strings.append(input())

# lexical analyzer Function
def lexicalAnalyzer():
    #Execute the functions to find elements and productions
    getHeaders()
    getTerminals()
    parseProductions()

# first follows generator function
def firstFollows():

    #Start the First and Follow arrays with empty sets
    for header in headers:
        FIRST[header] = set()
    for header in headers:
        FOLLOW[header] = set()

    #fill the 'FIRST' set following the rules
    for header in headers:
        FIRST[header] = FIRST[header] | getFirst(header, "auxprod")
    
    #Prepare the default case for the first FOLLOW production
    FOLLOW[firstHeader] = FOLLOW[firstHeader] | {'$'}
    #fill the 'FOLLOW' set following the rules
    for header in headers:
        FOLLOW[header] = FOLLOW[header] | getFollow(header)

# validate html table cells function
def LLTableValidation(header, terminal):
    result = ""
    if terminal in FIRST[header]:
        for prod2 in productionsParsed[header]:
            splitted = prod2.split(' ')
            if splitted[0] in terminals:
                if splitted[0] == terminal:            
                    result = str(header) + " &#8594; " + str(prod2)
                    TABLEINDEX[header][terminal] = str(prod2)
                    break
            else:
                result = str(header) + " &#8594; " + str(prod2)
                TABLEINDEX[header][terminal] = str(prod2)
    elif includesEpsilon:
        if "' '" in FIRST[header]:
            if terminal in FOLLOW[header]:
                result = str(header) + " &#8594; " + "'  '"
                TABLEINDEX[header][terminal] = "' '"

    return result

# html generator function
def HTMLTableLL():

    for header in headers:
        TABLEINDEX[header] = {}
        for terminal in terminals:
            TABLEINDEX[header][terminal] = {}

    #After first and follows generation, append the $ character to the terminals
    terminals.append("$")

    #Create an HTML file called LLTable.html
    f = open('LLTable.html','w')

    #Create html header
    HTMLHeader = """<!DOCTYPE html>\n<html>\n\t<head align="center">\n\t\t<title>LL(1) Table Generator</title>\n\t</head>\n\t<body>\n\t\t<h2 align="center">LL(1) Table Generator</h2>\n\t\t<table width="728" cellspacing="2" cellpadding="0" border="0" align="center" bgcolor="#ff6600">"""

    #Create section and code for tables
    HTMLTableHeaders = """\n\t\t\t<tr bgcolor="#ffffff">\n\t\t\t\t<th width="240" height="45">Non Terminal</th>"""
    for i in terminals:
        HTMLTableHeaders += """\n\t\t\t\t<th width="240" height="45">""" + str(i) + """</th>"""

    HTMLTableHeaders += """
            </tr>"""

    HTMLTableRows = ""
    for i in headers:
        HTMLTableRows += """\n\t\t\t<tr bgcolor="#ffffff" align="center">"""
        HTMLTableRows += """\n\t\t\t\t<td height="67"><b>""" + str(i) + """</b></td>"""
        for j in terminals:
            HTMLTableRows += """\n\t\t\t\t<td height="67">""" + LLTableValidation(i,j) + """</td>"""
        HTMLTableRows += """\n\t\t\t</tr>"""

    HTMLTables = HTMLTableHeaders + HTMLTableRows + """\n\t\t</table>"""

    #Create section and code for tests
    HTMLTests = """\n\t\t<div align="center">"""
    for index, test in enumerate(strings):
        HTMLTests += """\n\t\t\t<p><b>Input #""" + str(index + 1) + " " + str(test) + " : " + stringValidation(test) +"</b> " + """</p>"""
    HTMLTests += """\n\t\t</div>"""

    HTMLFooter = """\n\t</body>\n</html>"""

    fullHTMLFile = HTMLHeader + HTMLTables + HTMLTests + HTMLFooter
    f.write(fullHTMLFile)
    f.close()

# html generator function
def HTMLTableLLWrong():
    #Create an HTML file called LLTable.html
    f = open('LLTable.html','w')

    #Create html header
    HTMLHeader = """<!DOCTYPE html>\n<html>\n\t<head align="center">\n\t\t<title>LL(1) Table Generator</title>\n\t</head>\n\t<body align="center">\n\t\t<h2>LL(1) Table Generator</h2>"""

    #Create section and code for tables
    HTMLImage = """<img src="https://www.respectmyregion.com/wp-content/uploads/2017/07/dwight-schrute-wrong.jpg" alt="Wrong Input">\n\t\t<p>Sorry :( the grammar entered is not LL(1) so a table can't be created and the given strings won't be tested.</p>"""

    HTMLFooter = """\n\t</body>\n</html>"""

    fullHTMLFile = HTMLHeader + HTMLImage + HTMLFooter
    f.write(fullHTMLFile)
    f.close()

# strings validation function
def stringValidation(test):
    input = test.split(' ')
    input.append('$')
    pila = ['$', headers[0]]  

    for loc, inp in enumerate(input):
        fixed = inp.split("\n")
        input[loc] = fixed[0]

    print("\nTest: " + str(test))
    while len(input) > 0:
        print(pila, '|\t', input)
        if str(pila[-1]) == str(input[0]):
            input.pop(0)
            pila.pop()
        elif len(pila) == 1 and pila[0] == '$' and len(input) > 0:
            return "Not Accepted"
        elif len(TABLEINDEX[pila[-1]][input[0]]) > 0:
            if TABLEINDEX[pila[-1]][input[0]] == "' '":
                pila.pop()
            else:
                aux2 = TABLEINDEX[pila[-1]][input[0]].split(' ')
                aux2.reverse()
                pila.pop()
                for element in aux2:
                    pila.append(element)
        else: 
            return "Not Accepted"
        

    return "Accepted"

# main function
def main():
    #Usage options
    print("LL(1) table Generator\n")
    print("This generator parses a grammar to validate different inputs\n")
    print("There are two ways of using the generator, from file and from command line")
    option = input("Select the option: (1. From file, 2. From command line.) ")
    if option == "1": 
        lexicalAnalyzerConsoleFile()
    else:
        lexicalAnalyzerConsoleCMD()

##      Start running

#Analyze inputs
main()

#Execute lexical analyzer function
lexicalAnalyzer()

#Find the first header to later be used in the "follows" part
firstHeader = headers[0]

#Execute the firstFollows function
firstFollows()

#Check the rules to know if the grammar is LL
LLRules()

if isLL:
    #Execute the LL(1)Table generator function
    HTMLTableLL()
    print("\nGreat! an HTML file called LLTable.html has been generated with the table data and the strings tested :)")
else:
    #Create an html showing a wrong input
    HTMLTableLLWrong()
    print("\nSorry :( the grammar entered is not LL(1) so a table can't be created and the given strings won't be tested. (still check the html file generated tho)")