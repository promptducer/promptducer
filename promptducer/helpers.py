import importlib
import importlib.util
import os
from abc import ABC
from typing import Type


def import_module(path: str, class_name: str = None, parent_class: Type[ABC] = None):
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: {path}")
    if not class_name:
        class_name = os.path.basename(path.replace(".py", ""))
    spec = importlib.util.spec_from_file_location(class_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        dynamic_class = getattr(module, class_name)
    except AttributeError as ae:
        print(f"Cannot find the class {class_name}!")
        raise

    return dynamic_class

# def find_modules(json_field_name: str, parent_class: Type[ABC], use_class_names: bool):
#     PATHS = json.loads(FileUtility.read_file("paths.json"))
#
#     modules_dir = PATHS.get(json_field_name)
#     if not modules_dir:
#         raise ValueError(f"Please provide the field '{json_field_name}' in the paths.json file.")
#
#     classes_dict = {}
#     files = os.listdir(modules_dir)
#     module_names = [os.path.splitext(file)[0] for file in files if file.endswith('.py') and file != '__init__.py']
#
#     for module_name in module_names:
#         module_import_name = ".".join(modules_dir.split("/")[0:] + [module_name])
#         module = importlib.import_module(module_import_name)
#         classes = inspect.getmembers(module, inspect.isclass)
#         for name, module_class in classes:
#             if issubclass(module_class, parent_class):
#                 classes_dict[module_name if not use_class_names else name] = module_class
#
#     if len(classes_dict):
#         return classes_dict
#     else:
#         raise NotImplementedError(f"No classes found with parent {parent_class}."
#                                   f"Please check if '{json_field_name}' field has the correct path value in the"
#                                   f"paths.json file.")
