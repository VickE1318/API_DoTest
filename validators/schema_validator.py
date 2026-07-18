def validate_schema(actual_data, expected_schema,path=""):
    missing=[]
    added=[]
    type_changes=[]
    for key in expected_schema:
        current_path = f"{path}.{key}" if path else key
        if key in actual_data:
            if isinstance(actual_data[key],dict) and isinstance(expected_schema[key],dict):
                nested_result=validate_schema(actual_data[key],expected_schema[key],current_path)
                missing.extend(nested_result["missing"])
                added.extend(nested_result["added"])
                type_changes.extend(nested_result["type_changes"])
            else:
                actual_type = type(actual_data[key]).__name__
                if actual_type != expected_schema[key]:
                    type_changes.append({"field":current_path, "expected": expected_schema[key], "actual":actual_type})
        else:
            missing.extend(key)
    for key in actual_data:
        current_path = f"{path}.{key}" if path else key
        if key not in expected_schema:
            added.extend(current_path)

    return {"missing":missing,"added":added,"type_changes":type_changes}
    
   