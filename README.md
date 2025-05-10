# 🥗 PCOS Meal Recommender

**PCOS Meal Recommender** is a Django-based web application designed to recommend healthy meal options tailored for individuals with Polycystic Ovary Syndrome (PCOS). It uses a combination of nutritional database found in Kaggle and customized algorithms to personalize food suggestions and support healthier lifestyle choices.

---

## 📁 Project Structure

```
PCOSSAPP
├── pcos/                    # Django project settings
├── pcosapp/                  # Main app containing recommendation logic
├── db.sqlite3               # SQLite database
└── manage.py                # Django management script
└── path.code-workspace   
```

(*Note: Adjust folder names to match your actual setup if different.*)

---

## 🚀 Getting Started

Follow these steps to set up and run the app locally.

### 🔗 Clone the Repository

```bash
git clone https://github.com/hustinaa/PCOSApp.git
```

### 🛠️ Set Up the Environment

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> If not yet created, generate the requirements file with:
> ```bash
> pip freeze > requirements.txt
> ```

---

### 🗄️ Run the Server

Apply migrations and start the development server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 👩‍⚕️ Features

- Personalized meal recommendations based on dietary needs for PCOS
- Input-based filtering (e.g., calorie preference, sugar level, meal type)
- Clean, user-friendly UI
- Easily extendable for additional medical or nutritional use cases

---

## 🧠 Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS (Bootstrap or Tailwind)
- **Database**: SQLite
- **ML/Logic**: Custom rules or basic algorithms (KNN, Decision Trees, etc.)

---

## 👩‍💻 About the Developers

Developed by Justine Evora, Christine Sotoza, Amina Javellana 
Currently studying **Management Information Systems** at **Ateneo de Manila University**.

If you find this project helpful, feel free to give it a ⭐ and connect!
