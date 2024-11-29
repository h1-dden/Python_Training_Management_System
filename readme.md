# Yash Resource Management Tool

## Overview

The Yash Resource Management Tool is an application developed to manage and display insights of Yash’s training for different employees. The system allows users to upload CSV files, visualize data through bar graphs and other visualizations, and apply various filters to dynamically change the displayed data.

## Features

Data Retrieval: Users can upload CSV files to the application.
Data Visualization: The system displays bar graphs and other visualizations based on the uploaded data.
Dynamic Filtering: Users can apply various filters to dynamically change the displayed data.
Download TPR: Users can download Training Progress Report for an overall view

## Technical Details

Programming Language: Python
Libraries: Streamlit, Pandas, Pyplot, Matplotlib, Pymysql
Data Structure: Structured DataFrames
Database: MySQL

## Getting Started

To get started with the Python Training Management System, follow the instructions below:

### Prerequisites

- Python 3.x installed on your machine
- MySQL server installed and running

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/h1-dden/Yash_Resource_Management_Tool
   cd Yash_Resource_Management_Tool

2. **Install Dependencies:**
   ```bash
   Create a virtual environment and activate it.
   Install the required dependencies by running the requirements.txt file.

3. **Set up the database:**
   ```bash
   Run database_creation.txt found in the utils/database_scripts directory in your MySQL environment to create the necessary database structure.
   Execute the insertintosql.py script to populate the database with initial data.

4. **Set up the database:**
   ```bash
   Run database_creation.txt found in the utils/database_scripts directory in your MySQL environment to create the necessary database structure.
   Execute the insertintosql.py script to populate the database with initial data.

4. **Running:**
   ```bash
   Execute streamlit run app.py in console
