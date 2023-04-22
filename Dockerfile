FROM python:3.10

# Create a directory where the code is to be hosted
RUN mkdir /fortunato-wheels
# Define the working directory in the container
WORKDIR /fortunato-wheels 
# Copy and install the requirements.
COPY requirements.txt /fortunato-wheels/requirements.txt
RUN pip install -r requirements.txt

COPY src/ /fortunato-wheels/src/
COPY data/processed/ /fortunato-wheels/data/processed/

# Define environment variables
ENV dash_port=8050
ENV dash_debug="True"

EXPOSE 8050

CMD ["python", "src/app.py"]