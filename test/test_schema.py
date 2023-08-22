import json
import jsonschema
import pathlib
import pytest
import referencing


ROOT_DIR = pathlib.Path(__file__).parent.parent
OBJECT_FILES = (ROOT_DIR / "objects").rglob("*.json")
EVENT_FILES = (ROOT_DIR / "events").rglob("*.json")
BASE_URI = "https://schemas.ocsf.io/"


@pytest.fixture
def registry():
    registry = referencing.Registry()
    for schema_file_path in (ROOT_DIR / "test").rglob("*.schema.json"):
        with open(schema_file_path, 'r') as file:
            schema = json.load(file)
            resource = referencing.Resource.from_contents(schema)
            registry = registry.with_resource(BASE_URI + schema_file_path.name, resource=resource)

    return registry


def id_from_filepath(file_path: pathlib.Path):
    return str(file_path.relative_to(ROOT_DIR))


@pytest.mark.parametrize("object_file_path", OBJECT_FILES, ids=id_from_filepath)
def test_object(registry, object_file_path):
    schema = registry.resolver(BASE_URI).lookup("object.schema.json").contents

    with open(object_file_path, 'r') as file:
        instance = json.load(file)

    validator = jsonschema.Draft202012Validator(schema, registry=registry)
    validator.validate(instance)


@pytest.mark.parametrize("event_file_path", EVENT_FILES, ids=id_from_filepath)
def test_event(registry, event_file_path):
    schema = registry.resolver(BASE_URI).lookup("event.schema.json").contents

    with open(event_file_path, 'r') as file:
        instance = json.load(file)

    validator = jsonschema.Draft202012Validator(schema, registry=registry)
    validator.validate(instance)
