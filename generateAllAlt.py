#!/usr/bin/env python3
#
# Will generate a CSV with all Latitudes
import csv
import os

def writeFile(directory, filename, filenameExtension, data, count):
    csvFilename = os.path.join(directory, "%s-%s.%s"%(filename, count, filenameExtension))
    with open(csvFilename, 'w', newline='') as csvfile:
        output = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output.writerow(['altitude'])
        for row in data:
            output.writerow([row])
        csvfile.close()
        return "{'csv':'%s', 'out':'%s-%s.iq8s'},"%(csvFilename, filename, count)

def main():
    directory = 'generated'
    filename = 'allAlt'
    filenameExtension = 'csv'
    scriptFilename = 'allAlt.py'
    hackRFScriptFilename = 'hackRFAllAlt.sh'

    minAlt = -1100
    maxAlt = 100000
    splitNumber = 1000
    step = 1

    try:
        os.stat(directory)
    except:
        os.mkdir(directory) 

    script = open(scriptFilename, 'w')
    script.write('#!/usr/bin/env python3\n')
    script.write('import time\n')
    script.write('import threading\n')
    script.write('from ADSB_Encoder import *\n')

    hackRFScript = open(hackRFScriptFilename, 'w')
    hackRFScript.write('#!/bin/bash\n')
    
    
    i = minAlt
    j = 0
    k = 0
    data = []
     
    files = ''
    while i <= maxAlt:
        if j == splitNumber:
            files += writeFile(directory, filename, filenameExtension, data, k)
            data = []
            hackRFScript.write("hackrf_transfer -t %s-%s.iq8s -f 915000000 -s 2000000 -x 10\n" % (filename, k))
            k += 1
            j = 0            
        data.append(i)
        i += step
        j += 1
    files += writeFile(directory, filename, filenameExtension, data, k)
    data = []
    hackRFScript.write("hackrf_transfer -t %s-%s.iq8s -f 915000000 -s 2000000 -x 10\n" % (filename, k))
    k += 1
    j = 0    
    files = files[:-1]
    script.write('files = [%s]\n' % (files))
    script.write('for file in files:\n')
    script.write('    t = threading.Thread(target=threadingCSV, args=(file,))\n')
    script.write('    t.start()\n')
    script.write('    print(file)\n')
    script.write('    time.sleep(1)\n')
    script.close()
    hackRFScript.close()

if __name__ == "__main__":
    main()

    
		
