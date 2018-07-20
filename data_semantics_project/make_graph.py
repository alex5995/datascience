import pandas as pd
import rdflib
from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import RDF, FOAF, RDFS, XSD
import ast
import re
import json
import random
def isNotNan(x):
    return x==x
def makeIndex(x):
    if len(x)==1: return "00"+x
    if len(x)==2: return "0"+x
    if len(x)==3: return x

poke = pd.read_csv("pokemon.csv")
evoluzioni = pd.read_csv("ev_pul.csv", sep=";", encoding='latin1')
egg_groups = pd.read_csv("egg_groups.csv")
poke=pd.merge(left=poke,right=egg_groups,left_on="name",right_on="Pokémon")

pok = Namespace("https://bulbapedia.bulbagarden.net/wiki/")
typ = Namespace("https://bulbapedia.bulbagarden.net/wiki/") #capitalize della prima lettera + _(type)
gen = Namespace("https://bulbapedia.bulbagarden.net/wiki/Generation_") #va inserita la generazione dopo il trattino
abi = Namespace("https://bulbapedia.bulbagarden.net/wiki/") #+ _(Abilitity)
prop = Namespace("http://pokeprop/")
egg = Namespace("https://bulbapedia.bulbagarden.net/wiki/")

rdf_pok = URIRef("https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_(species)")
rdf_typ = URIRef("https://bulbapedia.bulbagarden.net/wiki/Type")
leg = URIRef("https://bulbapedia.bulbagarden.net/wiki/Legendary_Pok%C3%A9mon")
rdf_gen = URIRef("https://bulbapedia.bulbagarden.net/wiki/Generation")
rdf_abi = URIRef("https://bulbapedia.bulbagarden.net/wiki/Ability")
rdf_res = URIRef("https://bulbapedia.bulbagarden.net/wiki/Type#Type_chart")
rdf_cat = URIRef("https://bulbapedia.bulbagarden.net/wiki/Pok%C3%A9mon_category")
rdf_enemy = URIRef("https://bulbapedia.bulbagarden.net/wiki/Blue_(game)")
rdf_egg = URIRef("https://bulbapedia.bulbagarden.net/wiki/Egg_Group")

generations = ("I","II","III","IV","V","VI","VII")
against = ['against_bug', 'against_dark', 'against_dragon',
       'against_electric', 'against_fairy', 'against_fight', 'against_fire',
       'against_flying', 'against_ghost', 'against_grass', 'against_ground',
       'against_ice', 'against_normal', 'against_poison', 'against_psychic',
       'against_rock', 'against_steel', 'against_water']
stats = ['attack', 'base_egg_steps', 'base_happiness', 'base_total', 'capture_rate',
         'defense', 'experience_growth', 'height_m', 'hp', 'percentage_male', 'pokedex_number', 
         'sp_attack', 'sp_defense', 'speed', 'weight_kg']

g = Graph()

g.add( (rdf_pok, RDF.type, RDFS.Class) )
g.add( (rdf_typ, RDF.type, RDFS.Class) )
g.add( (leg, RDFS.subClassOf, rdf_pok) )
g.add( (rdf_gen, RDF.type, RDFS.Class) )
g.add( (rdf_abi, RDF.type, RDFS.Class) )
g.add( (rdf_res, RDF.type, RDFS.Class) )
g.add( (rdf_cat, RDF.type, RDFS.Class) )
g.add( (rdf_enemy, RDF.type, RDFS.Class))
g.add( (rdf_egg,RDF.type, RDFS.Class) )

g.add( (prop["has_egg_group.html"], RDF.type, RDF.Property) )
g.add( (prop["has_egg_group.html"], RDFS.domain, rdf_pok) )
g.add( (prop["has_egg_group.html"], RDFS.range, rdf_egg) )

g.add( (prop["has_type.html"], RDF.type, RDF.Property) )
g.add( (prop["has_type.html"], RDFS.domain, rdf_pok) )
g.add( (prop["has_type.html"], RDFS.range, rdf_typ) )

g.add( (prop["is_from_generation.html"], RDF.type, RDF.Property) )
g.add( (prop["is_from_generation.html"], RDFS.domain, rdf_pok) )
g.add( (prop["is_from_generation.html"], RDFS.range, rdf_gen) )

g.add( (prop["has_ability.html"], RDF.type, RDF.Property) )
g.add( (prop["has_ability.html"], RDFS.domain, rdf_pok) )
g.add( (prop["has_ability.html"], RDFS.range, rdf_abi) )

g.add( (prop["has_resistance.html"], RDF.type, RDF.Property) )
g.add( (prop["has_resistance.html"], RDFS.domain, rdf_pok) )
g.add( (prop["has_resistance.html"], RDFS.range, rdf_res) )

g.add( (prop["res_type.html"], RDF.type, RDF.Property) )
g.add( (prop["res_type.html"], RDFS.domain, rdf_res) )
g.add( (prop["res_type.html"], RDFS.range, rdf_typ) )

g.add( (prop["res_value.html"], RDF.type, RDF.Property) )
g.add( (prop["res_value.html"], RDFS.domain, rdf_res) )

g.add( (URIRef("http://pokeprop/category"), RDF.type, RDF.Property) )
g.add( (URIRef("http://pokeprop/category"), RDFS.domain, rdf_pok) )
g.add( (URIRef("http://pokeprop/category"), RDFS.range, rdf_cat) )

for el in stats:
    el = URIRef("http://pokeprop/" + el)
    g.add( (el, RDF.type, RDF.Property) )
    g.add( (el, RDFS.domain, rdf_pok) )
    
