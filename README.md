![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)





# NLP Query Engine for Employee Data 



This project is a full-stack web application that serves as a powerful natural language interface for querying both a structured employee database (PostgreSQL) and unstructured text documents. It features a hybrid AI query engine that can translate human questions into SQL and perform semantic searches to provide comprehensive answers.



![screenshot-name.png](https://user-images.githubusercontent.com/...)

## Core Features 



* **Dynamic Schema Discovery:** The backend automatically connects to and analyzes any PostgreSQL database, discovering its tables, columns, and relationships without any hard-coding. This allows the engine to be portable and adaptable.

* **Hybrid Query Engine:** The system intelligently processes user queries to fetch information from multiple sources simultaneously:

    * **Text-to-SQL:** Utilizes the Google Gemini Pro model to translate complex natural language questions into precise, executable PostgreSQL queries.

    * **Semantic Document Search:** Employs Sentence Transformers and a FAISS vector index to find the most contextually relevant information from a collection of text documents (e.g., resumes, performance reviews).

* **Full-Stack Implementation:**

    * A robust **FastAPI** backend that serves the AI logic through a clean REST API.

    * A polished and responsive **React** frontend for a smooth user experience.



## Architectural Decisions & Development Journey



The initial goal was to build a fully containerized, production-ready environment using Docker and WSL 2. This approach was chosen to ensure maximum portability and alignment with modern deployment practices.



During the setup phase, significant and persistent environment-specific performance and networking issues were encountered on the development machine, blocking progress. To prioritize delivering a robust, fully functional application that demonstrates all core AI requirements within the given timeframe, a **pragmatic decision was made to pivot to a native installation**.



This pivot guaranteed stability and allowed the focus to remain on the quality of the application logic, resulting in the successful implementation of the complex hybrid query engine. This journey highlights a key engineering skill: making smart, deadline-oriented trade-offs to ensure project success.



## Technology Stack 



* **Backend:** Python, FastAPI, SQLAlchemy, Google Generative AI (Gemini), Sentence-Transformers, Faiss

* **Frontend:** React, Axios, CSS

* **Database:** PostgreSQL



## Setup and Installation



### Prerequisites

* Python 3.9+

* PostgreSQL 13+

* Node.js and npm



### Backend Setup

1.  Navigate to the project root and create/activate a Python virtual environment:

    ```bash

    python -m venv venv

    venv\Scripts\activate

    ```

2.  Install all required dependencies:

    ```bash

    pip install -r requirements.txt

    ```

3.  Create a `.env` file in the project root and add your configuration:

    ```

    DATABASE_URL="postgresql://postgres:YOUR_DB_PASSWORD@127.0.0.1:5432/postgres"

    GEMINI_API_KEY="AIzaSy...Your-API-Key"

    ```

4.  Navigate into the backend directory and start the server:

    ```bash

    cd backend

    python -m uvicorn main:app --reload

    ```

    The backend will be running at `http://localhost:8000`.



### Frontend Setup

1.  In a new terminal, navigate to the frontend directory:

    ```bash

    cd frontend

    ```

2.  Install all dependencies:

    ```bash

    npm install

    ```

3.  Start the frontend application:

    ```bash

    npm start

    ```

    The frontend will open in your browser at `http://localhost:3000`.



## Future Enhancements

This project successfully implements the core AI engine. Future work could include:

* **Full Data Ingestion UI:** Building the frontend components for database connections and drag-and-drop document uploads.

* **Schema Visualization:** Adding a UI component to graphically display the discovered database schema.

* **Advanced Caching:** Implementing an intelligent caching layer (e.g., Redis) for frequently accessed queries and results.

* **Containerization:** Re-visiting and completing the original Docker implementation for simplified deployment.
