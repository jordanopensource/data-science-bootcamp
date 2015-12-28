FROM zaidfarekh/josa-luigi
MAINTAINER Zaid Farekh


RUN git clone https://github.com/zaidfarekh/data-science-bootcamp.git /home/ubuntu/josa
RUN pip install -r /home/ubuntu/josa/pipelines/requirements.txt
RUN mkdir /var/log/luigi/
CMD luigid --background --logdir /var/log/luigi/

EXPOSE 22 389 636 3306 0.0.0.0:8082

ENTRYPOINT exec /sbin/init --startup-event=failsafe-boot
