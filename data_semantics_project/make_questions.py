import pandas as pd
from rdflib import Graph
from rdflib import Literal
from rdflib import Namespace, URIRef
import re
import json
import random
def isNotNan(x):
    return x==x
def makeIndex(x):
    x = x.split(".")[0]
    if len(x)==1: return "00"+x
    if len(x)==2: return "0"+x
    if len(x)==3: return x

poke = pd.read_csv("pokemon.csv")
    
g = Graph()
g.parse("output.ttl", format="turtle")

q1 = g.query(
    
    """SELECT DISTINCT ?pokemon ?id
       WHERE {
       ?s rdf:type ?b .
          ?s rdfs:label ?pokemon .
          ?s poke:has_type.html ?t .
          ?t rdfs:label ?lab .
          ?s poke:is_from_generation.html ?x .
          ?x rdfs:label ?y .
          ?s poke:pokedex_number ?id
        FILTER ( ?pokemon != ?eevee)
       }""",
    
    initNs=dict(
        poke=Namespace("http://pokeprop/")),
    initBindings={ 'y': Literal("Gen. I"), 'eevee' : Literal( "Eevee")}
)
    
random_list = random.sample(q1.result,1)
random_pok = str(random_list[0][0])
random_pok_id = makeIndex(str(random_list[0][1]))

domanda1= "A che tipo appartiene " + random_pok + "?"

q2 = g.query(
    
    """SELECT DISTINCT ?pokemon ?type
       WHERE {
       ?s rdf:type ?b .
          ?s rdfs:label ?pokemon .
          ?s prop:has_type.html ?t .
          ?t rdfs:label ?type .
       }""",
    
    initNs=dict(
        prop=Namespace("http://pokeprop/")),
    initBindings={ 'pokemon': Literal(random_pok)}
)

true_typ = []
for row in q2.result:
    true_typ.append(str(row[1]))
true_typ1 = true_typ
true_typ1.append( "None")

q3 = g.query(
    
    """SELECT DISTINCT ?typ
       WHERE {
       ?s rdf:type ?b .
          ?s rdfs:label ?pokemon .
          ?s prop:has_type.html ?t .
          ?t rdfs:label ?typ .
       FILTER (?typ != ?type1 && ?typ != ?type2)
       }""",
    
    initNs=dict(
        prop=Namespace("http://pokeprop/")),
    
    initBindings={ 'type1': Literal(true_typ[0]), 'type2': Literal(true_typ[1])}
)

list1 = random.sample(q3.result,3)
random_typ1 = str(list1[0][0])
random_typ2 = str(list1[1][0])
random_typ3 = str(list1[2][0])

list2 = random.sample(q1.result,4)
random_pok1 = str(list2[0][0])
random_pok1_id = makeIndex(str(list2[0][1]))
random_pok2 = str(list2[1][0])
random_pok2_id = makeIndex(str(list2[1][1]))
random_pok3 = str(list2[2][0])
random_pok3_id = makeIndex(str(list2[2][1]))
random_pok4 = str(list2[3][0])
random_pok4_id = makeIndex(str(list2[3][1]))

q4 = g.query(
    
    """SELECT ?speed ?pokemon ?x
       WHERE {
          ?s poke:pokedex_number ?x .
          ?s rdf:type ?b .
          ?s rdfs:label ?pokemon .
          ?s poke:speed ?speed
       FILTER (?pokemon = ?pok1 || ?pokemon = ?pok2 || ?pokemon = ?pok3 || ?pokemon = ?pok4)
       }""",
    
    initNs=dict(
        poke=Namespace("http://pokeprop/")),
    
    initBindings={ 'pok1': Literal(random_pok1), 'pok2': Literal(random_pok2), 'pok3': Literal(random_pok3),
                  'pok4': Literal(random_pok4)}
)

sp1 = int(q4.result[0][0].split(".")[0])
sp2 = int(q4.result[1][0].split(".")[0])
sp3 = int(q4.result[2][0].split(".")[0])
sp4 = int(q4.result[3][0].split(".")[0])

