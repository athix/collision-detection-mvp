import yaml

with open('head_on.yml', 'r') as stream:
    try:
        example_file = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print(e)

print(yaml.dump(example_file))

for player in example_file['battle']['players']:
    print(player['color'])

