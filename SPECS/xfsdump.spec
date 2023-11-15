Summary: Administrative utilities for the XFS filesystem
Name: xfsdump
Version: 3.1.8
Release: 6%{?dist}
# Licensing based on generic "GNU GENERAL PUBLIC LICENSE"
# in source, with no mention of version.
License: GPL+
Group: System Environment/Base
URL: http://oss.sgi.com/projects/xfs/
Source0: http://kernel.org/pub/linux/utils/fs/xfs/%{name}/%{name}-%{version}.tar.xz
Patch0: 0001-xfsdump-Revert-xfsdump-handle-bind-mount-targets.patch
Patch1: 0002-xfsdump-intercept-bind-mount-targets.patch
Patch2: 0003-for-next-xfsrestore-fix-rootdir-due-to-xfsdump-bulkstat-misus.patch
Patch3: 0004-v3.1.9-common-types.h-Wrap-define-UUID_STR_LEN-36-in-ifndef.patch
Patch4: 0005-v3.1.12-xfsrestore-fix-on-media-inventory-media-unpacking.patch
Patch5: 0006-v3.1.12-xfsrestore-fix-on-media-inventory-stream-unpacking.patch
Patch6: 0007-v3.1.12-xfsdump-fix-on-media-inventory-stream-packing.patch
Patch7: 0008-v3.1.12-xfsrestore-untangle-inventory-unpacking-logic.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool, gettext, gawk
BuildRequires: xfsprogs-devel, libuuid-devel, libattr-devel ncurses-devel
Requires: xfsprogs >= 2.6.30, attr >= 2.0.0

%description
The xfsdump package contains xfsdump, xfsrestore and a number of
other utilities for administering XFS filesystems.

xfsdump examines files in a filesystem, determines which need to be
backed up, and copies those files to a specified disk, tape or other
storage medium.	 It uses XFS-specific directives for optimizing the
dump of an XFS filesystem, and also knows how to backup XFS extended
attributes.  Backups created with xfsdump are "endian safe" and can
thus be transfered between Linux machines of different architectures
and also between IRIX machines.

xfsrestore performs the inverse function of xfsdump; it can restore a
full backup of a filesystem.  Subsequent incremental backups can then
be layered on top of the full backup.  Single files and directory
subtrees may be restored from full or partial backups.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
%configure

make V=1 %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DIST_ROOT=$RPM_BUILD_ROOT install
# remove non-versioned docs location
rm -rf $RPM_BUILD_ROOT/%{_datadir}/doc/xfsdump/

# Bit of a hack to move files from /sbin to /usr/sbin
(cd $RPM_BUILD_ROOT/%{_sbindir}; rm xfsdump xfsrestore)
(cd $RPM_BUILD_ROOT/%{_sbindir}; mv ../../sbin/xfsdump .)
(cd $RPM_BUILD_ROOT/%{_sbindir}; mv ../../sbin/xfsrestore .)

