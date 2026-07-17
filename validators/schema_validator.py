def validate_schema(actual_data, expected_schema):
    missing=[]
    added=[]
    type_changes=[]

    for key in expected_schema:
        if key in actual_data:
            actual_type = type(actual_data[key]).__name__
            if actual_type != expected_schema[key]:
                type_changes.append({"field":key, "expected": expected_schema[key], "actual":actual_type})
        else:
            missing.append(key)
    for key in actual_data:
        if key not in expected_schema:
            added.append(key)

    return {"missing":missing,"added":added,"type_changes":type_changes}
    
   