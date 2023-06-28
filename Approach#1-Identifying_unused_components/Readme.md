# Approach #1 | Identifying unused components
    
The system will help users to avoid maintenance overload. The idea is to identify unused components and suggest designers for lightweight Assets.

| Technology readiness | Risks | Complexity |
| ----- | ----- | ---------- |
| 🟢 Ready for implementation | <div style="width: 100pt"> 🟡 Moderate risk | <div style="width: 150pt"> 🟢 Light complexity |


## Technologies *(No need AI)*

Check component ID within the exported Penpot file by parsing:
- <pages_id>.svg: parse by `penpot:component-id`
- components.svg: parse by `symbol`

## Requirements

- a python script for: [[Sample](sample.py)]

    1. Extract component-id from <pages_id>.svg and components.svg
    2. Then, compare and identify the unused components
- Input: exported penpot files
- Output: unused component name/id
- Data: no need for training data

## Pros and Cons

🟢 Pros
    
- Ready to use
- Simple and effective
- AI is not used for this task as it is more rule-based in nature, which ensures higher accuracy without relying on AI.

🔴 Cons

- It might be less attractive for designers than the co-pilot
