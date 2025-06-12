# import os
# import glob

# current_dir = os.path.dirname(__file__)
# modules = glob.glob(os.path.join(current_dir, "*.py"))

# __all__ = []

# for module_path in modules:
#     module_name = os.path.basename(module_path)[:-3]
#     if module_name not in ("__init__",):
#         __import__(f"{__name__}.{module_name}")
#         __all__.append(module_name)