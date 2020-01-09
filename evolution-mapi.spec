%define evo_version 2.32.0
%define eds_version 2.32.0
%define libmapi_version 1.0-4
%define intltool_version 0.35.5

%define evo_base_version 2.32
%define eds_api_version 1.2

%define strict_build_settings 0

### Abstract ###

Name: evolution-mapi
Version: 0.32.2
Release: 12%{?dist}
Group: Applications/Productivity
Summary: Evolution extension for MS Exchange 2007 servers
License: LGPLv2+
URL: http://www.gnome.org/projects/evolution-mapi/
Source: http://ftp.gnome.org/pub/gnome/sources/evolution-mapi/0.32/evolution-mapi-%{version}.tar.bz2
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

### Dependencies ###

Requires: evolution >= %{evo_version}
Requires: evolution-data-server >= %{eds_version}

### Patches ###

Patch01: evolution-mapi-0.32.2-gethierarchytable-fix.patch

# RH bug #605369 / less debug output on console
Patch02: evolution-mapi-0.28.3-less-debug-output.patch

# RH bug #680061
Patch03: evolution-mapi-0.28.3-crash-setting-props.patch

# RH bug #767678
Patch04: evolution-mapi-0.28.3-openchange-1.0.patch

# RH bug #694134
Patch05: evolution-mapi-0.32.2-books-for-offline.patch

# RH bug #625059
Patch06: evolution-mapi-0.32.2-slash-in-folder-name.patch

# RH bug #905591
Patch07: evolution-mapi-0.32.2-exchange2010.patch

# RH bug #909259
Patch08: evolution-mapi-0.32.2-meeting-invites.patch

# Address some of the Coverity scan issues
Patch09: evolution-mapi-0.32.2-covscan-issues.patch

# Translation updates
Patch10: evolution-mapi-0.32.2-translation-updates.patch

# RH bug #1005072
Patch11: evolution-mapi-0.32.2-profile-create-after-restore.patch

# RH bug #619842
Patch12: evolution-mapi-0.32.2-message-attachment-read.patch

# RH bug #621941
Patch13: evolution-mapi-0.32.2-show-events-owa.patch

# RH bug #906341
Patch14: evolution-mapi-0.32.2-create-book-cal-source.patch

# RH bug #1017108
Patch15: evolution-mapi-0.32.2-shorten-delay-of-open.patch

### Build Dependencies ###

BuildRequires: evolution-data-server-devel >= %{eds_version}
BuildRequires: evolution-devel >= %{evo_version}
BuildRequires: gettext
BuildRequires: intltool >= %{intltool_version}
BuildRequires: libtalloc-devel
BuildRequires: openchange-devel >= %{libmapi_version}
BuildRequires: samba4-devel

# Obsolete multilib version of this package,
# since openchange is no longer multilib.
Obsoletes: evolution-mapi < 0.28.3-9.el6

%description
This package allows Evolution to interact with MS Exchange 2007 servers.

%package devel
Summary: Development files for building against %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: evolution-data-server-devel >= %{eds_version}
Requires: evolution-devel >= %{evo_version}
Requires: openchange-devel >= %{libmapi_version}

%description devel
Development files needed for building things which link against %{name}.

%prep
%setup -q
%patch01 -p1 -b .gethierarchytable-fix
%patch02 -p1 -b .less-debug-output
%patch03 -p1 -b .crash-setting-props
%patch04 -p1 -b .openchange-1.0
%patch05 -p1 -b .books-for-offline
%patch06 -p1 -b .slash-in-folder-name
%patch07 -p1 -b .exchange2010
%patch08 -p1 -b .meeting-invites
%patch09 -p1 -b .covscan-issues
%patch10 -p1 -b .translation-updates
%patch11 -p1 -b .profile-create-after-restore
%patch12 -p1 -b .message-attachment-read
%patch13 -p1 -b .show-events-owa
%patch14 -p1 -b .create-book-cal-source
%patch15 -p1 -b .shorten-delay-of-open

%build

# Add stricter build settings here as the source code gets cleaned up.
# We want to make sure things like compiler warnings and avoiding deprecated
# functions in the GNOME/GTK+ libraries stay fixed.
#
# Please file a bug report at bugzilla.gnome.org if these settings break
# compilation, and encourage the upstream developers to use them.

%if %{strict_build_settings}
CFLAGS="$CFLAGS \
	-DG_DISABLE_DEPRECATED=1 \
	-DPANGO_DISABLE_DEPRECATED=1 \
	-DGDK_PIXBUF_DISABLE_DEPRECATED=1 \
	-DGDK_DISABLE_DEPRECATED=1 \
	-DGTK_DISABLE_DEPRECATED=1 \
	-DEDS_DISABLE_DEPRECATED=1 \
	-Wdeclaration-after-statement \
	-Werror-implicit-function-declaration"
%endif

%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -name '*.la' -exec rm {} \;

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

