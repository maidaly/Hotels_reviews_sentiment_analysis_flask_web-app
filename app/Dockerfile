FROM python:3.8-slim-buster
RUN mkdir /tone_analysis_app
WORKDIR /tone_analysis_app
COPY . /tone_analysis_app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]


