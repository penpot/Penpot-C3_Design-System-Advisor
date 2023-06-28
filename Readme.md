# Idea #3 | Design System Advisor

## 🔎 Idea overview

As a technologist, I want to analyze the ASSETS portion of a Penpot file, **in particular the COMPONENTS subsections**, against their usage in such Penpot file and get a new optimized and efficient version of the ASSETS and LAYERS content to avoid maintenance overload

<br>

## 💡 Feature analysis
### Approach #1 | Identifying unused components [[More](Approach\%231-Identifying_unused_components/Readme.md)]

The system will help users to avoid maintenance overload. The idea is to identify unused components and suggest designers for lightweight Assets.

### Approach #2 | Refactoring duplicated components [[More](Approach\%232-Refactoring_duplicated_components/Readme.md)]
    
The system will help users to avoid maintenance overload. The idea is to group the duplicated components with similar appearance but the same purpose and suggest designers merge the similar ones.

<br>

## 🏁 Final recommendation

[A1] **Identifying unused components** using the simple parsing method for comparing component ids appears more feasible in the short term. On the other hand, [A2] **Refactoring duplicated components** could potentially ship higher effectiveness for the designers; however, the implementation process is more complex with moderate risks. Therefore, we suggest putting [A2] to the long-term target.
