#!/usr/bin/env python3
#
# Cesar Olvera 2020, 2022
#

"""
Usage: python3 rfc_relationships.py [-di] [-h] [-v]

optional arguments:
    -di, --downloadIndex  Download current official RFC Index from
                          "http://www.ietf.org/download/rfc-index.txt",
                          if this option is not included, then use a
                          local RFC index downloaded previously.
    -h, --help            Show this help message and exit.
    -v, --version         Show program's version number and exit.


Input:  One file "my-rfc-list.txt" with the list of RFCs you want to verify.
        It has a list of RFCs specified as RFCXXXX or XXXX,
        and separated with new line (\n) or comma (,).

Output: Three files:
        - "rfc-analysis.txt"  with analysis of all RFCs with their information,
           and stating if they are "Obsoleted" or "Updated".
        - "rfc-obsoleted.txt" with the list of obsoleted RFCs.
        - "rfc-updated.txt"   with the list of updated RFCs.


From RFC 7841:
   [<RFC relation>:<RFC number[s]>]  Some relations between RFCs in the
      series are explicitly noted in the RFC header.  For example, a new
      RFC may update one or more earlier RFCs.  Currently two
      relationships are defined: "Updates" and "Obsoletes" [RFC7322].
      Variants like "Obsoleted by" are also used (e.g, in [RFC5143]).
      Other types of relationships may be defined by the RFC Editor and
      may appear in future RFCs.
"""

import argparse
import urllib.request
import re


rfcIndexUrl =   "http://www.ietf.org/download/rfc-index.txt"
rfcIndexFile =  "rfc-index.txt"
myRfcListFile = "my-rfc-list.txt"


def parseArguments():
    # Enter arguments
    # create argument parser
    parser = argparse.ArgumentParser()
    # print version
    parser.add_argument("-v", "--version", action="version", version="%(prog)s - Version 1.0")
    # optional arguments
    parser.add_argument("-di", "--downloadIndex", action="store_true", help="download current official RFC Index from IETF online repository")
    # parse arguments
    argms = parser.parse_args()
    return argms

def downloadOnlineRfcIndex():
    # Run only if argument "-di", "-- downloadIndex" is used
    # Download current official RFC Index from the IETF online repository
    # "http://www.ietf.org/download/rfc-index.txt"
    with urllib.request.urlopen(rfcIndexUrl) as f0:
        RfcIndexContent = f0.read().decode("utf-8")
        allLines = RfcIndexContent.split("\n\n")
        for line in allLines:
            if "CREATED" in line:
                print("GOT RFC INDEX " + line + "\n")
                break
        fRfcIndex = open(rfcIndexFile, "w")
        fRfcIndex.write(RfcIndexContent)
        f0.close()
        fRfcIndex.close()

def processRfcInformation():
    with open(myRfcListFile) as f1:
        myRfcListContent = f1.read()
        allMyRfcListRFC = re.split(r"[,\s]\s*", myRfcListContent)
        allMyRfcList = [sub.replace("RFC", "") for sub in allMyRfcListRFC]
        allMyRfcList = list(filter(None, allMyRfcList))
        fAnalysis = open("rfc-analysis.txt", "w")
        print("My RFC list include : " + str(allMyRfcList) + "\nMy RFC list total count : " + str(len(allMyRfcList)))
        fAnalysis.write("My RFC list include : " + str(allMyRfcList) + "\nMy RFC list total count : " + str(len(allMyRfcList)) + "\n")
        with open(rfcIndexFile) as f2:
            rfcIndexContent = f2.read()
            allLines = rfcIndexContent.split("\n\n")
            fObsoleted = open("rfc-obsoleted.txt", "w")
            fUpdated = open("rfc-updated.txt", "w")
            for rfc in allMyRfcList:
                for rfcLine in allLines:
                    rfcLine = " ".join(rfcLine.split())
                    rfcData = rfcLine.split(" ", 1) # rfcData[0] = RFC Number, rfcData[1] = RFC Details
                    if (rfcData[0].isdigit()) and (rfcData[0] == rfc):
                        print("\n-- Analysis for RFC" + rfc + " :\n  " + str(rfcData))
                        fAnalysis.write("\n-- Analysis for RFC" + rfc + " :\n  " + str(rfcData) + "\n")
                        contentInParentheses = re.findall("\((.*?)\)",rfcData[1])
                        for content in contentInParentheses:
                            if "Obsoleted" in content:
                                print("      - Found new relationship : " + content)
                                fAnalysis.write("      - Found new relationship : " + content + "\n")
                                fObsoleted.write("RFC" + rfc + " " + content + "\n")
                            if "Updated" in content:
                                print("      - Found new relationship : " + content)
                                fAnalysis.write("      - Found new relationship : " + content + "\n")
                                fUpdated.write("RFC" + rfc + " " + content + "\n")
                            else: continue
                        break
                    else: continue
    f1.close()
    f2.close()
    fAnalysis.close()
    fObsoleted.close()
    fUpdated.close()


if __name__ == "__main__":

    # Parse arguments
    args = parseArguments()
    downloadIndex = args.downloadIndex

    # If argument "-di, --downloadIndex" is used
    if  downloadIndex:
        print("Downloading current official RFC Index from IETF online repository...")
        downloadOnlineRfcIndex()

    # Main script
    processRfcInformation()
