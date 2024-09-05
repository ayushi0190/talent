FROM python:3.8.5-slim

RUN apt-get update && apt-get install -y libmariadb-dev gcc openssh-server
RUN echo PermitRootLogin yes >> /etc/ssh/sshd_config
RUN echo root:newadminpasswd | chpasswd

WORKDIR /api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 9003 22


RUN chmod +x start.sh
ENTRYPOINT ["/api/start.sh"]
#CMD [ "python3","-m","src.routes.main" ]