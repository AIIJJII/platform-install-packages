%define prefix /opt/kaltura
%define html5lib3_base %{prefix}/html5/html5lib/playkitSources/kaltura-ovp-player

Summary: Kaltura Open Source Video Platform 
Name: kaltura-html5lib3
Version: 1.0.3
Release: 1
License: AGPLv3+
Group: Server/Platform 
Source0: %{name}-%{version}.tar.gz 
Source1: create_playkit_uiconf.php

URL: https://github.com/kaltura/kaltura-player-js 
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: kaltura-base, httpd

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

This package installs the Kaltura HTML5 v3 player library.

%prep
%setup -q -n %{version} 

%install
mkdir -p $RPM_BUILD_ROOT%{html5lib3_base}/%{version}
cp -r * $RPM_BUILD_ROOT%{html5lib3_base}/%{version} 
cp %{SOURCE1} $RPM_BUILD_ROOT%{html5lib3_base}/

%clean
rm -rf %{buildroot}

%post

%postun

%files
%defattr(-, root, root, 0755)
%{html5lib3_base}

%changelog
* Wed Oct 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 1.0.3-1
- FEC-10161: add kava analytics url from server response (#355) (e4ce3f1)
- FEC-10275: Bumper incorrectly recognised as ad (#352) (716d01a)
- FEC-10417: playlist by sources stuck after press Play button when set IMA or bumper plugins (#349) (b2256f3)
- FEC-10455: incorrect order in reset and destroy process (#353) (fc9bf96)
- FEC-10468: PLAYBACK_START not fired on autoplay (#356) (78c3ed5)
- FEC-10076: add support for dynamic injection (#351) (b9e9a31)
- FEC-10296: upgrade hls.js to 0.14.9 (#348) (2d0ec6e)
- FEC-10435: upgrade shaka for fixing live issue and optimizations for smartTV (#354) (90ce625)
- FEC-10347: expose kaltura player as a global variable instead of UMD (#350) (b6253ff)
- FEC-10347: kaltura-player is not UMD anymore
- DRM doesn't play on edge chromium (#364) (cc4cce4)

* Sun Aug 9 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.56.0-1
- New RAPT plugin (0.4.2)
- Downgrade shaka from 3.0.x (#346) (f126796)
- Old browser(IE11) get mehtod in proxy doesn't work (#345) (4d3f69c)
- FEC-10356: 4K DASH HEVC + LIVE doesn't play correctly on LG (#342) (111cdac)
- FEC-10057: move the plugin manager to kaltura player (#332) (66b2f3d)
- FEC-10290: upgrade NPM packages (#335) (07fa73b)
- FEC-10291: migrate analytics plugins injection from kaltura player to server (#337) (1caf168)

* Fri Jun 26 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.54.0-2
- New RAPT plugin (0.4.0)

* Wed Jun 10 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.54.0-1
- FEC-10053: Subtitle issue for Player with TTML in MP4 container (#316) (c053ac2)
- FEC-10155: text track language is incorrect on cast disconnecting (#318) (75690a3), closes #188
- FEC-9631: add support for out of band text tracks on cast sdk (#319) (16562b6)

* Thu May 21 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.53.7-1
- FEC-9109: add DRM Load time metric (#305) (e0b267e)
- Remove French (fr) translation file (5529611)
- FEC-9734: auto play doesn't works, if "playsinline"=false on all platforms (#307) 
- New RAPT plugin (0.2.4)

* Mon Mar 16 2020 jess.portnoy@kaltura.com <Jess Portnoy> - 0.51.3-2
- New RAPT/PATH ver - 0.1.12

* Fri Dec 27 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.51.1-1
- FEC-9471, FEC-8436, FEC-8443: slider progress bar exceeds 100% (#287) (a617eae)
- FEC-9175: cast content coming from external sources (#288) (43a46b2)

* Mon Nov 25 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.49.0-1
- config keySystem isn't boolean (#283) (4280dc5)
- New hasUserInteracted api (#284) (6855309)
- FEC-9307: live issue on LG SDK2 with hls.js (#273) (1ca1b5d)
- FEC-9379: Edge chromium should use playready when exist (#274) (6b87274)
- FEC-9326: report productVersion (#275) (304f9ca)
- FEC-9389: media playing unmuted after unmute fallback (#272) (dafa0d6)

* Mon Sep 16 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.46.0-1
- playkit-js 0.53.0
- playkit-js-dash 1.15.0
- IMA plugin - 0.17.2

* Mon Aug 5 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.45.5-1
- Added the bumper and Youtube plugins

* Fri Apr 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.37.3-2
- Added RAPT plugin

* Tue Feb 12 2019 jess.portnoy@kaltura.com <Jess Portnoy> - 0.37.3-1
- First release
