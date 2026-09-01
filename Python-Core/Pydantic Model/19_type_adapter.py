# ================================================================
#               PYDANTIC - TYPEADAPTER
#
# TypeAdapter → Validates, parses and serializes Python types
#               without requiring a BaseModel
#
# validate_python() → Validates Python objects
# validate_json()   → Validates JSON data
# dump_python()     → Converts validated data into Python objects
# dump_json()       → Serializes validated data into JSON
# =================================================================

from pydantic import TypeAdapter


# List of Integers

numbers_adapter = TypeAdapter(list[int])


# ------------------------------------------------------------
# validate_python()
# ------------------------------------------------------------

numbers = numbers_adapter.validate_python(
    [10, 20, 30]
)

print("Validated Numbers:")
print(numbers)

print("Type:")
print(type(numbers))


# ------------------------------------------------------------
# validate_python() with conversion
# ------------------------------------------------------------

numbers = numbers_adapter.validate_python(
    ["10", "20", "30"]
)

print("\nConverted Numbers:")
print(numbers)


# ------------------------------------------------------------
# validate_json()
# ------------------------------------------------------------

numbers = numbers_adapter.validate_json(
    '[10, 20, 30]'
)

print("\nValidated JSON:")
print(numbers)


# ------------------------------------------------------------
# dump_python()
# ------------------------------------------------------------

python_data = numbers_adapter.dump_python(
    numbers
)

print("\nPython Data:")
print(python_data)

print("Type:")
print(type(python_data))


# ------------------------------------------------------------
# dump_json()
# ------------------------------------------------------------

json_data = numbers_adapter.dump_json(
    numbers
)

print("\nJSON Data:")
print(json_data)

print("Type:")
print(type(json_data))

