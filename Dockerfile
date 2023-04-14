FROM python:3.10.8 AS stage_1
WORKDIR /app
COPY req.txt req.txt
RUN python -m venv venv && venv/bin/pip install --upgrade pip wheel setuptools
RUN apt-get update && apt-get install -y wget gnupg unzip
RUN venv/bin/pip install -r req.txt
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get update && apt-get install -y sudo && apt-get -y --no-install-recommends install libgbm1
RUN sudo apt-get update && sudo apt-get install -y fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libgtk-3-0 libnspr4 libnss3 libu2f-udev libvulkan1 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils
RUN sudo dpkg -i google-chrome-stable_current_amd64.deb && sudo apt --fix-broken install -y
RUN curl -Lo chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/112.0.5615.49/chromedriver_linux64.zip"
RUN sudo apt install unzip
RUN mkdir -p "chromedriver/stable" && \
    unzip -q "chromedriver_linux64.zip" -d "chromedriver/stable" && \
    chmod +x "chromedriver/stable/chromedriver"
COPY . /app
ENTRYPOINT [ "/app/venv/bin/python","/app/main.py" ]

FROM stage_1 AS stage_2
WORKDIR /app
COPY req.txt req.txt
RUN apt-get update && apt-get upgrade -y && apt-get install virtualenv pkg-config -y
RUN python -m venv venv && venv/bin/pip install --upgrade pip wheel setuptools
RUN venv/bin/pip install -r req.txt
COPY . /app
EXPOSE 8050
ENTRYPOINT [ "/app/venv/bin/python","/app/Dashboard.py" ]