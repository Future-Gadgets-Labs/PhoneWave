FROM python:3.9.9 as deps

WORKDIR /PhoneWave

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.9.9
COPY --from=deps /opt/venv /opt/venv
ENV PATH="opt/venv/bin:$PATH"

WORKDIR /PhoneWave

COPY ./app ./main.py ./.env ./.env.development ./

CMD ["main.py"]