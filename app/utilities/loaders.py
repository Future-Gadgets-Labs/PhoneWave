from importlib.resources import contents
import importlib

from . import logger


def load_extentions(client):
    """Load all extentions in the app/extentions folder"""
    extentions = [ext for ext in contents("app.extentions") if not ext.startswith("_")]

    for ext in extentions:
        try:
            client.load_extension(f"app.extentions.{ext}")
            logger.info(f"Loaded extention: {ext}")
        except Exception as e:
            logger.error(f"Failed to load extention: {ext}")
            logger.error(e)


def load_modules(client, parent):
    client.add_cog(parent)

    parent_package = ".".join(parent.__module__.split(".")[:-1])
    parent_modules_path = f"{parent_package}.modules"

    for module in contents(parent_modules_path):
        if module.startswith("_"):
            continue

        module_name = module.split(".")[0]
        module_path = f"{parent_modules_path}.{module_name}"
        module_class = getattr(importlib.import_module(module_path), "__CLASS", None)

        if module_class:
            client.add_cog(module_class(client, parent))
        else:
            logger.warning(f"Module {module_name} has no __CLASS attribute")
