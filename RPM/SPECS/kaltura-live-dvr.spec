%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)
%define kaltura_root_prefix	/opt/kaltura
%define livedvr_prefix %{kaltura_root_prefix}/livedvr
%define kaltura_user	kaltura
%define kaltura_group	kaltura
%define ffmpeg_version 3.0 
%define nginx_conf_dir /etc/nginx/conf.d/

Summary: Kaltura Open Source Video Platform - Live DVR
Name: kaltura-livedvr
Version: 2.3.10
Release: 1
License: AGPLv3+
Group: Server/Platform 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-monit kaltura-base redhat-lsb-core nodejs >= 7.0.0 kaltura-nginx nodejs-chunked-stream nodejs-commander  nodejs-log4js nodejs-glob nodejs-mkdirp nodejs-q nodejs-q-io nodejs-touch nodejs-underscore nodejs-nconf nodejs-request nodejs-forever nodejs-ini nodejs-string-width nodejs-strip-ansi nodejs-minimatch nodejs-inherits nodejs-wrappy nodejs-once nodejs-socket.io-client 
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
BuildRequires: unzip
Source0: %{name}-%{version}.tar.gz
Source1: %{name}.logrotate
Source2: %{name}.recorder.init
Source3: %{name}.controller.init


%description
Kaltura is the world's first Open Source Online Video Platform, transforming the way people work, 
learn, and entertain using online video. 
The Kaltura platform empowers media applications with advanced video management, publishing, 
and monetization tools that increase their reach and monetization and simplify their video operations. 
Kaltura improves productivity and interaction among millions of employees by providing enterprises 
powerful online video tools for boosting internal knowledge sharing, training, and collaboration, 
and for more effective marketing. Kaltura offers next generation learning for millions of students and 
teachers by providing educational institutions disruptive online video solutions for improved teaching,
learning, and increased engagement across campuses and beyond. 
For more information visit: http://corp.kaltura.com, http://www.kaltura.org and http://www.html5video.org.

This package sets up a Kaltura LiveDvr.

#%package debug
#Summary: debug binaries for livedvr
#Requires: kaltura-livedvr
#%description debug
#Not stripped version of ts_to_mp4_convertor

%clean
rm -rf %{buildroot}

%prep
%setup -qn liveDVR-%{version}

%build
NODE_PATH=~/node_modules
export LDFLAGS="-g -lX11"
mkdir -p %{buildroot}/%{name}-%{version}/tmp/build 
sed -i 's@configure @configure --disable-vdpau @g' ./build_scripts/build_ffmpeg4.sh
./build_scripts/build_ffmpeg4.sh %{buildroot}/%{name}-%{version}/tmp/build
./build_scripts/build_ffmpeg.sh %{buildroot}/%{name}-%{version}/tmp/build %{ffmpeg_version}
./build_scripts/build_ts2mp4_convertor.sh ./liveRecorder %{buildroot}/%{name}-%{version}/tmp/build
npm install nan
./build_scripts/build_addon.sh `pwd` %{buildroot}/%{name}-%{version}/tmp/build/ffmpeg-%{ffmpeg_version} Release