idsp1 = makeIndex(str((q4.result[0][2].split(".")[0])))
idsp2 = makeIndex(str((q4.result[1][2].split(".")[0])))
idsp3 = makeIndex(str((q4.result[2][2].split(".")[0])))
idsp4 = makeIndex(str((q4.result[3][2].split(".")[0])))

poksp1 = str(q4.result[0][1])
poksp2 = str(q4.result[1][1])
poksp3 = str(q4.result[2][1])
poksp4 = str(q4.result[3][1])

max_sp = max( [sp1, sp2, sp3, sp4])

score1=25
score2=25
score3=25
score4=25
if sp1 == max_sp: score1=100
if sp2 == max_sp: score2=100
if sp3 == max_sp: score3=100
if sp4 == max_sp: score4=100    
    
domanda2 = "Quale tra questi ha speed maggiore?"

random_list_ab = random.sample(q1.result,1)
random_pokab = str(random_list_ab[0][0])
random_pokab_id = makeIndex(str(random_list_ab[0][1]))

domanda3= "Quale di queste ability possiede " + random_pokab + "?"

q6 = g.query(
    
    """SELECT DISTINCT ?pokemon ?ab
       WHERE {
       ?s rdf:type ?b .
          ?s rdfs:label ?pokemon .
          ?s prop:has_ability.html ?t .
          ?t rdfs:label ?ab .
       }""",
    
    initNs=dict(
        prop=Namespace("http://pokeprop/")),
    initBindings={ 'pokemon': Literal(random_pokab)}
)

true_ab = []
for row in q6.result:
    true_ab.append(str(row[1]))
true_ab1= true_ab
true_ab1.append( "None1")
true_ab1.append( "None2")
true_ab1.append( "None3")
true_ab1.append( "None4")

q7 = g.query(
    
    """SELECT DISTINCT ?ab
       WHERE {
       ?s rdf:type ?b .
          ?s rdfs:label ?pokemon .
          ?s prop:has_ability.html ?t .
          ?t rdfs:label ?ab .
       FILTER (?ab != ?ab1 && ?ab != ?ab2 && ?ab != ?ab3 && ?ab != ?ab4 && ?ab != ?ab5)
       }""",
    
    initNs=dict(
        prop=Namespace("http://pokeprop/")),
    
    initBindings={ 'ab1': Literal(true_ab[0]), 'ab2': Literal(true_ab[1]), 
                  'ab3': Literal(true_ab[2]), 'ab4': Literal(true_ab[3]), 'ab5': Literal(true_ab[4])}
)
    
list3 = random.sample(q7.result,3)
random_ab1 = str(list3[0][0])
random_ab2 = str(list3[1][0])
random_ab3 = str(list3[2][0])

random_list_ev = random.sample(q1.result,1)
random_pokev = str(random_list_ev[0][0])
random_pokev_id = makeIndex(str(random_list_ev[0][1]))

domanda4 = "In cosa si evolve " + random_pokev + '?'

q8 = g.query(
    
    """SELECT DISTINCT ?pokev ?id
       WHERE {
       ?s rdf:type ?b .
          ?s rdfs:label ?pokemon .
          ?s poke:evolves_to ?ev .
          ?ev rdfs:label ?pokev .
          ?ev poke:pokedex_number ?id.
       }""",
    
    initNs=dict(
        poke=Namespace('http://pokeprop/')),
    initBindings ={ 'pokemon': Literal(random_pokev)}
)

true_ev = []
true_ev_id=[]
for row in q8.result:
    true_ev.append(str(row[0]))
    true_ev_id.append(makeIndex(str(row[1])))
if true_ev == [] : 
    true_ev.append ( "Non ha evoluzioni")
    true_ev_id.append("")
true_ev.append( "None")

q9 = g.query(
    
    """SELECT DISTINCT ?pokemon ?id
       WHERE {
        ?s rdf:type ?b .
        ?s rdfs:label ?pokemon .
        ?s poke:is_from_generation.html ?x .
        ?x rdfs:label ?y .
        ?s poke:pokedex_number ?id.
    FILTER ( ?pokemon != ?pok1 && ?pokemon != ?pok2  && ?pokemon != ?pok3)
       }""",
    
    initNs=dict(
        poke=Namespace('http://pokeprop/')),
    initBindings ={ 'pok1': Literal(random_pokev), 'pok2': Literal(true_ev[0]), 'pok3': Literal(true_ev[1]) ,
                   "y" : Literal("Gen. I") }
)

