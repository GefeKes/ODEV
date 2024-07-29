FROM python:3.11.9
WORKDIR  /app
COPY .   /app
RUN pip install -r req.txt
CMD ["python3", "Gorkem_Efe_Odev.py"]