g.add( (URIRef("http://pokeprop/evolves_to"), RDF.type, RDF.Property) )
g.add( (URIRef("http://pokeprop/evolves_to"), RDFS.domain, rdf_pok) )
g.add( (URIRef("http://pokeprop/evolves_to"), RDFS.range, rdf_pok) )

g.add( (URIRef("http://pokeprop/possible_selection_against"), RDF.type, RDF.Property) )
g.add( (URIRef("http://pokeprop/possible_selection_against"), RDFS.domain, rdf_pok) )
g.add( (URIRef("http://pokeprop/possible_selection_against"), RDFS.range, rdf_enemy) )

g.add( (URIRef("http://pokeprop/enemy"), RDF.type, RDF.Property) )
g.add( (URIRef("http://pokeprop/enemy"), RDFS.domain, rdf_enemy) )
g.add( (URIRef("http://pokeprop/enemy"), RDFS.range, rdf_pok) )

g.add( (URIRef("http://pokeprop/number_of_possible_selections"), RDF.type, RDF.Property) )
g.add( (URIRef("http://pokeprop/number_of_possible_selections"), RDFS.domain, rdf_enemy) )

g.add( (URIRef("http://pokeprop/number_of_selections"), RDF.type, RDF.Property) )
g.add( (URIRef("http://pokeprop/number_of_selections"), RDFS.domain, rdf_enemy) )

for row in poke.itertuples():
    nome = URIRef(row.name.replace(" ","_") + "_(Pokémon)")
    g.add( (pok[nome], RDFS.label, Literal(row.name)) )
    tipo1 = URIRef(row.type1.capitalize() + "_(type)")
    g.add( (pok[nome], prop["has_type.html"], typ[tipo1]) )
    g.add( (typ[tipo1], RDF.type, rdf_typ) )
    g.add( (typ[tipo1], RDFS.label, Literal(row.type1.capitalize())) )
    if isNotNan(row.type2):
        tipo2 = URIRef(row.type2.capitalize() + "_(type)")
        g.add( (pok[nome], prop["has_type.html"], typ[tipo2]) )
        g.add( (typ[tipo2], RDF.type, rdf_typ) )
        g.add( (typ[tipo2], RDFS.label, Literal(row.type2.capitalize())) )
    egg1=URIRef(row._43.replace(" ","_").capitalize()+"_(Egg_Group)")
    g.add((pok["nome"],prop["has_egg_group.html"],egg[egg1]))
    g.add((egg[egg1],RDF.type,rdf_egg))
    g.add((egg[egg1],RDFS.label,Literal(row._43.capitalize())))
    if isNotNan(row._44):
        egg2 = URIRef(row._44.replace(" ","_").capitalize() + "_(Egg_Group)")
        g.add( (pok[nome], prop["has_egg_group.html"], egg[egg2]) )
        g.add( (egg[egg2], RDF.type, rdf_egg) )
        g.add( (egg[egg2], RDFS.label, Literal(row._44.capitalize())) )
    if row.is_legendary == 1:
        g.add( (pok[nome], RDF.type, leg) )
    else:
        g.add( (pok[nome], RDF.type, rdf_pok) )
    gener = URIRef(generations[row.generation - 1])
    g.add( (pok[nome], prop["is_from_generation.html"], gen[gener]) )
    g.add( (gen[gener], RDF.type, rdf_gen) )
    g.add( (gen[gener], RDFS.label, Literal("Gen. "+generations[row.generation-1])) )
    abilit = ast.literal_eval(row.abilities)
    for elm in abilit:
        el = URIRef(elm.replace(" ","_") + "_(Ability)")
        g.add( (pok[nome], prop["has_ability.html"], abi[el]) )
        g.add( (abi[el], RDF.type, rdf_abi) )
        g.add( (abi[el], RDFS.label, Literal(elm)) )
    for i in range(2,20):
        resistance = URIRef("http://pokeres/"+against[i-2]+"/"+str(row[i]))
        g.add( (pok[nome], prop["has_resistance.html"], resistance) )
        g.add( (resistance, RDF.type, rdf_res) )
        g.add( (resistance, prop["res_value.html"], Literal(row[i], datatype=XSD.float)) )
        el = URIRef(re.split('\_',against[i-2])[1].capitalize() + "_(type)")
        g.add( (resistance, prop["res_type.html"], typ[el]) )
    mycat = URIRef("http://pokecat/" + row.classfication.replace(" ","_"))
    mypropcat = URIRef("http://pokeprop/category")
    g.add( (pok[nome], mypropcat, mycat) )
    g.add( (mycat, RDF.type, rdf_cat) )
    j=0
    for i in [20,21,22,23,24,26,27,28,29,32,33,34,35,36,39]:
        myprop = URIRef("http://pokeprop/" + stats[j])
        j+=1
        try:
            float(row[i])
            g.add( (pok[nome], myprop, Literal(row[i], datatype=XSD.float)) )
        except:
            g.add( (pok[nome], myprop, Literal(142.5, datatype=XSD.float)) )
            
evolv = URIRef("http://pokeprop/evolves_to")
for row in evoluzioni.itertuples():
    nome1=URIRef(row.pokemon.replace(" ","_") + "_(Pokémon)")
    nome2=URIRef(row.evoluzione.replace(" ","_") + "_(Pokémon)")
    if row.evoluzione=="Nidorino": nome1 = URIRef("Nidoran♂_(Pokémon)")
    if row.evoluzione=="Nidorina": nome1 = URIRef("Nidoran♀_(Pokémon)")
    g.add( (pok[nome1], evolv, pok[nome2]) )

g.serialize(destination='output.ttl', format='turtle')