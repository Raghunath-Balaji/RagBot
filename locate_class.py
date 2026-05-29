import pkgutil
import importlib
import inspect

def find_class_in_packages(class_name, package_prefixes=['langchain']):
    for info in pkgutil.walk_packages():
        if any(info.name.startswith(prefix) for prefix in package_prefixes):
            try:
                module = importlib.import_module(info.name)
                for name, obj in inspect.getmembers(module):
                    if name == class_name and inspect.isclass(obj):
                        print(f"FOUND: {class_name} is in {info.name}")
                        return
            except Exception:
                continue
    print(f"NOT FOUND: {class_name} could not be located in {package_prefixes}")

find_class_in_packages("ContextualCompressionRetriever")
