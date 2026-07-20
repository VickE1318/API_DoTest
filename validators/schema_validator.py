class SchemaValidator:

    def validate_data(self,actual_data, expected_schema,path=""):
        missing=[]
        added=[]
        type_changes=[]

        for key in expected_schema:            
            current_path = f"{path}.{key}" if path else key

            if key in actual_data:
                actual_value = actual_data[key]
                expected_value = expected_schema[key]
                #Handing lists
                if isinstance(actual_value,list) and isinstance(expected_value,list):
                    expected_item_schema = expected_value[0] if len(expected_value) > 0 else None

                    for index, item in enumerate(actual_value):
                        item_path = f"{current_path}[{index}]"

                        if isinstance(item,dict) and isinstance(expected_item_schema, dict):
                            nested_result_list=self.validate_data(item,expected_item_schema,item_path)
                            missing.extend(nested_result_list["missing"])
                            added.extend(nested_result_list["added"])
                            type_changes.extend(nested_result_list["type_changes"])
                        elif expected_item_schema is not None:
                            type_changes.extend(self.validate_type(item,expected_item_schema,item_path))
                #Handling Dictionaries
                elif isinstance(actual_value,dict) and isinstance(expected_value,dict):
                    nested_result=self.validate_data(actual_value,expected_value,current_path)
                    missing.extend(nested_result["missing"])
                    added.extend(nested_result["added"])
                    type_changes.extend(nested_result["type_changes"])
                #Handling Primitives
                else:
                    type_changes.extend(self.validate_type(actual_value,expected_value,current_path))

            else:
                missing.append(current_path)

        for key in actual_data:
            current_path = f"{path}.{key}" if path else key
            if key not in expected_schema:
                added.append(current_path)
        
        return {"missing":missing,"added":added,"type_changes":type_changes}
    
    def validate_type(self,actual_value,expected_value,current_path):
        type_changes=[]
        actual_type = type(actual_value).__name__
        expected_type_name = expected_value.__name__ if isinstance(expected_value, type) else str(expected_value)
        if actual_type != expected_type_name:
            type_changes.append({"field":current_path, "expected": expected_type_name, "actual":actual_type})
        return type_changes
    
   