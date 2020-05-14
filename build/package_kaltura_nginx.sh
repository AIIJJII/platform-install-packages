#!/bin/bash -e 
#===============================================================================
#          FILE: package_kaltura_core.sh
#         USAGE: ./package_kaltura_core.sh 
#   DESCRIPTION: 
#       OPTIONS: ---
# 	LICENSE: AGPLv3+
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Jess Portnoy (), <jess.portnoy@kaltura.com>
#  ORGANIZATION: Kaltura, inc.
#       CREATED: 01/10/14 08:46:43 EST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
SOURCES_RC=`dirname $0`/sources.rc
if [ ! -r $SOURCES_RC ];then
	echo "Could not find $SOURCES_RC"
	exit 1
fi
. $SOURCES_RC 
if [ ! -x "`which wget 2>/dev/null`" ];then
	echo "Need to install wget."
	exit 2
fi
wget $KALTURA_NGINX_SECURE_TOKEN_URI -O$RPM_SOURCES_DIR/nginx-secure-token-module-$KALTURA_NGINX_SECURE_TOKEN_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-secure-token-module-$KALTURA_NGINX_SECURE_TOKEN_VERSION.zip"
wget $KALTURA_NGINX_AKAMAI_TOKEN_VALIDATE_URI -O$RPM_SOURCES_DIR/nginx-akamai-token-validate-module-$KALTURA_NGINX_AKAMAI_TOKEN_VALIDATE_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-akamai-token-validate-module-$KALTURA_NGINX_AKAMAI_TOKEN_VALIDATE_VERSION.zip"
wget $KALTURA_NGINX_KAFKA_LOG_URI -O$RPM_SOURCES_DIR/nginx-kafka-log-module-$KALTURA_NGINX_KAFKA_LOG_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-kafka-log-module-$KALTURA_NGINX_KAFKA_LOG_VERSION.zip"
wget $KALTURA_NGINX_JSON_VAR_URI -O$RPM_SOURCES_DIR/nginx-json-var-module-$KALTURA_NGINX_JSON_VAR_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-json-var-module-$KALTURA_NGINX_JSON_VAR_VERSION.zip"
wget $KALTURA_NGINX_STRFTIME_URI -O$RPM_SOURCES_DIR/nginx-strftime-module-$KALTURA_NGINX_STRFTIME_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-strftime-module-$KALTURA_NGINX_STRFTIME_VERSION.zip"
wget $KALTURA_NGINX_VOD_URI -O$RPM_SOURCES_DIR/nginx-vod-module-$KALTURA_NGINX_VOD_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-vod-module-$KALTURA_NGINX_VOD_VERSION.zip"
wget $NGINX_VTS_URI -O$RPM_SOURCES_DIR/nginx-module-vts-$NGINX_VTS_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-module-vts-$NGINX_VTS_VERSION.zip"
wget $NGINX_RTMP_URI -O$RPM_SOURCES_DIR/nginx-module-rtmp-$NGINX_RTMP_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/nginx-module-rtmp-$NGINX_RTMP_VERSION.zip"
wget $NGINX_URI -O$RPM_SOURCES_DIR/kaltura-nginx-$NGINX_VERSION.tar.gz
echo "Packaged into $RPM_SOURCES_DIR/kaltura-nginx-$NGINX_VERSION.tar.gz"
wget $NGX_AWS_AUTH_URI -O$RPM_SOURCES_DIR/ngx_aws_auth-$NGX_AWS_AUTH_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/ngx_aws_auth-$NGX_AWS_AUTH_VERSION.zip"
wget $HEADERS_MORE_NGINX_URI -O$RPM_SOURCES_DIR/headers-more-nginx-module-$HEADERS_MORE_NGINX_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/headers-more-nginx-module-$HEADERS_MORE_NGINX_VERSION.zip"
wget $NGINX_SET_MISC_URI -O$RPM_SOURCES_DIR/set-misc-nginx-module-$NGINX_SET_MISC_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/set-misc-nginx-module-$NGINX_SET_MISC_VERSION.zip"
wget $NGINX_DEVEL_KIT_URI -O$RPM_SOURCES_DIR/devel-kit-nginx-module-$NGINX_DEVEL_KIT_VERSION.zip
echo "Packaged into $RPM_SOURCES_DIR/devel-kit-nginx-module-$NGINX_DEVEL_KIT_VERSION.zip"

if [ -x "`which rpmbuild 2>/dev/null`" ];then
	rpmbuild -ba $RPM_SPECS_DIR/kaltura-nginx.spec
fi
