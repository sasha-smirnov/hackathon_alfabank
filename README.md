Hack&Change 2025 — Альфа-Банк

Репозиторий проекта: [https://github.com/sasha-smirnov/hackathon_alfabank](https://github.com/sasha-smirnov/hackathon_alfabank)

Проект состоит из:

ML-модели (CatBoost)
backend-сервиса (FastAPI)
frontend-приложения (React + Vite)
системы рекомендаций
документации и демонстрационного видео

Команда проекта

Участник Роль
Александр Смирнов, Глеб Колясников - ML Engineer
Александра Васенина - Backend Developer
Артём Саидов - Frontend Developer 


Технологический стек

catboost==1.2.8
cloudpickle==3.1.2
contourpy==1.3.3
cycler==0.12.1
fonttools==4.61.0
graphviz==0.21
joblib==1.5.2
kiwisolver==1.4.9
llvmlite==0.45.1
matplotlib==3.10.7
narwhals==2.12.0
numba==0.62.1
numpy==2.3.5
packaging==25.0
pandas==2.3.3
pillow==12.0.0
plotly==6.5.0
pyparsing==3.2.5
python-dateutil==2.9.0.post0
pytz==2025.2
scikit-learn==1.7.2
scipy==1.16.3
shap==0.50.0
six==1.17.0
slicer==0.0.8
threadpoolctl==3.6.0
tqdm==4.67.1
typing_extensions==4.15.0
tzdata==2025.2
fastapi==0.115.0
uvicorn==0.30.1
pandas==2.0.3
numpy==1.24.4
catboost==1.2.3
shap==0.43.0
joblib==1.3.2

Запуск проекта

Клонирование репозитория

git clone https://github.com/sasha-smirnov/hackathon_alfabank
cd hackathon_alfabank


Запуск backend

cd backend
pip install -r requirements.txt
python -m venv venv
(windows) venv\Scripts\activate
(mac) source venv/bin/activate
pip install fastapi uvicorn catboost numpy pandas shap pyarrow joblib
source venv/bin/activate
uvicorn main:app --reload --port 8000

Запуск frontend

cd frontend
npm install
npm run dev


После запуска frontend доступен по адресу:
http://localhost:5173


API Эндпоинты

Метод       Путь            Назначение              

`POST`  `/predict`    Предсказать доход клиента    
`POST`  `/explain`    SHAP-объяснение предсказания 
`POST`  `/recommend`  Персональные рекомендации   


ML-модель

Модель: CatBoostRegressor
https://drive.google.com/drive/folders/1P-jwOWQF-AQ13bUxmgGqBWgMouoHPj_3?usp=share_link

