FROM python:3
EXPOSE 5000

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=shortener_app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0
CMD ["python", "-m", "flask", "run", "-p", "5000", "--host", "0.0.0.0"]
