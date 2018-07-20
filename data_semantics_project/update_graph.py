import os
import pandas as pd
from rdflib import Graph
from rdflib import URIRef, Literal
from rdflib import Namespace
from rdflib.namespace import XSD
import warnings
import time
warnings.filterwarnings("ignore")
test = pd.read_csv("export.csv")
pok = Namespace("https://bulbapedia.bulbagarden.net/wiki/")
prop = Namespace("http://pokeprop/")
g = Graph()
g.parse("output.ttl", format="turtle")
for row in test.itertuples(): 
    a = g.query( 
        """SELECT ?s ?e ?t ?z
           WHERE {
              ?s rdf:type ?b .
              ?s rdfs:label ?pokemon .
              ?s prop:possible_selections_against ?r.
              ?r prop:enemy ?e.
              ?e rdfs:label ?pokemon2.
              ?r prop:number_of_possible_selections ?t.
              ?r prop:number_of_selections ?z
           }""",
        initNs=dict(
            prop=Namespace("http://pokeprop/"),
            poke=Namespace("http://pokeprop/"))
        ,
    initBindings={ 'pokemon': Literal(row.pokemon), 'pokemon2': Literal(row.against)}
    ).result
    nome = URIRef(row.pokemon.replace(" ","_")+"_(Pokémon)")    
    nome2 = URIRef(row.against.replace(" ","_")+"_(Pokémon)")
    enemy = URIRef("http://pokenemy/"+(row.pokemon.replace(" ","_")+"/"+(row.against.replace(" ","_"))))
    if len(a) == 0:
        g.add( (pok[nome], prop["possible_selections_against"], enemy) )
        g.add((enemy, prop["enemy"], pok[nome2]))                                   
        g.add((enemy, prop["number_of_possible_selections"], Literal(1,datatype=XSD.float)))
        g.add((enemy, prop["number_of_selections"], Literal(row.points,datatype=XSD.float)))
    else: 
        g.set((enemy, prop["number_of_possible_selections"],Literal(g.value( enemy, prop["number_of_possible_selections"] )+1, datatype=XSD.float)))
        g.set((enemy, prop["number_of_selections"],Literal(g.value( enemy, prop["number_of_selections"] )+row.points, datatype=XSD.float)))
os.remove("export.csv")      

a = g.query( 
        """SELECT ?pokemon ?t ?z
           WHERE {
              ?s rdf:type ?b .
              ?s rdfs:label ?pokemon .
              ?s prop:possible_selections_against ?r.
              ?r prop:enemy ?e.
              ?e rdfs:label ?pokemon2.
              ?r prop:number_of_possible_selections ?t.
              ?r prop:number_of_selections ?z
           }""",
        initNs=dict(
            prop=Namespace("http://pokeprop/"),
            poke=Namespace("http://pokeprop/"))
        ,
    initBindings={ 'pokemon2': Literal("Alakazam")}
    ).result
user_pokemon_list = []
for row in a:
    user_pokemon_list.append([str(row[0]),float(row[2])/float(row[1])])
user_pokemon_list = pd.DataFrame.from_records(user_pokemon_list, columns=["Pokemon","Points"])
print(user_pokemon_list.sort_values("Points", ascending=False))
g.serialize(destination="output.ttl", format="turtle")
time.sleep(10)