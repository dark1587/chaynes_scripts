#!/usr/bin/env python

import re

def extractAddress(fwConfig):
    addressSplit = []
    uniqueAddresses = []

    for line in fwConfig:
        if re.match(r'set security address-book global address ', line):

            addressSplit = line.split()
            uniqueAddresses.append(addressSplit[5])

    return(uniqueAddresses)

def extractAddressSet(fwConfig):
    addressSplit = []
    addressSetDictionary = {}

    for line in fwConfig:
        if re.match(r'set security address-book global address-set ', line):
            addressSplit = line.split()

            keyValue = addressSplit[5]
            addressValue = addressSplit[7]

            if keyValue in addressSetDictionary:
                addressSetDictionary[keyValue].append(addressValue)

            else:
                addressSetDictionary[keyValue] = []
                addressSetDictionary[keyValue].append(addressValue)

    return(addressSetDictionary)

def compareEntries(uniqueAddress, uniqueAddressSet):
    for address in uniqueAddress:
        tempAddressSet = []
        for key, value in uniqueAddressSet.iteritems():
            if address in value:
                tempAddressSet.append(key)
        if len(tempAddressSet) > 1:
            print "Address "+address+" is in the following groups:"
            print("\n".join(tempAddressSet))

def main():
    addresses = []
    duplicateAddresses = {}
    with open (raw_input("Enter Filename: "), 'r') as fwConfig:

        compare = fwConfig.readlines()
        uniqueAddress = extractAddress(compare)
        uniqueAddressSet = extractAddressSet(compare)
        compareEntries(uniqueAddress, uniqueAddressSet)

if __name__ == "__main__":
    main()
