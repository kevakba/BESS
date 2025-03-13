# Use an official Python image as a base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install required Python libraries
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the project files to the container
COPY . /app

# Expose Jupyter Notebook port
EXPOSE 8888

# Run Jupyter Notebook by default
# CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--no-browser"]

# Set entry point to /home
ENTRYPOINT ["/bin/bash"]