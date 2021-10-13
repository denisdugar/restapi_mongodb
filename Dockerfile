FROM python
COPY . . 
ENV FLASK_APP=app.py
RUN pip install Flask && pip install pymongo && pip install flask_pymongo && pip install numpy && pip install "pymongo[srv]"
EXPOSE 5000
CMD flask run
