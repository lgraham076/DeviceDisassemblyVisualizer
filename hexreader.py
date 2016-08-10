#-------------------------------------------------------------------------------
# Name:        hexreader.py
# Purpose:     Converts file into hex dump
#
# Author:      Langston Graham
#
# Created:     08/14/2013
#-------------------------------------------------------------------------------

HEXLINELIMIT=16
HEXADDRESSWIDTH=8

#Converts given number to hex value with appropriate padding for display
def gethexaddress(intnum):
            hexaddress=hex(intnum*HEXLINELIMIT)
            hexaddress=hexaddress.replace('0x','')
            if(len(str(hexaddress)) < 8):
                diff=8-len(str(hexaddress))
                while(diff > 0):
                    hexaddress='0'+hexaddress
                    diff-=1
            return hexaddress

#Convert a string to a list of hex values
def tohexvalues(content):
    hexvalues=[]
    #Iterate through all characters in content
    for character in content:
        val=ord(character) #Translate to ascii value
        val=hex(val) #Translate to hex value

        val=val.replace('0x','') #Get rid of '0x'

        if(len(val) == 1):
            val=('0' + val) #Add a 0 to hex values with one digit

        hexvalues.append((val,character))

    return hexvalues

#Creates a list of 2d coordinates from the given hex values
def hexcoordinates2d(hexvalues):
    hexcoords=set()
    count=0
    while ((count + 1) < len(hexvalues)):
        x=int(hexvalues[count],16)
        y=int(hexvalues[count+1],16)
        hexcoords.add((x,y))

        count+=1

    return hexcoords

#Creates a list of 3d coordinates from the given hex values
def hexcoordinates3d(hexvalues):
    hexcoords=set()
    count=0
    while ((count + 2) < len(hexvalues)):
        x=int(hexvalues[count],16)
        y=int(hexvalues[count+1],16)
        z=int(hexvalues[count+2],16)
        hexcoords.add((x,y,z))

        count+=1

    return hexcoords


#Format a list of hex values to for display
def formathexvalues(hexvalues):
    hexlines=[]
    asciivals=[]
    hexline=''
    hexcount=0
    addresscount=0

    for value in hexvalues:
        hexline += value[0]
        asciivals.append(value[1])
        hexcount += 1
        #Limit the number of hex values to the specified limit and start new line
        if(hexcount == HEXLINELIMIT):
            #Add hexaddress
            hexline=gethexaddress(addresscount)+' | '+hexline+' | '

            for asciival in asciivals:
                if ord(asciival) == 0:
                    hexline = hexline + '..'
                else:
                    hexline = hexline + asciival

            hexlines.append(hexline)
            hexline=''
            hexcount=0
            addresscount+=1
            asciivals=[]
        else:
            hexline += ' '
    #Append any remaining values to list
    if(hexcount!=0):
        hexline=gethexaddress(addresscount)+' | '+hexline
        hexline=hexline[:-1]#Remove space if incomplete line
        hexlines.append(hexline)

    return hexlines

#Read given file and convert it to list of hex values
def readFile(fileName):
    hexvalues=[]
    try:
        file=open(fileName, encoding="latin-1")
    except FileNotFoundError:
        print ("File could not be found to get hexvalues!")
        return hexvalues
    else:
        content=file.read()
        hexvalues=tohexvalues(content)
        file.close()

        return hexvalues
