FROM python:3-onbuild
EXPOSE 5000
ENV PYTHONPATH .
CMD ["python", "./main.py","--file=interface.raml"]