%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d 
mkdir -p $RPM_BUILD_ROOT%{livedvr_prefix}/bin $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/bin $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/Config $RPM_BUILD_ROOT%{livedvr_prefix}/log $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/recordings/newSession $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/recordings/append $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/error $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/incoming $RPM_BUILD_ROOT/%{kaltura_root_prefix}/web/content/kLive/liveRecorder/recordings $RPM_BUILD_ROOT%{nginx_conf_dir} $RPM_BUILD_ROOT%{kaltura_root_prefix}/log/livedvr
strip %{_builddir}/liveDVR-%{version}/liveRecorder/bin/ts_to_mp4_convertor
strip %{_builddir}/liveDVR-%{version}/node_addons/FormatConverter/build/Release/FormatConverter.so
cp %{_builddir}/liveDVR-%{version}/liveRecorder/bin/ts_to_mp4_convertor $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/bin/ts_to_mp4_convertor
cp %{_builddir}/liveDVR-%{version}/node_addons/FormatConverter/build/Release/FormatConverter.so $RPM_BUILD_ROOT%{livedvr_prefix}/bin/FormatConverter.node
cp -r %{_builddir}/liveDVR-%{version}/lib $RPM_BUILD_ROOT%{livedvr_prefix}
cp -r %{_builddir}/liveDVR-%{version}/common $RPM_BUILD_ROOT%{livedvr_prefix}
cp -r %{_builddir}/liveDVR-%{version}/liveRecorder/* $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/

# get rid of shit we do not want to package:
for RUBBISH in  serviceWrappers ts_to_mp4_convertor install.sh installPython.sh ;do
	rm -rf $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/$RUBBISH
done

cp %{_builddir}/liveDVR-%{version}/liveRecorder/Config/configMapping.ini.template $RPM_BUILD_ROOT%{livedvr_prefix}/liveRecorder/Config
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/kaltura-live-recorder 
cp %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/kaltura-live-controller
sed 's#@CONTENT_DIR@#%{kaltura_root_prefix}/web#g' %{_builddir}/liveDVR-%{version}/packager/config/nginx.conf.live.bootstrap.template > $RPM_BUILD_ROOT%{nginx_conf_dir}/nginx.conf.live.bootstrap
cp %{_builddir}/liveDVR-%{version}/packager/config/nginx.conf.live.conf.template $RPM_BUILD_ROOT%{nginx_conf_dir}/live.conf
cp %{_builddir}/liveDVR-%{version}/packager/config/nginx.conf.live.protocols.template $RPM_BUILD_ROOT%{nginx_conf_dir}/

%{__mkdir} -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
%{__install} -m 644 -p %{SOURCE1} \
   $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

%pre
# maybe one day we will support SELinux in which case this can be ommitted.
if which getenforce >> /dev/null 2>&1; then
	
	if [ `getenforce` = 'Enforcing' ];then
		echo "You have SELinux enabled, please change to permissive mode with:
# setenforce permissive
and then edit /etc/selinux/config to make the change permanent."
		exit 1;
	fi
fi
# create user/group, and update permissions
getent group %{kaltura_group} >/dev/null || groupadd -r %{kaltura_group} -g7373 2>/dev/null
getent passwd %{kaltura_user} >/dev/null || useradd -m -r -u7373 -d %{prefix} -s /bin/bash -c "Kaltura server" -g %{kaltura_group} %{kaltura_user} 2>/dev/null

usermod -g %{kaltura_group} %{kaltura_user} 2>/dev/null || true
%post
if [ "$1" = 1 ];then
	/sbin/chkconfig --add kaltura-live-controller
	/sbin/chkconfig kaltura-live-controller on
	/sbin/chkconfig --add kaltura-live-recorder
	/sbin/chkconfig kaltura-live-recorder on
fi
%preun
if [ "$1" = 0 ] ; then
	/sbin/chkconfig --del kaltura-live-controller
	service kaltura-live-controller stop
	/sbin/chkconfig --del kaltura-live-recorder
	service kaltura-live-recorder stop
fi
%postun

%files
%defattr(-, %{kaltura_user}, %{kaltura_group} , 0775)
%dir %{livedvr_prefix}
%{livedvr_prefix}
%{kaltura_root_prefix}/web/content/kLive/liveRecorder/*
%{kaltura_root_prefix}/log/livedvr
%config %{livedvr_prefix}/common/config/*
%config %{livedvr_prefix}/liveRecorder/Config/*
%config %{nginx_conf_dir}/*
%{_sysconfdir}/init.d/kaltura-live-controller
%{_sysconfdir}/init.d/kaltura-live-recorder
%config %{_sysconfdir}/logrotate.d/%{name}

#%files debug

%changelog
* Tue Nov 24 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 2.3.10-1
- Don't remove redirect when reset recording by default
- https://kaltura.atlassian.net/browse/SUP-22697
- https://kaltura.atlassian.net/browse/PSVAMB-14598
- https://kaltura.atlassian.net/browse/PSVAMB-14598 
- https://kaltura.atlassian.net/browse/SUP-22058
- SUP-22058: reset recording if per session is used (#625)
- PLAT-10319

* Wed Nov 28 2018 jess.portnoy@kaltura.com <Jess Portnoy> - 2.0.4-2
- Added dep: nodejs-socket.io-client

* Thu Nov 9 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 1.22.1-1
- Fixed init scripts
- Added logrotate config

* Thu Oct 26 2017 Jess Portnoy <jess.portnoy@kaltura.com> - 1.20.2-1
- PLAT-8051: Recording, jobs in processing queue of UploadTask, are not handled (https://github.com/kaltura/liveDVR/pull/534)
- Replace number with explicit kalturaLiveStatus

* Thu Mar 31 2016 Jess Portnoy <jess.portnoy@kaltura.com> - 1.9.2-1
- First package.

