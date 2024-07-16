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

1. Pull [data-genie-agents](https://github.com/interstellarninja/data-genie-agents):
```bash
make data_genie_setup
```

2. Create a virtualenv and install the requirements:        
```bash
make install
```

3. Add your `GROQ_API_KEY` to the `.env` file.

## Usage

To run the pipeline:
```bash
make run
```
