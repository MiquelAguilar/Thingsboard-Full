# Everything you need to run Thingsboard

- Django API
- thingsboard.deb (Debian Software Package file of Thinsboard compiled)
- sendEmailScheduler.py -> (created as a service and called from a shell script)
  - /lib/systemd/system/iotProxy.service
    - /root/services/aplicationLoader.sh
- python (formatSigfox, sendMsgThingboard, macCheck,...)