list4 = random.sample(q9.result,3)
random_ev1 = str(list4[0][0])
random_ev1_id = makeIndex(str(list4[0][1]))
random_ev2 = str(list4[1][0])
random_ev2_id = makeIndex(str(list4[1][1]))
if true_ev[0] == "Non ha evoluzioni": 
    random_ev3 = str(list4[2][0])
    random_ev3_id = makeIndex(str(list4[2][1]))
else: 
    random_ev3 = "Non ha evoluzioni"
    random_ev3_id = ""
    
img = "https://bulbapedia.bulbagarden.net/wiki/File:"

response={"domanda1":{"statement": domanda1,
                      "pokemon":[random_pok, random_pok_id, img+random_pok_id+random_pok+".png"],
                      'r1' : [random_typ1, 25], 
                      'r2' : [random_typ2, 25], 
                      'r3' : [random_typ3, 25], 
                      'r4' : [true_typ1[0], 100]},
          "domanda2":{"statement": domanda2,
                     'r1' : [poksp1, idsp1, img+idsp1+poksp1+".png", score1],
                     'r2' : [poksp2, idsp2, img+idsp2+poksp2+".png", score2], 
                     'r3' : [poksp3, idsp3, img+idsp3+poksp3+".png", score3], 
                     'r4' : [poksp4, idsp4, img+idsp4+poksp4+".png", score4]},
          "domanda3":{"statement": domanda3,
                      "pokemon":[random_pokab, random_pokab_id, img+random_pokab_id+random_pokab+".png"],
                     'r1' : [random_ab1, 25], 
                     'r2' : [random_ab2, 25],
                     'r3' : [random_ab3, 25],
                     'r4' : [true_ab1[0], 100]},
          "domanda4":{"statement": domanda4,
                      "pokemon":[random_pokev, random_pokev_id, img+random_pokev_id+random_pokev+".png"],
                     'r1' : [random_ev1, random_ev1_id, img+random_ev1_id+random_ev1+".png", 25], 
                     'r2' : [random_ev2, random_ev2_id, img+random_ev2_id+random_ev2+".png", 25],
                     'r3' : [random_ev3, random_ev3_id, img+random_ev3_id+random_ev3+".png", 25], 
                     'r4' : [true_ev[0], true_ev_id[0], img+true_ev_id[0]+true_ev[0]+".png", 100]}
         }

if random_ev3_id == "": response["domanda4"]["r3"][2]=""
else: response["domanda4"]["r4"][2]=""

with open ("domande.json", 'w') as outfile:
    json.dump(response, outfile)
    
import math
def get_type_coeff(x):
    if x["resistance_Total"]==0: return 5
    return 1 - math.log(float(x["resistance_Total"]))/math.log(2)/5

def nidoran(x):
    if x == "Nidoran♀" or x =="Nidoran♂": return "Nidoran"
    else: return x
