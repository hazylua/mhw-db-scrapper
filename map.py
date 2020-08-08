import requests
import json

skillmap = {
    'high': {},
    'low': {},
    'master': {},
    'decorations':{}
}

# KEYS
# id, rarity ( INT )
# name, type, rank ( STRING )
# defense, resistances, attributes, assets ( DICTIONARY/OBJECT )
# slots, skills ( ARRAY )

response = requests.get("https://mhw-db.com/armor").json()
for gear in response:
    rank = gear['rank']
    rarity = gear['rarity']

    for skill in gear['skills']:
        n = skill['skillName'].lower().replace(" ", "-")
        
        slots = []
        for slot in gear['slots']:
            slots.append(slot['rank'])

        t = (gear['id'], gear['type'], skill['level'], slots, n, rarity) 

        if n in skillmap[rank]:
            skillmap[rank][n].append(t)
        else:
            skillmap[rank][n] = []
            skillmap[rank][n] = []
            skillmap[rank][n].append(t)

response = requests.get("https://mhw-db.com/charms").json()

for charm in response:
    
    c = charm['ranks'][len(charm['ranks'])-1]
    rarity = c['rarity']

    for skills in c['skills']:
        lvl = skills['level']
        sklnm = skills['skillName'].lower().replace(' ', '-')
        
        tp = (charm['id'], 'charm', lvl, [], sklnm, rarity)

        for rank in skillmap:
            if rank != 'decorations':
                if sklnm in skillmap[rank]:
                    skillmap[rank][sklnm].append(tp)
                else:
                    skillmap[rank][sklnm] = []
                    skillmap[rank][sklnm].append(tp)     

with open('skillmap.json', 'w') as f:
    json.dump(skillmap, f)

response = requests.get("https://mhw-db.com/decorations").json()
mapped = [{}, {}, {}, {}]
for deco in response:
    jewel = []
    id_ = deco['id']
    slot = deco['slot']
    for skill in deco['skills']:
        level = skill['level']
        skillName = skill['skillName'].replace(' ', '-').lower()
        jewel.append((level, skillName)) 
    
    if skillName in mapped[slot-1]:
        mapped[slot-1][skillName].append((id_, jewel))
    else:
        mapped[slot-1][skillName] = []
        mapped[slot-1][skillName].append((id_, jewel))      

with open('decomap.json', 'w') as f:
    json.dump(mapped, f)




response = requests.get("https://mhw-db.com/armor").json()

armormap = [None] * 1800
print(len(armormap))
for gear in response:
    s = []
    for skill in gear['skills']:
        st = (skill['id'], skill['level'], skill['skillName'].lower().replace(' ', '-'))
        s.append(st)
    armormap[gear['id']] = s
        
with open('armormap.json', 'w') as f:
    json.dump(armormap, f)


charmmap = [None]*400
response = requests.get("https://mhw-db.com/charms").json()
for charm in response:
    _id = charm['id']
    max_level = len(charm['ranks'])-1
    effects = []
    for skill in charm['ranks'][max_level]['skills']:
        id_ = skill['id']
        level = skill['level']
        name = skill['skillName'].lower().replace(' ', '-')
        tp = (id_, level, name)
        effects.append(tp)

    charmmap[_id] = effects

with open('charmmap.json', 'w') as f:
    json.dump(charmmap, f)