# COPYING has the wrong license.  Do not include it until fixed.

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog INSTALL README
%{_libdir}/libexchangemapi-1.0.so.*
%{_libdir}/evolution/%{evo_base_version}/plugins/*
%{_libdir}/evolution-data-server-%{eds_api_version}/camel-providers/libcamelmapi.so
%{_libdir}/evolution-data-server-%{eds_api_version}/camel-providers/libcamelmapi.urls
%{_libdir}/evolution-data-server-%{eds_api_version}/extensions/libebookbackendmapi.so
%{_libdir}/evolution-data-server-%{eds_api_version}/extensions/libecalbackendmapi.so
%{_datadir}/evolution-data-server-%{evo_base_version}/mapi

%files devel
%defattr(-,root,root,-)
%{_includedir}/evolution-data-server-%{evo_base_version}/mapi
%{_libdir}/libexchangemapi-1.0.so
%{_libdir}/pkgconfig/libexchangemapi-1.0.pc

%changelog
* Thu Oct 17 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-12
- Fix a copy&paste error in a patch update for RH bug #621941

* Wed Oct 16 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-11
- Update patch for RH bug #621941 (Created events not shown in OWA)
- Add patch for RH bug #1017108 (Shorten delay of calendar open)

* Mon Oct 14 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-10
- Add patch for RH bug #621941 (Created events not shown in OWA)
- Add patch for RH bug #906341 (Cannot create book/calendar)

* Thu Sep 19 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-9
- Update patch for RH bug #1005072 (Calendars could not authenticate)

* Wed Sep 11 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-8
- Add patch for RH bug #619842 (Attached email message is empty in forwarded email)

* Fri Sep 06 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-7
- Add patch for RH bug #1005072 (Authentication after migration/restore fails)

* Mon Aug 12 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-6
- Add patch for translation updates
- Update patch for issues found by Coverity scan

* Fri Jun 14 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-5
- Bump libmapi requirement to 1.0-4

* Wed Jun 12 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-4
- Add patch for some issues found by Coverity scan

* Tue Jun 11 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-3
- Add patch for RH bug #909259 (Meeting invite accept duplicates event)

* Fri Jun 07 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-2
- Add patch for RH bug #694134 (Contacts book not searchable)
- Add patch for RH bug #625059 (Allow slash in folder names)
- Add patch for RH bug #905591 (Refresh folder can fail with Exchange 2010 server)

* Mon Jun 03 2013 Milan Crha <mcrha@redhat.com> - 0.32.2-1
- Rebase to 0.32.2
- Remove patch for RH bug #589193 (obsolete by rebase)
- Remove patch for RH bug #602749 (part of rebase)
- Remove patch for RH bug #605369 (part of rebase)
- Remove patch for RH bug #666492 (obsolete by rebase)
- Remove patch for RH bug #902932 (merged to openchange-1.0 patch)
- Remove patch for RH bug #903241 (part of rebase)

* Wed Jan 23 2013 Milan Crha <mcrha@redhat.com> - 0.28.3-12
- Add patch for RH bug #903241 (Double-free on message copy/move)

* Tue Jan 22 2013 Milan Crha <mcrha@redhat.com> - 0.28.3-11
- Add patch for RH bug #902932 (Cannot connect with latest samba)

* Mon Jan 07 2013 Matthew Barnes <mbarnes@redhat.com> - 0.28.3-10
- Drop multilib by obsoleting evolution-mapi < 0.28.3-9 (RH bug #886914).

* Wed Oct 03 2012 Matthew Barnes <mbarnes@redhat.com> - 0.28.3-9
- Adapt to OpenChange 1.0 (RH bug #767678).

* Fri Sep 07 2012 Matthew Barnes <mbarnes@redhat.com> - 0.28.3-8
- Add patch for RH bug #680061 (crash while setting props).

* Tue Jan 18 2011 Milan Crha <mcrha@redhat.com> - 0.28.3-7
- Add patch for RH bug #666492 (crash with EDataBookView)

* Tue Aug 10 2010 Matthew Barnes <mbarnes@redhat.com> - 0.28.3-6
- Translation updates for Red Hat Supported Languages (RH bug #589193).

* Fri Jun 25 2010 Milan Crha <mcrha@redhat.com> - 0.28.3-5
- Bump openchange requirement to 0.9-7
- Add patches for RH bug #605369, namely:
  - Exchange 2010 support (tags and encrypted connection)
  - Less debug output on console
  - GNOME bug #569631 (Hangs during the initial fetch of calendar items)
  - GNOME bug #581434 (Double free or corruption in calendar)
  - GNOME bug #593176 (winmail.dat sent in outgoing plaintext mail)
  - GNOME bug #595914 (Doesn't display the Cyrrilic symbols in folder names)
  - GNOME bug #598564 (Has problems encoding mails containing html)
  - GNOME bug #600386 (Do not use charset on messages with UNICODE body fetched)
  - GNOME bug #600389 (UTF8 characters not shown properly)
  - GNOME bug #602896 (CC field is shown twice in message)
  - GNOME bug #607384 (Replying causes the message to appear as garbage)
  - GNOME bug #607422 (Crash while importing a message without From header)
  - GNOME bug #610224 (Crash on a meeting forward notification mail)

* Sat Jun 12 2010 Matthew Barnes <mbarnes@redhat.com> - 0.28.3-4
- Add patch for RH bug #602749 (extra Re: in replies).

* Fri Jun 11 2010 Matthew Barnes <mbarnes@redhat.com> - 0.28.3-3
- Translation updates for Red Hat Supported Languages (RH bug #589193).

* Wed Apr 28 2010 Matthew Barnes <mbarnes@redhat.com> - 0.28.3-2
- Rebuild against newer libmapi (RH bug #586901).

* Tue Mar 02 2010 Matthew Barnes <mbarnes@redhat.com> - 0.28.3-1
- Update to 0.28.3

* Wed Jan 13 2010 Milan Crha <mcrha@redhat.com> - 0.28.2-1
- Update to 0.28.2
- Disable build on s390/s390x, because evolution is too

* Mon Oct 19 2009 Milan Crha <mcrha@redhat.com> - 0.28.1-1
- Update to 0.28.1
- Remove patch for Gnome bug #588453 (fixed upstream).
- Remove patch for Gnome bug #595260 (fixed upstream).
- Remove patch for Gnome bug #595355 (fixed upstream).
- Remove patch for Gnome bug #595480 (fixed upstream).

* Tue Sep 22 2009 Milan Crha <mcrha@redhat.com> - 0.28.0-1
- Update to 0.28.0
- Add patch for Gnome bug #588453 (slow retrieval of message IDs).
- Add patch for Gnome bug #595260 (crash in mapi_sync_deleted).
- Add patch for Gnome bug #595355 (crash and incorrect header parsing).
- Add patch for Gnome bug #595480 (crash on fetching GAL).

* Mon Sep 07 2009 Milan Crha <mcrha@redhat.com> - 0.27.92-1
- Update to 0.27.92

* Mon Aug 24 2009 Milan Crha <mcrha@redhat.com> - 0.27.91-1
- Update to 0.27.91

* Mon Aug 10 2009 Milan Crha <mcrha@redhat.com> - 0.27.90-1
- Update to 0.27.90

* Tue Jul 28 2009 Milan Crha <mcrha@redhat.com> - 0.27.5-2
- Add new libebookbackendmapigal.so to a list of installed files.
- Bump requirement of evolution and evolution-data-server to 2.27.5.

* Mon Jul 27 2009 Milan Crha <mcrha@redhat.com> - 0.27.5-1
- Update to 0.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthew Barnes <mbarnes@redhat.com> - 0.27.4-1
- Update to 0.27.4

* Thu Jul 02 2009 Matthew Barnes <mbarnes@redhat.com> - 0.27.3-4
- Remove redundant library flag from pkg-config file.

* Mon Jun 29 2009 Matthew Barnes <mbarnes@redhat.com> - 0.27.3-3
- Rebuild against mutated openchange (see RH bug #503783).

* Fri Jun 26 2009 Matthew Barnes <mbarnes@redhat.com> - 0.27.3-2
- Remove ldconfig calls since all the libraries we install are
  dlopen'ed modules (RH bug #586991).

* Mon Jun 15 2009 Matthew Barnes <mbarnes@redhat.com> - 0.27.3-1
- Update to 0.27.3

* Fri May 29 2009 Matthew Barnes <mbarnes@redhat.com> - 0.27.2-1
- Update to 0.27.2

* Mon May 04 2009 Matthew Barnes <mbarnes@redhat.com> - 0.27.1-1
- Update to 0.27.1
- Bump eds_major to 2.28.
- Bump evo and eds req's to 2.27.1.

* Mon Apr 13 2009 Matthew Barnes <mbarnes@redhat.com> - 0.26.1-1
- Update to 0.26.1

* Thu Mar 19 2009 Matthew Barnes <mbarnes@redhat.com> - 0.26.0.1-1
- Update to 0.26.0.1

* Mon Mar 16 2009 Matthew Barnes <mbarnes@redhat.com> - 0.26.0-1
- Update to 0.26.0

* Mon Mar 02 2009 Matthew Barnes <mbarnes@redhat.com> - 0.25.92-1
- Update to 0.25.92

* Thu Feb 26 2009 Matthew Barnes <mbarnes@redhat.com> - 0.25.91-3
- Formal package review cleanups.

* Thu Feb 19 2009 Matthew Barnes <mbarnes@redhat.com> - 0.25.91-2
- Add some missing build requirements.

* Mon Feb 16 2009 Matthew Barnes <mbarnes@redhat.com> - 0.25.91-1
- Update to 0.25.91

* Thu Feb 05 2009 Matthew Barnes <mbarnes@redhat.com> - 0.25.90-1
- Update to 0.25.90

* Mon Jan 19 2009 Matthew Barnes <mbarnes@redhat.com> - 0.25.5-1
- Update to 0.25.5

* Tue Jan 06 2009 Matthew Barnes <mbarnes@redhat.com> - 0.25.4-1
- Update to 0.25.4
- Handle translations.

* Mon Dec 15 2008 Matthew Barnes <mbarnes@redhat.com> - 0.25.3-1
- Update to 0.25.3

* Fri Dec 12 2008 Matthew Barnes <mbarnes@redhat.com> - 0.1-1
- Initial packaging of evolution-mapi.
