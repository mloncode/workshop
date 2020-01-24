import yaml


with open("languages.yml") as f:
    n_langs = 0
    content = yaml.load(f.read())
    for k in content:
        if content[k]["type"] == "programming":
            n_langs += 1
            print(n_langs, k)