# Create inventory dir (otherwise created @ runtime)
mkdir -p $RPM_BUILD_ROOT/%{_sharedstatedir}/xfsdump/inventory

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc README doc/COPYING doc/CHANGES doc/README.xfsdump doc/xfsdump_ts.txt
%{_mandir}/man8/*
%{_sbindir}/*
%{_sharedstatedir}/xfsdump/inventory

%changelog
* Tue Jun 20 2023 Pavel Reichl <preichl@redhat.com> - 3.1.8-6
- xfsdump: restoring inventory prevents non-directory files being restored from tape
- related: bz#2166554

* Mon Jun 19 2023 Pavel Reichl <preichl@redhat.com> - 3.1.8-5
- xfsrestore: Files from the backup go to orphanage dir because of xfsdump issue
- related: bz#2055289

* Fri Feb 11 2022 Eric Sandeen <sandeen@redhat.com> 3.1.8-4
- Fix bind mount vs root inode problems (#2020494)

* Wed May 15 2019 Eric Sandeen <sandeen@redhat.com> 3.1.8-3
- Bump revision for test infrastructure (#1681970)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 21 2017 Eric Sandeen <sandeen@redhat.com> 3.1.8-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Eric Sandeen <sandeen@redhat.com> 3.1.6-4
- Build with largefile support on 32-bit platforms

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Eric Sandeen <sandeen@redhat.com> 3.1.6-1
- New upstream release

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Eric Sandeen <sandeen@redhat.com> 3.1.4-1
- New upstream release

* Mon Jun 16 2014 Eric Sandeen <sandeen@redhat.com> 3.1.3-5
- Fix aarch64 build (#926800)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 20 2014 Eric Sandeen <sandeen@redhat.com> 3.1.3-3
- Add /var/lib/xfsdump/inventory to file list (was created runtime)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 08 2013 Eric Sandeen <sandeen@redhat.com> 3.1.3-1
- New upstream release

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Eric Sandeen <sandeen@redhat.com> 3.1.2-1
- New upstream release, with non-broken tarball

* Thu Dec 13 2012 Eric Sandeen <sandeen@redhat.com> 3.1.1-1
- New upstream release

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Eric Sandeen <sandeen@redhat.com> 3.1.0-2
- Move files out of /sbin to /usr/sbin

* Fri Mar 23 2012 Eric Sandeen <sandeen@redhat.com> 3.1.0-1
- New upstream release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Eric Sandeen <sandeen@redhat.com> 3.0.6-1
- New upstream release

* Thu Mar 31 2011 Eric Sandeen <sandeen@redhat.com> 3.0.5-1
- New upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 13 2010 Eric Sandeen <sandeen@redhat.com> 3.0.4-1
- New upstream release

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.0.1-3.1
- Rebuilt for RHEL 6

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-2
- Fix up build-requires after e2fsprogs splitup

* Tue May 05 2009 Eric Sandeen <sandeen@redhat.com> 3.0.1-1
- New upstream release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Eric Sandeen <sandeen@redhat.com> 3.0.0-1
- New upstream release

* Wed Nov 12 2008 Eric Sandeen <sandeen@redhat.com> 2.2.48-2
- Enable parallel builds

* Sun Feb 10 2008 Eric Sandeen <sandeen@redhat.com> - 2.2.48-1
- Update to xfsdump version 2.2.48
- First build with gcc-4.3

* Mon Sep 10 2007 Eric Sandeen <sandeen@redhat.com> - 2.2.46-1
- Update to xfsdump version 2.2.46
- Dropped O_CREAT patch, now upstream

* Fri Aug 24 2007 Eric Sandeen <sandeen@redhat.com> - 2.2.45-3
- Update license tag
- Fix up O_CREAT opens with no mode
- Add gawk to buildrequires

* Tue Jun 19 2007 Eric Sandeen <sandeen@redhat.com> - 2.2.45-2
- Remove readline-devel & libtermcap-devel BuildRequires

* Thu May 31 2007 Eric Sandeen <sandeen@redhat.com> - 2.2.45-1
- Update to xfsdump 2.2.45

* Thu Aug 31 2006 Russell Cattelan <cattelan@thebarn.com> - 2.2.42-2
- Remove Distribution: tag

* Wed Aug 23 2006 Russell Cattelan <cattelan@thebarn.com> - 2.2.42-1
- update to version 2.2.42 

* Tue Aug 22 2006 Russell Cattelan <cattelan@thebarn.com> - 2.2.38-3
- Fix the /usr/sbin sym links to relative links
- Add the Distribution tag
- Add ncurses-devel to buildrequires

* Wed Aug 16 2006 Russell Cattelan <cattelan@thebarn.com> - 2.2.38-2
- install removes the makefile installed version of the docs
	package the docs based in the version specfic directory
 
* Wed Aug  9 2006 Russell Cattelan <cattelan@thebarn.com> - 2.2.38-1
- Add xfsdump to Fedora
