# SPEC file for libmtp, primary target is the Fedora
# RPM repository.

Name:           libmtp
Version:        1.0.1
Release:        2%{?dist}
Summary:        A software library for MTP media players
URL:            http://libmtp.sourceforge.net/

Group:          System Environment/Libraries
Source0:        http://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
License:        LGPLv2+
Requires:       udev
Requires:	hal
BuildRequires:  libusb-devel
BuildRequires:  doxygen

%description
This package provides a software library for communicating with MTP
(Media Transfer Protocol) media players, typically audio players, video
players etc.

%package examples
Summary:        Example programs for libmtp
Group:          Applications/Multimedia
Requires:       %{name} = %{version}-%{release}

%description examples
This package provides example programs for communicating with MTP
devices.

%package devel
Summary:        Development files for libmtp
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig
Requires:       libusb-devel

%description devel
This package provides development files for the libmtp
library for MTP media players.

%prep
%setup -q

%build
%configure --disable-static --program-prefix=mtp-
make %{?_smp_mflags}
# Remove permissions from udev rules, but register for ACL management
examples/hotplug -a"SYMLINK+=\"libmtp-%k\", ENV{ACL_MANAGE}=\"1\"" > libmtp.rules

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
# Remove libtool archive remnant
rm -f $RPM_BUILD_ROOT%{_libdir}/libmtp.la
# Replace links with relative links
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-delfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-getfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-newfolder
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-sendfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-sendtr
pushd $RPM_BUILD_ROOT%{_bindir}
ln -sf mtp-connect mtp-delfile
ln -sf mtp-connect mtp-getfile
ln -sf mtp-connect mtp-newfolder
ln -sf mtp-connect mtp-sendfile
ln -sf mtp-connect mtp-sendtr
popd
# Install udev rules file.
mkdir -p $RPM_BUILD_ROOT/lib/udev/rules.d
install -p -m 644 libmtp.rules $RPM_BUILD_ROOT/lib/udev/rules.d/60-libmtp.rules
mkdir -p $RPM_BUILD_ROOT%{_datadir}/hal/fdi/information/10freedesktop
install -p -m 644 libmtp.fdi $RPM_BUILD_ROOT%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi
# Copy documentation to a good place
install -p -m 644 AUTHORS ChangeLog COPYING INSTALL README TODO \
$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
# Touch generated files to make them always have the same time stamp.
touch -r configure.ac \
      $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html/* \
      $RPM_BUILD_ROOT%{_includedir}/*.h \
      $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*.pc \
      $RPM_BUILD_ROOT%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi
# Remove the Doxygen HTML documentation, this get different
# each time it is generated and thus creates multiarch conflicts.
# I don't want to pre-generate it but will instead wait for upstream
# to find a suitable solution that will always bring the same files,
# or that Doxygen is fixed not to do this.
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html


%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root,root,-)
%{_libdir}/*.so.*
/lib/udev/rules.d/*
%{_datadir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi

%files examples
%defattr(-,root,root,-)
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/*
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc


%changelog
* Tue Dec 1 2009 Linus Walleij <triad@df.lth.se> 1.0.1-2
- Two patches from Dan Nicholson to fix up the udev rules a bit.

* Sat Sep 12 2009 Linus Walleij <triad@df.lth.se> 1.0.1-1
- New upstream release. No interface changes!

* Tue Aug 4 2009 Linus Walleij <triad@df.lth.se> 1.0.0-1
- New upstream release. Dependent packages need to be rebuilt against this.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Linus Walleij <triad@df.lth.se> 0.3.7-1
- New upstream bugfix release.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Linus Walleij <triad@df.lth.se> 0.3.6-1
- New upstream bugfix release.

* Sun Dec 21 2008 Linus Walleij <triad@df.lth.se> 0.3.5-1
- New upstream bugfix release.
- Nuke documentation again. Multilib no like.

* Fri Nov 7 2008 Linus Walleij <triad@df.lth.se> 0.3.4-1
- New upstream bugfix release.
- Bastiens patch is upstreamed, dropping that patch.

* Sat Oct 25 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.3-4
- Update device list from CVS and fix the build

* Sat Oct 25 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.3-3
- Add support for more Nokia phones from their WMP10 drivers

* Fri Oct 24 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.3-2
- Add support for the Nokia N82

* Fri Sep 26 2008 Linus Walleij <triad@df.lth.se> 0.3.3-1
- New upstream bugfix release.

* Sat Sep 20 2008 Linus Walleij <triad@df.lth.se> 0.3.2-1
- New upstream version. (API and ABI compatible.) Fixes
  bugs on Creative devices.

* Tue Aug 26 2008 Linus Walleij <triad@df.lth.se> 0.3.1-1
- New upstream version. (API and ABI compatible.)

* Thu Aug 7 2008 Linus Walleij <triad@df.lth.se> 0.3.0-1
- Upgrade to 0.3.0. This has to happen some way, perhaps the
  painful way: I upgrade to gnomad2 2.9.2 that use 0.3.0 and
  then I write patches to Rhythmbox and Amarok to use 0.3.0
  and also send these upstream.

* Fri Jul 11 2008 Linus Walleij <triad@df.lth.se> 0.2.6.1-3
- Loose PAM console permissions, also assume that we can ship
  documentation again since Doxygen has been updated. Fedora
  HALd rules for the portable_audio_player capability in
  20-acl-management.fdi will change permissions on the device
  node for each plugged-in device.

* Fri May 23 2008 Adam Jackson <ajax@redhat.com> 0.2.6.1-2
- libmtp-0.2.6.1-simpler-rules.patch: Simplify udev rules for faster bootup.

* Sat Mar 8 2008 Linus Walleij <triad@df.lth.se> 0.2.6.1-1
- New upstream bugfix release.

* Sun Mar 2 2008 Linus Walleij <triad@df.lth.se> 0.2.6-1
- New upstream release.

* Sat Feb 9 2008 Linus Walleij <triad@df.lth.se> 0.2.5-2
- Rebuild for GCC 4.3.

* Wed Jan 9 2008 Linus Walleij <triad@df.lth.se> 0.2.5-1
- New upstream release.

* Thu Nov 22 2007 Linus Walleij <triad@df.lth.se> 0.2.4-1
- New upstream release.

* Thu Oct 25 2007 Linus Walleij <triad@df.lth.se> 0.2.3-1
- New upstream release.
- New soname libmtp.so.7 so all apps using libmtp have to
  be recompiled, have fun.
- If it works out we'll try to reserve a spot to backport
  this fixed version to F8 and F7 in a controlled manner.

* Wed Oct 24 2007 Linus Walleij <triad@df.lth.se> 0.2.2-2
- Flat out KILL the Doxygen HTML docs to resolve multiarch conflicts.
  Either upstream (that's me!) needs to work around the HTML files being 
  different each time OR Doxygen must stop generating anchors that
  hash the system time, creating different files with each generation.
  Pre-generating the docs is deemed silly. (Someone will disagree.)

* Fri Aug 17 2007 Linus Walleij <triad@df.lth.se> 0.2.2-1
- New upstream release.

* Fri Aug 17 2007 Linus Walleij <triad@df.lth.se> 0.2.1-2
- License field update from LGPL to LGPLv2+

* Tue Aug 7 2007 Linus Walleij <triad@df.lth.se> 0.2.1-1
- Upstream bugfix release.

* Sat Aug 4 2007 Linus Walleij <triad@df.lth.se> 0.2.0-1
- New upstream release.
- Fixes (hopefully) the issues found by Harald.
- Dependent apps will need to recompile and patch some minor code.

* Mon Jul 30 2007 Harald Hoyer <harald@redhat.com> - 0.1.5-2
- changed udev rules for new kernel and udev versions

* Mon Mar 26 2007 Linus Walleij <triad@df.lth.se> 0.1.5-1
- New upstream release.
- Candidate for FC5, FC6 backport.
- Hopefully API/ABI compatible, testing in devel tree.

* Wed Mar 7 2007 Linus Walleij <triad@df.lth.se> 0.1.4-1
- New upstream release.
- Candidate for FC5, FC6 backport.
- Hopefully API/ABI compatible, testing in devel tree.

* Wed Jan 17 2007 Linus Walleij <triad@df.lth.se> 0.1.3-1
- New upstream release.
- Candidate for FC5, FC6 backport.

* Thu Dec 7 2006 Linus Walleij <triad@df.lth.se> 0.1.0-1
- New upstream release.
- Start providing HAL rules.

* Fri Oct 20 2006 Linus Walleij <triad@df.lth.se> 0.0.21-1
- New upstream release.

* Tue Sep 26 2006 Linus Walleij <triad@df.lth.se> 0.0.20-1
- New upstream release.
- Updated after review by Parag AN, Kevin Fenzi and Ralf Corsepius.
- Fixed pkgconfig bug upstream after being detected by Ralf...

* Sun Aug 27 2006 Linus Walleij <triad@df.lth.se> 0.0.15-1
- New upstream release.

* Wed Aug 23 2006 Linus Walleij <triad@df.lth.se> 0.0.13-1
- First RPM'ed
