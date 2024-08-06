from sqlalchemy import Integer, String, Boolean

def test_true():
    assert True

"""
## TABLE AND COLUMN VALIDATION
"""    

"""
- [] CONFIRM THE PRESENCE OF ALL REQUIRED TABLES WITHIN THE DATABASE SCHEMA
"""
def test_model_structure_table_exists(db_inspector):
    assert db_inspector.has_table("category")
    
"""
-[] VALIDATE THE EXISTENCE OF EXPAND COLUMNS IN EACH TABLE, ENSURING CORRECT DATA TYPES
"""
def test_model_strucutre_column_data_type(db_inspector):
    table = "category"
    columns = {columns["name"]:columns for columns in db_inspector.get_columns(table)}
    
    assert isinstance(columns["id"]["type"], Integer)
    assert isinstance(columns["name"]["type"], String)
    assert isinstance(columns["slug"]["type"], String)
    assert isinstance(columns["is_active"]["type"], Boolean)
    assert isinstance(columns["level"]["type"], Integer)
    assert isinstance(columns["parent_id"]["type"], Integer)
    
"""
- [] VERIFY NULLABLE OR NOT NULLABLE FIELDS
"""

def test_model_structure_nullable_constraints(db_inspector):
    table = "category"
    columns = db_inspector.get_columns(table)
    expected_nullable = {
        "id":False,
        "name":False,
        "slug":False,
        "is_active":False,
        "level":False,
        "parent_id":True,
        }
    for column in columns:
        column_name = column["name"]
        assert column["nullable"] == expected_nullable.get(column_name), f"column '{column_name}' is not nullable as expected"