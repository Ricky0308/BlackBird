FROM python:3.8
WORKDIR /backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /backend/
# COPY . /backend/
RUN pip install -r requirements.txt 
#CMD python manage.py runserver 0.0.0.0:8000
CMD /bin/bash

# command 
# docker image build -t blackbird .
# docker container run --rm --name test_blackbird_ricky -v /Users/ricky/dev/BlackBird:/backend -it -p 8000:8000 blackbird
# -v /Users/ricky/dev/BlackBird:/backend

# commands
# docker container start -i 
# docker container exec -it "bin/bash"