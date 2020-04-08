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

def extractAddressSetFromAddressSet(fwConfig):
    addressSplit = []
    addressSetFromAddressSet = {}

    for line in fwConfig:
        if re.match(r'set security address-book global address-set .* address-set', line):
            addressSplit = line.split()

            keyValue = addressSplit[5]
            addressValue = addressSplit[7]

            if keyValue in addressSetFromAddressSet:
                addressSetFromAddressSet[keyValue].append(addressValue)

            else:
                addressSetFromAddressSet[keyValue] = []
                addressSetFromAddressSet[keyValue].append(addressValue)

    return(addressSetFromAddressSet)

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

def compareEntries(uniqueAddress, uniqueAddressSet, addressSetFromAddressSet):

    for key, value in addressSetFromAddressSet.items():
        for item in range(len(value)):
            addressSetCompare = value[item]
            if addressSetCompare in uniqueAddressSet:
                for addressEntry in uniqueAddressSet[addressSetCompare]:
                    uniqueAddressSet[key].append(addressEntry)

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
        addressSetFromAddressSet = extractAddressSetFromAddressSet(compare)
        uniqueAddressSet = extractAddressSet(compare)
        compareEntries(uniqueAddress, uniqueAddressSet, addressSetFromAddressSet)

if __name__ == "__main__":
    main()
