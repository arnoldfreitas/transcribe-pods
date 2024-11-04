FROM selenium/standalone-chrome

COPY ./ /home/app

USER root
# Install Python and pip
# Update package lists and install Python, pip, and virtualenv
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

USER 1200
WORKDIR /home/seluser
RUN /usr/bin/python3 -m venv .venv && . .venv/bin/activate && pip install -r /home/app/requirements.txt

# Set the virtual environment as the default Python
ENV PATH="/home/seluser/.venv/bin:$PATH"
ENV SE_OFFLINE=false
WORKDIR /home/app