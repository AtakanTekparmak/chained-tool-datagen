import os 

# Declare constants
STATIC_DIR = os.environ.get("STATIC_DIR", "static")
CURRICULUM_PATH = os.environ.get("CURRICULUM_PATH", os.path.join(STATIC_DIR, "curriculum/base.csv"))

# Template paths
FN_CALL_TEMPLATE_PATH = os.environ.get("FN_CALL_TEMPLATE_PATH", "chained_fnc_call.j2")
FN_GENERATE_TEMPLATE_PATH = os.environ.get("FN_GENERATE_TEMPLATE_PATH", "function_schema_generate.j2")
QUERY_GENERATE_TEMPLATE_PATH = os.environ.get("QUERY_GENERATE_TEMPLATE_PATH", "user_query_generate.j2")

# Result directory and paths
RESULT_DIR = os.environ.get("RESULT_DIR", "results")
FN_SCHEMAS_PATH = os.environ.get("FN_SCHEMAS_PATH", os.path.join(RESULT_DIR, "function_schemas.json"))
USER_QUERIES_PATH = os.environ.get("USER_QUERIES_PATH", os.path.join(RESULT_DIR, "user_queries.json"))