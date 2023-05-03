import sys
import yaml
import os


description = []


def any_constructor(loader, tag_suffix, node):
    if isinstance(node, yaml.MappingNode):
        return loader.construct_mapping(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_scalar(node)


yaml.add_multi_constructor('', any_constructor, Loader=yaml.SafeLoader)

variable_dict = dict()
with open("./template.yaml", "r") as file:
    try:
        yaml_dict = yaml.safe_load(file)
        for resource in yaml_dict["Resources"]:
            if yaml_dict["Resources"][resource]["Type"] == 'AWS::Serverless::Function':
                for variable in yaml_dict["Resources"][resource]["Properties"]["Environment"]["Variables"]:
                    variable_dict[variable] = {
                        "files": [],
                        "count": 0
                    }
                source = os.path.dirname(os.path.realpath(__file__)).replace("utility", yaml_dict["Resources"][resource][
                    "Properties"]["CodeUri"])
                sys.path.append(source)
    except yaml.YAMLError as error:
        print(error)
        exit(1)
file.close()
print(f'{"Variable":40s}{"Count":10s}{"Files"}')
for env_var in variable_dict:
    file_array = os.listdir(source)
    for file_name in file_array:
        if os.path.isfile(os.path.join(source, file_name)):
            with open(os.path.join(source, file_name), "r") as source_file:
                for line in source_file.readlines():
                    line.strip()
                    if line[0] == '#':
                        continue

                    # Wanted to just use the variable names for searching, but they are used as variable names.
                    # This made the count too high for some env variables

                    if f"os.environ.get('{env_var}')" in line or f'os.environ.get("{env_var}")' in line \
                        or f'os.environ["{env_var}"]' in line or f"os.environ['{env_var}']" in line \
                            or f'os.getenv("{env_var}")' in line or f"os.getenv('{env_var}'')" in line:
                        variable_dict[env_var]["count"] += 1
                        if file_name not in variable_dict[env_var]["files"]:
                            variable_dict[env_var]["files"].append(file_name)
            source_file.close()

    print(f'{env_var:40s}{str(variable_dict[env_var]["count"]):10s}{variable_dict[env_var]["files"]}')
