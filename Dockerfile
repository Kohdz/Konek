FROM python:3
WORKDIR <path of repo>
COPY requirements.txt requirements.txt
ENV SQLALCHEMY_DATABASE_URI="Insert Path to Database Here"
ENV RECAPTCHA_PUBLIC_KEY="Insert Recaptcha Public Key Here"
ENV RECAPTCHA_PRIVATE_KEY="Insert Recaptcha Private Key Here"
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python"]
CMD ["run.py", "runserver", "--host=0.0.0.0"]