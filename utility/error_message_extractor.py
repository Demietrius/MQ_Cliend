import sys
import csv
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

# Note: This file is meant to be ran from the top level of the project.
# run command 'python ./utility/error_message_extractor.py'.
# If you run from the utility/ folder you'll have to change the path of the template file to ../template.yaml


with open("./template.yaml", "r") as file:
    try:
        yaml_dict = yaml.safe_load(file)
    except yaml.YAMLError as error:
        print(error)
        exit(1)

for key in yaml_dict["Resources"]:
    if yaml_dict["Resources"][key]["Type"] == 'AWS::Serverless::Function':
        error_num = yaml_dict["Resources"][key]["Properties"]["Environment"]["Variables"]["CAG_ERROR_NUMBER"]
        domain = yaml_dict["Resources"][key]["Properties"]["Environment"]["Variables"]["CAG_DOMAIN"]
        source = os.path.dirname(os.path.realpath(__file__)).replace("utility", yaml_dict["Resources"][key]["Properties"]["CodeUri"])
        break


sys.path.append(source)
import Message
with open("./utility/output/error_messages_sheet.csv", "w", newline='') as sheet:
    try:
        message = Message.Message()
        error_messages = message.dictionary
        writer = csv.writer(sheet)
        writer.writerow(("Error Number", "Error Message(EN)", "Type", "HTTP Code", "Error Message (SP)", "Domain"))
        for error in error_messages:
            writer.writerow((error_num+error, error_messages[error], "FATAL", "400", "", domain))
    except csv.Error as error:
        print(error)
        exit(1)

print("error_message_sheet.csv Created Successfully!")
