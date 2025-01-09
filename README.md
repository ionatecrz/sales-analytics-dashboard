# Sales Analytics Dashboard

## Project Description

This project focuses on building an interactive Sales Analytics Dashboard to provide valuable insights into sales performance, customer behavior, and promotional effectiveness. By leveraging modern visualization techniques with Dash and Plotly, the dashboard enables businesses to explore data dynamically and make informed decisions based on real-time analysis.

## Repository Contents

- **`data/`**: Contains the sales datasets used for analysis and visualization.
- **`notebooks/`**: Includes the notebook `sales_dashboard.ipynb`, which documents the development process and initial data exploration.
- **`scripts/`**:
  - `config.py`: Manages styling configurations for tabs and charts.
  - `tabs_content.py`: Defines the content of each dashboard tab, including metrics, graphs, and documentation.
  - `utils.py`: Provides helper functions for data loading, graph generation, and component creation.
- **`app.py`**: Runs the Dash application, managing layout, tabs, and callbacks.
- **`requirements.txt`**: Lists the dependencies required to run the dashboard.
- **`README.md`**: This file, offering an overview of the project and usage instructions.

## Requirements

- **Python**: >= 3.7
- Key Libraries:
  - **Data Manipulation**: `pandas`, `numpy`
  - **Visualization**: `plotly`, `dash`
  - **Development**: `jupyter-dash`

## Usage Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ionatecrz/sales-analytics-dashboard.git
   cd sales-analytics-dashboard
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   - Execute the `app.py` script:
     
     ```bash
     python scripts/app.py
     ```
   - Open the dashboard in your browser at `http://localhost:5001`.

4. **Explore the notebook**:
   - Open the `notebooks/sales_dashboard.ipynb` file using Jupyter Notebook or Jupyter Lab to review data exploration and development steps.

## Dashboard Features

- **Tab 1: Resumen de Métricas**:
  - Key metrics like the number of stores, products, and states.
  - Graphs for top-selling products, monthly sales, and sales by day and state.
- **Tab 2: Análisis por Tienda**:
  - Store-specific analysis, including annual sales, product sales, and promotional performance.
- **Tab 3: Análisis Avanzado**:
  - In-depth seasonal analysis, multidimensional comparisons, and sales pattern heatmaps.
- **Tab 4: Documentación**:
  - Detailed explanations of each tab and design decisions.

## Business Benefits

- **Real-Time Insights**: Provides actionable insights for optimizing sales strategies and promotions.
- **Customizable Analysis**: Allows users to drill down into specific stores, products, or regions.
- **Enhanced Decision-Making**: Facilitates data-driven strategies for improving performance.

## Author

- **Author Name**: Íñigo de Oñate Cruz
- **Contact**: [LinkedIn](https://www.linkedin.com/in/%C3%AD%C3%B1igo-de-o%C3%B1ate-cruz-855b55263/)

## License

This project is licensed under the [MIT License](LICENSE), allowing use, modification, and distribution.
