# Installing Kaltura on a Single Server (RPM)
This guide describes RPM installation of an all-in-one Kaltura server and applies to all major RH based Linux distros including Fedora Core, RHEL, CentOS, etc.
([Note the supported distros and versions](http://kaltura.github.io/platform-install-packages/#supported-distros)).

**Kaltura CE was just ported to CentOS/RHEL 8. Please note that this is a beta version and one must exercise judgement before deploying it to Prod ENVs.**

[Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.

#### Table of Contents
[Prerequites](pre-requisites.md)

[Pre-Install Steps](install-kaltura-redhat-based.md#pre-install-steps)

[Non-SSL Step-by-step Installation](install-kaltura-redhat-based.md#non-ssl-step-by-step-installation)

[Apache SSL Step-by-step Installation](install-kaltura-redhat-based.md#apache-ssl-step-by-step-installation)

[Nginx SSL Configuration](nginx-ssl-config.md)

[Securing Monit](install-kaltura-redhat-based.md#securing-monit)

[Unattended Installation](install-kaltura-redhat-based.md#unattended-installation)

[Live Streaming with Nginx and the RTMP module](install-kaltura-redhat-based.md#live-streaming-with-nginx-and-the-rtmp-module)

[Upgrade Kaltura](install-kaltura-redhat-based.md#upgrade-kaltura)

[Remove Kaltura](install-kaltura-redhat-based.md#remove-kaltura)

[Troubleshooting](install-kaltura-redhat-based.md#troubleshooting)

[Additional Information](install-kaltura-redhat-based.md#additional-information)

[How to contribute](CONTRIBUTERS.md)

## Pre-Install steps
* This guide assumes that you have a clean, basic install of one of the RHEL based OS's in 64bit architecture.
* During the installation process, you will be prompted about several hostnames. Note that it is crucial that all host names will be resolvable by other members of the cluster (and outside the cluster in the case of API/front machines). Before installing, verify that your DNS contains records for all the hostnames you intend to use or that the /etc/hosts file on all machines is properly configured to include them.
* Before you begin, make sure you're logged in as the system root. Root access is required to install Kaltura, and you should execute `sudo -i` or `su -` to make sure that you are indeed root.

#### Firewall requirements
Kaltura requires certain ports to be open for proper operation. [See the list of required open ports](kaltura-required-ports.md).
If you're **just testing locally** and don't mind an open system, you can use the below to disable iptables altogether:
```bash
# iptables -F
# service iptables stop
# chkconfig iptables off
```
#### Set SELinux to permissive mode - REQUIRED
**Currently Kaltura doesn't properly support running with SELinux in `enforcing` mode, things will break if you don't set it to permissive**.

```bash
# setenforce permissive
```

To verify SELinux will not revert to enabled next restart:

1. Edit the file `/etc/selinux/config`
1. Verify or change the value of SELINUX to permissive: `SELINUX=permissive`
1. Save the file `/etc/selinux/config`

#### Setup the Kaltura RPM repository

```bash
# rpm -ihv http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
```

#### Additional repos
Before proceeding with the deployment process, please ensure that the EPEL repos are enabled.

#### Installing on AWS EC2 instances
Depending on your setup, you may need to enable two additional repos: rhui-REGION-rhel-server-extras and rhui-REGION-rhel-server-optional.
This can be done by editing /etc/yum.repos.d/redhat-rhui.repo and changing:
```
enabled=0
```
to:
```
enabled=1
```
under the following sections:
```
rhui-REGION-rhel-server-optional
rhui-REGION-rhel-server-extras
```

Or by running the following commands:
```
# yum -y install yum-utils
# yum-config-manager --enable rhui-REGION-rhel-server-extras rhui-REGION-rhel-server-optional
```

#### Enabling the EPEL repo
See https://fedoraproject.org/wiki/EPEL#Quickstart

#### Enabling the Remi repos
Please see: https://blog.remirepo.net/post/2017/12/04/Install-PHP-7.2-on-CentOS-RHEL-or-Fedora
Then, run:
```
# dnf module reset php
# dnf module install php:remi-7.2
```


The `kaltura-nginx` package depends on certain packages from the main Remi repo.
In addition, while Kaltura CE can work with PHP 5.5 and above, we highly recommend that you pre-install the PHP 7.2 packages from the Remi repos. For instructions, please see `remi-php72 repository activation` in the document referenced above.

NOTE: Kaltura CE was ported to PHP 7.4 recently but it is not as well tested. You may elect to use that version instead, in which case, invoke:
```
# dnf module install php:remi-7.4
```

**Please test on a non-production instance first. We're happy to receive bug reports should you encounter issues.**

#### Enabling the PowerTools repos ####
For CentOS/RHEL 8, it is also necessary to enable the PowerTools repos:
```
# dnf config-manager --set-enabled PowerTools
```

#### Enabling the RPM Fusion repos ####
For CentOS/RHEL 8, it is also necessary to enable the Fusion repos:
```
# rpm -ihv https://download1.rpmfusion.org/free/el/rpmfusion-free-release-8.noarch.rpm
```

#### MySQL Install and Configuration
Kaltura CE does not currently support MySQL 5.6 and above. Please be sure to deploy MySQL 5.5.
If your distro's repos do not provide a suitable version (the CentOS/RHEL 8 repos have a higher version), we recommend the Percona project. See:
https://github.com/percona/percona-server/tree/5.5
And, in particular:
https://github.com/percona/percona-server/blob/5.5/build-ps/build-rpm.sh



RHEL/CentOS 6 setup:
```bash
# yum install mysql-server
# service mysqld start
# mysql_secure_installation
# chkconfig mysqld on
```

RHEL/CentOS 7 setup:
```bash
# yum install mariadb-server
# service mariadb start
# mysql_secure_installation
# chkconfig mariadb on
```

**Make sure to answer YES for all steps in the `mysql_secure_install` install, and follow through all the mysql install questions before continuing further.
Failing to properly run `mysql_secure_install` will cause the kaltura mysql user to run without proper permissions to access your mysql DB, and require you to start over again.

#### Mail Server (MTA) Install and Configuration
If your machine doesn't have postfix email configured before the Kaltura install, you will not receive emails from the install system nor publisher account activation mails.
If postfix runs without further configuration starting it is sufficient to make Kaltura work.
```bash
# service postfix restart
```

If you are using Amazon Web Services (AWS) please note that by default EC2 machines are blocked from sending email via port 25. For more information see [this thread on AWS forums](https://forums.aws.amazon.com/message.jspa?messageID=317525#317525).

##### Note regarding desktop installations

When installing on a "desktop" environment there may be package conflicts with media encoding/decoding plugins.

In Redhat 6.5 you should run the following to remove the conflicting packages:
`# rpm -e gstreamer-plugins-bad-free totem totem-nautilus`


## Non-SSL Step-by-step Installation
Before you can deploy your Kaltura CE Server, you need to perform some preliminary actions such as adding the Kaltura RPM repos, setting SELinux to persmissive mode and deploying MySQL. Please see [pre-install steps](install-kaltura-redhat-based.md#pre-install-steps). 

Install the basic Kaltura Packages:
```bash
# yum clean all
# yum install kaltura-server
```

Configure MySQL with the required Kaltura Settings
```bash
# /opt/kaltura/bin/kaltura-mysql-settings.sh
```

Start required service and configure them to run at boot:
```bash
# service memcached restart
# service ntpd restart
# chkconfig memcached on
# chkconfig ntpd on
```

### Start of Kaltura Configuration
```bash
# /opt/kaltura/bin/kaltura-config-all.sh
```

The below is a sample question answer format, replace the input marked by <> with your own details:

```
[Email\NO]: "<your email address>"
CDN hostname [kalrpm.lcl]: "<your hostname>"
Apache virtual hostname [kalrpm.lcl]: "<your hostname>"
Which port will this Vhost listen on [80]?:

DB hostname [127.0.0.1]: "<127.0.0.1>"
DB port [3306]: "<3306>"
MySQL super user [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "<root>"
MySQL super user passwd [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "<your root password>"
Analytics DB hostname [127.0.0.1]: "<127.0.0.1>"
Analytics DB port [3306]: "<3306>"
Sphinx hostname [127.0.0.1]: "<127.0.0.1>"

Secondary Sphinx hostname: [leave empty if none] "<empty>"

VOD packager hostname [kalrpm.lcl]: "<kaltura-nginx-hostname>"

VOD packager port to listen on [88]: 

Service URL [http://kalrpm.lcl:80]: "<http://apache-hostname:80>"

Kaltura Admin user (email address): "<your email address>"
Admin user login password (must be minimum 8 chars and include at least one of each: upper-case, lower-case, number and a special character): "<your kaltura admin password>"
Confirm passwd: "<your kaltura admin password>"

Your time zone [see http://php.net/date.timezone], or press enter for [Europe/Amsterdam]: "<your timezone>"
How would you like to name your system (this name will show as the From field in emails sent by the system) [Kaltura Video Platform]? "<your preferred system name>"
Your website Contact Us URL [http://corp.kaltura.com/company/contact-us]: "<your contact URL>"
'Contact us' phone number [+1 800 871 5224]? "<your phone number>"

Is your Apache working with SSL?[Y/n] "<n>"
It is recommended that you do work using HTTPs. Would you like to continue anyway?[N/y] "<y>"
Which port will this Vhost listen on? [80] "<80>"
Please select one of the following options [0]: "<0>"
```

Your install will now automatically perform all install tasks.



**Your Kaltura installation is now complete.**

## Apache SSL Step-by-step Installation
Before you can deploy your Kaltura CE Server, you need to perform some preliminary actions such as adding the Kaltura RPM repos, setting SELinux to permissive mode and deploying MySQL. Please see [pre-install steps](install-kaltura-redhat-based.md#pre-install-steps)  

Note: prior to installing Kaltura, while not a must, we recommend you update the installed packages to latest by running:
```bash
# yum update
```

Install the basic Kaltura Packages:
```bash
# yum clean all
# yum update "*kaltura*" 
# yum install kaltura-server
```

Configure MySQL with the required Kaltura Settings
```bash
# /opt/kaltura/bin/kaltura-mysql-settings.sh
```

Start required service and configure them to run at boot:
```bash
# service memcached restart
# service ntpd restart
# chkconfig memcached on
# chkconfig ntpd on
```

### Start of Kaltura Configuration
```bash
# /opt/kaltura/bin/kaltura-config-all.sh
```

The below is a sample question answer format, replace the input marked by <> with your own details:

```
[Email\NO]: "<your email address>"
CDN hostname [kalrpm.lcl]: "<your hostname>"
Apache virtual hostname [kalrpm.lcl]: "<your hostname>"
Which port will this Vhost listen on [80]?: "<443>"

DB hostname [127.0.0.1]: "<127.0.0.1>"
DB port [3306]: "<3306>"
MySQL super user [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "<root>"
MySQL super user passwd [this is only for setting the kaltura user passwd and WILL NOT be used with the application]: "<your root password>"
Analytics DB hostname [127.0.0.1]: "<127.0.0.1>"
Analytics DB port [3306]: "<3306>"
Sphinx hostname [127.0.0.1]: "<127.0.0.1>"

Secondary Sphinx hostname: [leave empty if none] "<empty>"

VOD packager hostname [kalrpm.lcl]: "<kaltura-nginx-hostname>"

VOD packager port to listen on [88]: 

Service URL [http://kalrpm.lcl:443]: "<http://your-hostname:443>"

Kaltura Admin user (email address): "<your email address>"
Admin user login password (must be minimum 8 chars and include at least one of each: upper-case, lower-case, number and a special character): "<your kaltura admin password>"
Confirm passwd: "<your kaltura admin password>"

Your time zone [see http://php.net/date.timezone], or press enter for [Europe/Amsterdam]: "<your timezone>"
How would you like to name your system (this name will show as the From field in emails sent by the system) [Kaltura Video Platform]? "<your preferred system name>"
Your website Contact Us URL [http://corp.kaltura.com/company/contact-us]: "<your contact URL>"
'Contact us' phone number [+1 800 871 5224]? "<your phone number>"

Is your Apache working with SSL?[Y/n]: "<Y>"
Please input path to your SSL certificate: "</path/to/my/ssl/certificate>"
Please input path to your SSL key: "</path/to/my/ssl/key>"
Please input path to your SSL chain file or leave empty in case you have none: "</path/to/my/ssl/chainfile>"
Which port will this Vhost listen on? [443] "<443>"
Please select one of the following options [0]: "<0>"
```

### Nginx SSL configuration
Please see [nginx-ssl-config.md](nginx-ssl-config.md)

### Live Streaming with Nginx and the RTMP module
Kaltura CE includes the kaltura-nginx package, which is compiled with the [Nginx RTMP module](https://github.com/arut/nginx-rtmp-module).

Please see documentation here [nginx-rtmp-live-streaming.md](nginx-rtmp-live-streaming.md)

A longer post about it can be found at https://blog.kaltura.com/free-and-open-live-video-streaming


### Securing Monit
To use the [monit](http://mmonit.com/monit/) Monitoring tab in admin console, you will need to also configure the SSL certificate for monit, see [Generate PEM Instructions](http://www.digicert.com/ssl-support/pem-ssl-creation.htm)

Edit: `/opt/kaltura/app/configurations/monit/monit.conf` and add:
```
SSL ENABLE
PEMFILE /path/to/your/certificate.pem
```

The Monit HTTP daemon binds to loopback only by default [127.0.0.1]. If you wish to access the I/F from the Monitoring tab in admin console, edit /opt/kaltura/app/configurations/monit/monit.conf and change the following block to suit your needs:
```
set httpd port 2812
ADDRESS 127.0.0.1
allow root:@MONIT_PASSWD@
```

For Monit's conf documentation, please refer to https://mmonit.com/monit/documentation/monit.html, specifically, look under the "MONIT HTTPD" section.

Once done, run: ```/etc/init.d/kaltura-monit restart```

**Your Kaltura installation is now complete.**

## Unattended Installation
All the post install scripts optionally accept an answer file as the first argument
In order to preform an unattended [silent] install, simply edit the [template](kaltura.template.ans) and pass it along to kaltura-config-all.sh.

## Upgrade Kaltura
*This will only work if the initial install was using this packages based install, it will not work for old Kaltura deployments using the PHP installers*
```bash
# rpm -Uhv http://installrepo.kaltura.org/releases/kaltura-release.noarch.rpm
# yum clean all
# yum update "*kaltura*"
```
Once the upgrade completes, run:
```bash
# /opt/kaltura/bin/kaltura-config-all.sh
```


In the event you would like to see what changes the package includes before deciding whether or not you wish to upgrade, run:
```bash
# yum install yum-plugin-changelog
# yum changelog all kaltura-package-name-here
```

## Remove Kaltura
Use this in cases where you want to clear the database and start from fresh.
```bash
# /opt/kaltura/bin/kaltura-drop-db.sh
# yum remove "*kaltura*"
# rm -rf /opt/kaltura
```

## Troubleshooting
Once the configuration phase is done, you may wish to run the sanity tests, for that, run:
```base
# /opt/kaltura/bin/kaltura-sanity.sh
```

If you experience unknown, unwanted or erroneous behaviour, the logs are a good place to start, to get a quick view into errors and warning run:
```bash
kaltlog
```

If this does not give enough information, increase logging verbosity:
```bash
# sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*7@writers.\1.filters.priority.priority=4@g' /opt/kaltura/app/configurations/logger.ini
```

To revert this logging verbosity run:
```bash
# sed -i 's@^writers.\(.*\).filters.priority.priority\s*=\s*4@writers.\1.filters.priority.priority=7@g' /opt/kaltura/app/configurations/logger.ini
```

Or output all logged information to a file for analysis:
```bash
allkaltlog > /path/to/mylogfile.log
```

For posting questions, please go to:
(http://forum.kaltura.org)

## Additional Information
* Please review the [frequently answered questions](kaltura-packages-faq.md) document for general help before posting to the forums or issue queue.
* This guide describes the installation and upgrade of an all-in-one machine where all the Kaltura components are installed on the same server. For cluster deployments, please refer to [cluster deployment document](http://bit.ly/kipp-cluster-yum), or [Deploying Kaltura using Opscode Chef](rpm-chef-cluster-deployment.md).
* To learn about monitoring, please refer to [configuring platform monitors](http://bit.ly/kipp-monitoring).
* You can find VMWare images at - https://www.osboxes.org/vmware-images
* Two working solutions to the AWS EC2 email limitations are:
  * Using SendGrid as your mail service ([setting up ec2 with Sendgrid and postfix](http://www.zoharbabin.com/configure-ssmtp-or-postfix-to-send-email-via-sendgrid-on-centos-6-3-ec2)).
  * Using [Amazon's Simple Email Service](http://aws.amazon.com/ses/).
* [Kaltura Inc.](http://corp.kaltura.com) also provides commercial solutions and services including pro-active platform monitoring, applications, SLA, 24/7 support and professional services. If you're looking for a commercially supported video platform  with integrations to commercial encoders, streaming servers, eCDN, DRM and more - Start a [Free Trial of the Kaltura.com Hosted Platform](http://corp.kaltura.com/free-trial) or learn more about [Kaltura' Commercial OnPrem Edition™](http://corp.kaltura.com/Deployment-Options/Kaltura-On-Prem-Edition). For existing RPM based users, Kaltura offers commercial upgrade options.