def get_pokemon_list(pokemon_to_fight, tipo1, tipo2):
    q_supereff = g.query(
        """SELECT DISTINCT ?pokemon ?res_val
           WHERE {
              ?s rdf:type ?b .
              ?s rdfs:label ?pokemon .
              ?s prop:has_resistance.html ?r .
              ?r prop:res_type.html ?type .
              ?r prop:res_value.html ?res_val.
              ?type rdfs:label ?tipo.
            ?s prop:is_from_generation.html ?x .
              ?x rdfs:label ?y.
           }""",
        
        initNs=dict(
            prop=Namespace("http://pokeprop/")),
        initBindings={ 'tipo': Literal(tipo1), 'y': Literal('Gen. I')}
    )
    pokemon = []
    for row in q_supereff.result:
        row= str(row)
        pokemon.append( re.split('\(\'|\'\)|\',|\(\"|\"\)', row)[1:4:2])
    tabella = pd.DataFrame.from_records(pokemon, columns=["Pokemon","resistance_Total"])
    if tipo2 != "Nessuno":
        q_supereff = g.query(
            """SELECT DISTINCT ?pokemon ?res_val
               WHERE {
                  ?s rdf:type ?b .
                  ?s rdfs:label ?pokemon .
                  ?s prop:has_resistance.html ?r .
                  ?r prop:res_type.html ?type .
                  ?r prop:res_value.html ?res_val.
                  ?type rdfs:label ?tipo.
                  ?s prop:is_from_generation.html ?x .
                  ?x rdfs:label ?y.
               }""",
        
            initNs=dict(
                prop=Namespace("http://pokeprop/")),
                initBindings={ 'tipo': Literal(tipo2), 'y': Literal('Gen. I')}
        )
        pokemon = []
        for row in q_supereff.result:
            row= str(row)
            pokemon.append( re.split('\(\'|\'\)|\',|\(\"|\"\)', row)[1:4:2])
        tipo_2 = pd.DataFrame.from_records(pokemon, columns=["Pokemon","resistance_2"])
        tabella = pd.merge(left= tabella, right = tipo_2, on="Pokemon")
        tabella["resistance_Total"] = tabella.apply(lambda x:float(x["resistance_Total"]) * float(x["resistance_2"]), axis=1)
    tabella["type_coeff"] = tabella.apply(lambda x: get_type_coeff(x), axis=1)
    stats_query = g.query( 
        """SELECT ?pokemon ?base_total 
           WHERE {
              ?s rdf:type ?b .
              ?s rdfs:label ?pokemon .
              ?s poke:base_total ?base_total.
              ?s prop:is_from_generation.html ?x .
              ?x rdfs:label ?y.
           }""",
        initNs=dict(
            prop=Namespace("http://pokeprop/"),
            poke=Namespace("http://pokeprop/")),
            initBindings={ 'y': Literal('Gen. I')}   
    )
    pokemon = []
    for row in stats_query.result:
        row= str(row)
        pokemon.append( re.split('\(\'|\'\)|\',|\(\"|\"\)', row)[1:4:2])
    stats = pd.DataFrame.from_records(pokemon, columns=["Pokemon","stats_total"])
    tabella = pd.merge(left = tabella, right = stats, on = "Pokemon")
    stats_base = tabella[tabella["Pokemon"]==pokemon_to_fight]["stats_total"]
    tabella["stats_coeff"] = tabella.apply(lambda x: float(x["stats_total"]) / float(stats_base), axis=1) 
    speed_query = g.query( 
        """SELECT ?pokemon ?speed 
           WHERE {
              ?s rdf:type ?b .
              ?s rdfs:label ?pokemon .
              ?s poke:speed ?speed.
              ?s prop:is_from_generation.html ?x .
              ?x rdfs:label ?y.
           }""",
        initNs=dict(
            prop=Namespace("http://pokeprop/"),
            poke=Namespace("http://pokeprop/")),
            initBindings={ 'y': Literal('Gen. I')}   
    )
    pokemon = []
    for row in speed_query.result:
        row= str(row)
        #lst = [1,3]
        pokemon.append( re.split('\(\'|\'\)|\',|\(\"|\"\)', row)[1:4:2])
    speed = pd.DataFrame.from_records(pokemon, columns=["Pokemon","speed"])
    tabella = pd.merge(left = tabella, right = speed, on = "Pokemon")
    speed_base = tabella[tabella["Pokemon"]==pokemon_to_fight]["speed"]
    tabella["speed_coeff"] = tabella.apply(lambda x: float(x["speed"]) / float(speed_base), axis=1)
    tabella["coeff"] = tabella["stats_coeff"] * tabella["type_coeff"] ** 2 * tabella["speed_coeff"] ** 2 
    tabella["coeff"] = tabella["coeff"] / tabella["coeff"].sum()
    ev_query = g.query( 
        """SELECT ?pokemon
           WHERE {
              ?s rdf:type ?b .
              ?s rdfs:label ?pokemon .
              ?s prop:is_from_generation.html ?x .
              ?x rdfs:label ?y.
              MINUS{
                ?s prop:evolves_to ?ev 
              }
           }""",
        initNs=dict(
            prop=Namespace("http://pokeprop/"),
            poke=Namespace("http://pokeprop/")),
            initBindings={ 'y': Literal('Gen. I')}
    )
    pokemon_ev = []
    for row in ev_query.result:
        pokemon_ev.append(str(row[0]))
    evo = pd.DataFrame(pokemon_ev, columns=["Pokemon"])
    tabella = pd.merge(left = tabella, right = evo, on = "Pokemon")
    import random
    pokemon_lista = []
    while (pokemon_lista == None or len(pokemon_lista) < 10):
        seed = random.random()
        cum = 0 
        for row in tabella.iterrows():
            pokemon_to_add=row[1]["Pokemon"]
            if seed < (cum + row[1]["coeff"]): 
                pokemon_to_add = row[1]["Pokemon"]
                break
            else: 
                cum = cum + row[1]["coeff"]
        if (pokemon_lista != None and pokemon_to_add in pokemon_lista):
            continue
            print("Pokemon già presente")
        else: 
            pokemon_lista.append(pokemon_to_add)
    pokedex_list = [0,0,0,0,0,0,0,0,0,0]
    i = 0
    pokemon_lista2 = list(map(nidoran, pokemon_lista))
    for po in pokemon_lista:
        a = str(poke[poke["name"]==po]["pokedex_number"].item())
        while (len(a) < 3):
            a = "0" + str(a)
        pokedex_list[i] = a
        i = i+1
    response={pokemon_lista[0]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[0]+pokemon_lista[0]+".png",
                          pokemon_lista[1]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[1]+pokemon_lista2[1]+".png",
                          pokemon_lista[2]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[2]+pokemon_lista2[2]+".png",
                          pokemon_lista[3]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[3]+pokemon_lista2[3]+".png",
                          pokemon_lista[4]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[4]+pokemon_lista2[4]+".png",
                          pokemon_lista[5]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[5]+pokemon_lista2[5]+".png",
                          pokemon_lista[6]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[6]+pokemon_lista2[6]+".png",
                          pokemon_lista[7]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[7]+pokemon_lista2[7]+".png",
                          pokemon_lista[8]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[8]+pokemon_lista2[8]+".png",
                          pokemon_lista[9]: "https://bulbapedia.bulbagarden.net/wiki/File:"+pokedex_list[9]+pokemon_lista2[9]+".png"}
    with open (pokemon_to_fight+".json", 'w') as outfile:
        json.dump(response, outfile)
    return pokemon_lista                        

