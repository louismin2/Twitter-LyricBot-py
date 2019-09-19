import json

with open('Keys.json') as json_file:
    keys = json.load(json_file)
    
#print(keys)

print(keys['Genius_Key'])
print(keys['Twitter_Consumer_Key'])
print(keys['Twitter_Consumer_Secret'])
print(keys['Twitter_Access_Token'])
print(keys['Twitter_Access_Secret'])