FROM python:alpine3.15

COPY . /app
WORKDIR /app
RUN chmod -R a+w /app

RUN if [ -d "build" ]; then rm -rf build; fi \
  && python -m pip wheel -w /app/dist --verbose . \
  && python -m pip install /app/dist/ffhelper*.whl