get_pokemon_list("Gyarados","Water","Flying");
get_pokemon_list("Arcanine","Fire","Nessuno");
get_pokemon_list("Alakazam","Psychic","Nessuno");
get_pokemon_list("Rhydon","Ground","Rock");
get_pokemon_list("Exeggutor","Grass","Psychic");
get_pokemon_list("Pidgeot","Normal","Flying");
with open('Gyarados.json') as f:
    gyarados = json.load(f)
with open('Arcanine.json') as f:
    arcanine = json.load(f)
with open('Alakazam.json') as f:
    alakazam = json.load(f)
with open('Rhydon.json') as f:
    rhydon = json.load(f)
with open('Exeggutor.json') as f:
    exeggutor = json.load(f)
with open('Pidgeot.json') as f:
    pidgeot = json.load(f)
response = {
    "Blue": {
        "Gyarados": "https://bulbapedia.bulbagarden.net/wiki/File:130Gyarados.png",
        "Arcanine": "https://bulbapedia.bulbagarden.net/wiki/File:059Arcanine.png",
        "Alakazam": "https://bulbapedia.bulbagarden.net/wiki/File:065Alakazam.png",
        "Rhydon": "https://bulbapedia.bulbagarden.net/wiki/File:112Rhydon.png",
        "Exeggutor": "https://bulbapedia.bulbagarden.net/wiki/File:103Exeggutor.png",
        "Pidgeot": "https://bulbapedia.bulbagarden.net/wiki/File:018Pidgeot.png"
    },
    "Gyarados": gyarados,
    "Arcanine": arcanine,
    "Alakazam": alakazam,
    "Rhydon": rhydon,
    "Exeggutor":exeggutor,
    "Pidgeot": pidgeot
}
with open ("list_pokemon.json", 'w') as outfile:
    json.dump(response, outfile)