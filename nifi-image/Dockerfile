FROM apache/nifi
COPY mysql-connector-j-9.0.0.jar /opt/nifi/nifi-current/lib/lib/mysql-connector-j-9.0.0.jar
ADD properties.tar /opt/nifi/nifi-current/conf/
ENTRYPOINT ["../scripts/start.sh"]