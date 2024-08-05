# chained-tool-datagen

The general idea of the pipeline is this (currently in development):
```mermaid
graph TD
    A[Curriculum<br>Category, Subcategory, Task] -->|Function Schema Generating LLM| B[Generated Function Schemas]
    B -->|Dummy Function Generating LLM| C[Python Functions<br>with Static Values]
    B -->|User Query Generating LLM| D[User Query]
    D & B --> E[Function Calling LLM]
    E --> F[Thoughts + Function Calls]
    F & C --> G[Function Execution Engine]
    G --> H[Tool Results]
    H -->|Validation LLM| I{Valid?}
    I -->|No| J[Discard]
    I -->|Yes| K[Response Generation LLM]
    B & D --> K
    K --> L[Assistant Reply]
    L --> M{Conversation<br>Complete?}
    M -->|No| N[Follow-up Query Generator LLM]
    N --> D
    M -->|Yes| O[Final Formatting LLM]
    O --> P[Final Dataset Entry]

    subgraph Function Calling Pipeline
        E
        F
        G
        H
        I
        K
    end
```

## Installation and Setup

1. Install the required packages using the following command:
```bash
make install
```

And you should be good to go.

## Usage

### 1. Generating Function Schemas

To generate function schemas, run the following command:
```bash
make run_schema_gen
```

which will save the results to `results/function_schemas.json`.

### 2. Generating User Queries

To generate user queries, run the following command:
```bash
make run_user_query_gen
```

which will save the results to `results/user_queries.json`.

### 3. Generating Dummy Functions

To generate dummy functions, run the following command:
```bash
make run_dummy_function_gen
```

which will save the results to `results/dummy_functions.py`.