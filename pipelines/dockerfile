FROM ubuntu:14.04
MAINTAINER Zaid Farekh

ENV DEBIAN_FRONTEND noninteractive
RUN mkdir -p /etc/apt /var/run
RUN apt-get update
RUN apt-get install --reinstall -y openssh-server python-apt upstart sysvinit-utils python python-dev python-distribute python-pip git
RUN mv /sbin/initctl.distrib /sbin/initctl
RUN groupadd ubuntu
RUN useradd -g ubuntu -G sudo ubuntu
RUN echo ubuntu:u | chpasswd
RUN cp -a /etc/skel /home/ubuntu
RUN chown -R ubuntu.ubuntu /home/ubuntu
RUN ln -sf /proc/mounts /etc/mtab
RUN echo "ubuntu ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/ubuntu

RUN update-rc.d rsyslog defaults
RUN update-rc.d ssh defaults

RUN mkdir /home/ubuntu/.ssh
RUN chown ubuntu.ubuntu /home/ubuntu/.ssh
RUN chmod 700 /home/ubuntu/.ssh
#RUN echo "<snip>" >> /home/ubuntu/.ssh/authorized_keys
RUN echo UseDNS=no >> /etc/ssh/sshd_config

ENV HOME /home/ubuntu
RUN git clone https://github.com/zaidfarekh/data-science-bootcamp.git /home/ubuntu/josa
RUN pip install -r /home/ubuntu/josa/pipelines/requirements.txt
RUN mkdir /var/log/luigi/
CMD luigid --background --logdir /var/log/luigi/

EXPOSE 22 389 636 3306 8082

ENTRYPOINT exec /sbin/init --startup-event=failsafe-boot
