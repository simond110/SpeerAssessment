# Note-taking API

This is a RESTful API that allows users to create, read, update, delete, share, and search for notes.

## Technology Stack
- **Framework:** Django and Django Rest Framework (DRF)
- **Database:** PostgreSQL
- **Authentication:** Rest Framework TokenAuthentication
- **Testing:** pytest, pytest-django, model_bakery

### Choice of Technologies:

1. **Django & DRF:** 
   - Django is a high-level web framework that encourages rapid development and clean, pragmatic design. 
   - DRF is a powerful and flexible toolkit for building Web APIs on top of Django. Its built-in functionalities save development time and ensure adherence to best practices.
   
2. **PostgreSQL:** 
   - It's a powerful, open-source object-relational database system with a strong reputation for reliability, feature robustness, and performance.
   - Also, there is built-in FullTextSearch feature that can be used in Django

4. **pytest & pytest-django:** 
   - pytest is a mature testing framework in Python that makes it easy to write simple and scalable test cases.
   - pytest-django allows using pytest features with Django.
   - model_bakery allows to create a dummy instance from model.

## Local Setup

### Prerequisites:
- Python >= 3.10
- PostgreSQL >= 15.x
- pip

### Steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Ambitiont109/SpeerAssessment.git
    cd note-taking-api
    ```

2. **Set up a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up PostgreSQL**:
   - Start PostgreSQL and create a new database named `notes_db` or your preferred name.
   - Update the `DATABASES` setting in `settings.py` with your PostgreSQL credentials.

5. **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```

### Running Tests:

Make sure you're in the project root directory and your virtual environment is activated.

```bash
pytest
```
