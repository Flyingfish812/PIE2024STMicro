# Project: Supervised Learning for Evaluating Microelectronic Components Similarity

---

## Project Description

This is a group engineering project (projet d'ingénierie en équipe, PIE) of ENSTA 2024. This project focuses on applying supervised learning techniques to evaluate the similarity of microelectronic components based on their characteristics. The goal is to develop a system that compares two components and provides a similarity score. The project will start with basic machine learning models like regression and decision trees, progressing to neural networks and semi-supervised methods. An important aspect is fine-tuning the models on new datasets, with input from engineers at STMicroelectronics.

## Project Objectives

- Develop algorithms to evaluate the similarity between microelectronic components.
- Explore a range of machine learning models, starting from basic to advanced techniques.
- Implement a model specialization system for small datasets.
- Work closely with engineers to refine models based on feedback.

## Expected Deliverables

- A machine learning algorithm that outputs a similarity score for components.
- A refined methodology incorporating iterative feedback from engineers.
- A final report detailing methods, results, and conclusions.

---

## File Structure

```
/project_root
│
├── /data                   # Directory for datasets and preprocessed data
│   ├── dataset.csv
│   └── README_data.txt      # Documentation for datasets
│
├── /src                    # Main codebase
│   ├── main.py             # Main script to run the models
│   ├── models.py           # Script containing model implementations
│   ├── utils.py            # Utility functions (data processing, etc.)
│   └── train.py            # Model training scripts
│
├── /notebooks              # Jupyter notebooks for exploratory data analysis (EDA)
│   └── eda_component_similarity.ipynb
│
├── /results                # Output results like model evaluation and plots
│   ├── model_results.csv
│   └── evaluation_plots.png
│
├── requirements.txt        # Python package dependencies
├── README.md               # Project description and instructions
└── LICENSE.txt             # License information
```

---

## Nomenclature

To ensure consistency across the project, the following conventions are adopted for naming variables, functions, classes, and files:

1. **Variables and Functions:**
   - Use snake_case for variable and function names: e.g., `similarity_score`, `train_model()`.
   - Use descriptive names to convey the purpose: e.g., `model_accuracy`, `load_dataset()`.

2. **Classes:**
   - Use PascalCase for class names: e.g., `SimilarityModel`, `DataLoader`.

3. **File Names:**
   - Use lowercase and underscores for Python scripts: e.g., `train_model.py`, `data_preprocessing.py`.
   - Keep file names concise yet descriptive.

4. **Comments:**
   - Provide comments for complex logic or important function steps.
   - Docstrings should be used for every function and class explaining their purpose and parameters.

**Example:**

```python
class SimilarityModel:
    """
    This class implements different models to evaluate component similarity.
    """
    def __init__(self, model_type: str):
        self.model_type = model_type
        # Initialize the model based on type
    
    def train(self, X_train, y_train):
        """
        Trains the selected model using the training data.
        """
        # Training logic here
    
    def evaluate(self, X_test, y_test):
        """
        Evaluates the model on the test dataset.
        """
        # Evaluation logic here
```

**Version Control:**

We use the `MAJOR.MINOR.PATCH` paradigm to control the development of the project.

- **MAJOR**: Incremented when there are incompatible API changes.
- **MINOR**: Incremented when adding functionality in a backward-compatible manner.
- **PATCH**: Incremented when making backward-compatible bug fixes.

---

## Project Members

- **Anthony Aoun** - Project Supervisor
- **Philippe Rochette** - Project Supervisor

- **WANG Yuran** - Project Manager
- **AROUS Mohamed Amine**
- **BASTIANELLO LIMA Gabriel**
- **BEN ARBIA Imene**
- **EZZINA Mohamed Naceur**
- **GASSEM Adam**
- **GHNIMI Mohamed Neji**
- **GHOZZI Seifeddine**
- **HIDOURI Ameni**
- **HUANG Lingyun**
- **LÓPEZ NIETO Nicolás**
- **YANG Shuya**

For any questions or clarifications, please contact **anthony.aoun@st.com** or **philippe.rochette@st.com**.
