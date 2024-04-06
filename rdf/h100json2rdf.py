#!/usr/bin/env python3

# Create Turtle RDF from the JSON Billboard Hot 100 JSON data at
# https://github.com/mhollingshead/billboard-hot-100. 

# run as
# ./h100json2rdf.py ../all.json

import json
import sys
import urllib.parse

if (len(sys.argv) < 2):
   print("Enter an input filename as an argument.")
   exit()
   
inputFile = sys.argv[1]


jsonBlock = ""

with open(inputFile) as fp:
    for line in fp:
        jsonBlock += line
       
    jsonData = json.loads(jsonBlock)

print('@prefix h1: <http://rdfdata.org/hot100#> .')
print('@prefix schema: <http://schema.org/> .')
print('@prefix dc: <http://purl.org/dc/elements/1.1/> .')
print('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .')
print('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .')

print()

for week in jsonData:
    
    chartDate = week["date"]

    for recording in week["data"]:
        artistName =recording["artist"]
        artistName = artistName.replace('"','\\"')
        songName = recording["song"]
        songName = songName.replace('"','\\"')
        # ID of song is artistURIStub + song because two different songs can
        # have the same title, e.g. Taylor Swift's and Banarama's "Cruel Summer"
        songURI = 'h1:' + urllib.parse.quote(artistName + songName).replace('%20','')
        artistURI = 'h1:' + urllib.parse.quote(artistName).replace('%20','')
        # Lose characters that screw up URI. 
        for c in ' &/.\"\'':
            songURI = songURI.replace(c,'')
            artistURI = artistURI.replace(c,'')

        print(artistURI + ' a h1:MusicalArtist ; ')
        print('   rdfs:label "' + artistName + '"@en .\n')
        print(songURI + ' a schema:Recording;')
        print('     schema:byArtist ' + artistURI + ';')
        print('     dc:title ' + '"' + songName + '";')
        print('     h1:charted ' + '"' + chartDate + '"^^xsd:date {| ')
        print('        h1:position ' + str(recording['this_week']))
        print('|}.\n')
