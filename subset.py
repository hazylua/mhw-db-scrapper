import json
import copy

data = None
armor = None
charms = None
deco = None
with open('skillmap.json', 'r') as f:
    data = json.load(f)
with open('armormap.json', 'r') as f:
    armor = json.load(f)
with open('charmmap.json', 'r') as f:
    charms = json.load(f)
with open('decomap.json', 'r') as f:
    deco = json.load(f)
search = {
    'critical-eye':7,
    'attack-boost':7,
    'peak-performance':3,
}   

limit = 200
inventory = {
    'head':[],
    'chest':[],
    'gloves':[],
    'waist':[],
    'legs':[],
    'charm': []
}

for s in search:
    for a in data['master'][s]:
        inventory[a[1]].append(a)
        inventory[a[1]].append

inventory['head'].append([0,0,0])
inventory['chest'].append([0,0,0])
inventory['gloves'].append([0,0,0])
inventory['waist'].append([0,0,0])
inventory['legs'].append([0,0,0])
inventory['charm'].append([0,0,0])


for i in inventory:
    inventory[i] = sorted(inventory[i], key=lambda x: x[2], reverse=True)    

def check_levels(total):
    for skill in search:
        if skill in total['skills'] and total['skills'][skill] == search[skill]:
            pass
        else:            
            return False
      
    return True        

def equip_deco(armor, level, skill, total):

    if skill in deco[level]:
        for effects in deco[level][skill]:
            if total['slots'][level] <= 0:
                return

            temporary = {}

            for s in effects[1]:
                temporary[s[1]] = s[0]
                if s[1] in total['skills']:
                    temporary[s[1]] += total['skills'][s[1]]

            if temporary[skill] <= search[skill]:
                for key in temporary:
                    total['skills'][key] = temporary[key]
                total['slots'][level] -= 1
                armor['decos'].append(effects[0])     

    else:
        return    
    pass

def fill_decoration(armorset, total):
    #print(total)

    for skill in copy.deepcopy(total['skills']):
        if skill in search and total['skills'][skill] < search[skill]:
            for slot_level, _ in enumerate(total['slots']):
                equip_deco(armorset, slot_level, skill, total)
                if total['skills'][skill] == search[skill]:
                    break

    #for slot_level, qtd in enumerate(total['slots']):
    #    print(deco[slot_level])
    #print(armorset)

def fits(armorset, piece, piece_type, total):
    if piece[0] == 0:
        return (total, True, armorset)
    
    d = None
    if piece_type == 'charm':
        d = charms[piece[0]] 
    else:
        d = armor[piece[0]] 

    armor_copy = copy.deepcopy(armorset)
    armor_copy[piece_type] = piece[0]
    
    tcopy = copy.deepcopy(total)
    
    for slot in piece[3]:
        tcopy['slots'][slot-1] += 1
    for i in d:
        if i[2] in tcopy['skills']:
            tcopy['skills'][i[2]] += i[1]
        else:
            tcopy['skills'][i[2]] = i[1]

    if tcopy['skills'][piece[4]] > search[piece[4]]:
        return (total, False, armorset)
    return (tcopy, True, armor_copy)    

def chest(armory, armor, total, check, sets):
    if not check:
        return

    for g in armory:
        t,c,a = fits(armor, g, 'chest', total)
        gloves(inventory['gloves'], a, t, c, sets)  
        if len(sets) > limit:
            return  

def gloves(armory, armor, total, check, sets):
    if not check:
        return
    
    for g in armory:
        t, c, a = fits(armor, g, 'gloves', total)
        waist(inventory['waist'], a, t, c, sets)    
        if len(sets) > limit:
            return  

def waist(armory, armor, total, check, sets):
    if not check:
        return
    
    for g in armory:
        t,c,a = fits(armor, g, 'waist', total)
        legs(inventory['legs'], a, t, c, sets)  
        if len(sets) > limit:
            return  

def legs(armory, armor, total, check, sets):
    if not check:
        return
    
    for g in armory:
        t,c,a = fits(armor, g, 'legs', total)
        charm(inventory['charm'], a, t, c, sets)  
        if len(sets) > limit:
            return  

def charm(armory, armor, total, check, sets):
    if not check:
        return
    if len(sets) > limit:
        return

    for g in armory:
        t,c,a = fits(armor, g, 'charm', total)

        #fill_decoration(a, t)
        if check_levels(t):
            sets.append((t, a)) 
        
        if len(sets)>limit:
            return   
        
def subset():

    sets = []
    
    for g1 in inventory['head']:
        armor = {'decos':[]}
        s = {'slots':[0,0,0,0], 'skills':{}}
        t,c,a  = fits(armor, g1, 'head', s) 
        chest(inventory['chest'], a, t, c, sets)

    return sets

for s in subset():      
    print(s)
    print()