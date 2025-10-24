-----

# OrbitMe - Intelligent Life Management System

OrbitMe is an intelligent life management platform designed to harmonize your personal and professional life. It provides data-driven insights, intelligent tracking, and actionable analytics to help you monitor wellness, optimize productivity, and achieve your goals.

-----

\#\# Key Features

  * **Main Dashboard:** A central "at-a-glance" hub (`App.py`) showing key stats, core capabilities, and recent activity.
  * **Work Management:** (`Work.py`) A full CRUD (Create, Read, Update, Delete) module to manage tasks. Track by category, priority, status, hours, and deadlines.
  * **Health Tracking:** (`Health.py`) A module to log daily health metrics such as mood, sleep, steps, stress, and more.
  * **Goal Tracking:** (`Goals.py`) A dedicated module to set, track, and manage long-term personal and professional goals with progress bars and milestones.
  * **Analytics Dashboard:** (`Dashboard.py`) A comprehensive page for visualizing trends in both health and work data using interactive Plotly charts.
  * **Advanced Analytics:** (`Analytics.py`) A deep-dive module to find powerful correlations between different life areas, such as the impact of sleep on mood or work hours on stress.
  * **Modern UI:** A beautiful, responsive interface built with custom CSS, featuring "glass morphism" cards, animated gradients, and a clean, professional layout.
  * **Data-Driven:** Uses `pandas` for data manipulation and persists all data to local `.csv` files (`work_data.csv`, `health_data.csv`, `goals_data.csv`).

-----

## \#\# Project Structure

This is a multi-page Streamlit application. To run it correctly, you must organize the files into the following directory structure:

```
OrbitMe_Project/
│
├── App.py               # This is the main homepage
│
├── pages/               # All other pages MUST go in this folder
│   ├── 1_Dashboard.py     # (Visualizes all data)
│   ├── 2_Work.py          # (Module for task management)
│   ├── 3_Health.py        # (Module for logging health data)
│   ├── 4_Analytics.py     # (Module for deep-dive analysis)
│   └── 5_Goals.py         # (Module for goal tracking)
│
├── data/                # Create this folder to store the data
│   ├── health_data.csv    # (Created by Health.py)
│   ├── work_data.csv      # (Created by Work.py)
│   └── goals_data.csv     # (Created by Goals.py)
│
├── requirements.txt     # Project dependencies
├── data_processor.py    # (Utility file for data loading)
└── style.css            # (Contains some CSS, though most is in App.py)
```

**Note:** The page numbering (e.g., `1_Dashboard.py`) is a Streamlit convention to set the display order in the sidebar.

-----

## \#\# Installation & Setup

1.  **Clone or Download:** Get the project files onto your local machine.

2.  **Arrange Files:** Create the `pages/` and `data/` directories and move the Python files into the structure shown above.

3.  **Create Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  **Install Dependencies:** Install all required libraries from the `requirements.txt` file.

    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the App:**

    ```bash
    streamlit run App.py
    ```

    Your browser should automatically open to the OrbitMe application.

-----

\#\# How to Use

1.  **Home Page:** The app will open on the main `App.py` dashboard. This gives you a high-level overview.
2.  **Add Data:** Use the sidebar to navigate to:
      * **Work:** To add, update, and manage your daily tasks.
      * **Health:** To log your daily wellness metrics.
      * **Goals:** To set and track your long-term objectives.
3.  **Analyze Data:** Navigate to:
      * **Dashboard:** To see visual trends and summaries of your work and health data.
      * **Analytics:** To explore correlations and gain deeper insights into how your habits affect each other.
4.  **Export:** The `Dashboard` and `Analytics` pages have sidebar controls to export your data as a `.csv` file.

-----

 \#\# Dependencies

This project relies on the following Python libraries:

  * `streamlit==1.28.0`
  * `pandas==2.0.3`
  * `plotly==5.15.0`
  * `openpyxl==3.1.2`
