import json

j = None
with open('skillmap.json') as f:
    j = json.load(f)

sn = input("what's the skill you're looking for? ")

for key in j['master'][sn]:
    print(key)

print(len(j['master'][sn]))