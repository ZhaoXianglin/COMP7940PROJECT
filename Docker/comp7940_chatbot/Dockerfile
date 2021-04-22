FROM python:3.7
COPY /app /app
COPY secert.json secert.json
COPY setup.sh setup.sh
RUN pip install pip update
RUN pip install -r app/requirements.txt
ENV TELE_TOKEN 1688917154:AAGd8RuH7ZrJNLnsh9Dr3zsEPrPe-H1n8nI
ENV KKID  3a00b4f9b9e7a0f8c9b6b6df4752bb0f
ENV KKSecret = 38bb01486702f78bd91d057ecdcefc74
ENV MAP b9c801261a39fb23d6093d8912d51446
ENV MYSQL_USER docker
ENV MYSQL_PWD 123456
ENV MYSQL_HOST mysql
ENV MYSQL_PORT 3306
ENV MYSQL_DB comp7940

CMD ["sh", "setup.sh"]