%define openchange_version 2.3
%define intltool_version 0.35.5

%define evo_base_version 3.22

%define strict_build_settings 0

### Abstract ###

Name: evolution-mapi
Version: 3.22.6
Release: 1%{?dist}
Group: Applications/Productivity
Summary: Evolution extension for MS Exchange 2007 servers
License: LGPLv2+
URL: https://wiki.gnome.org/Apps/Evolution
Source: http://download.gnome.org/sources/%{name}/3.22/%{name}-%{version}.tar.xz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# GN-bug #729028
#Patch0: evolution-mapi-3.12.1-openchange-2.1-changes.patch

### Dependencies ###

Requires: evolution >= %{version}
Requires: evolution-data-server >= %{version}

### Build Dependencies ###

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gettext
BuildRequires: gnome-common
BuildRequires: intltool >= %{intltool_version}
BuildRequires: libtool >= 1.5

BuildRequires: pkgconfig(camel-1.2) >= %{version}
BuildRequires: pkgconfig(evolution-data-server-1.2) >= %{version}
BuildRequires: pkgconfig(evolution-mail-3.0) >= %{version}
BuildRequires: pkgconfig(evolution-shell-3.0) >= %{version}
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libebackend-1.2) >= %{version}
BuildRequires: pkgconfig(libebook-1.2) >= %{version}
BuildRequires: pkgconfig(libecal-1.2) >= %{version}
BuildRequires: pkgconfig(libedata-book-1.2) >= %{version}
BuildRequires: pkgconfig(libedata-cal-1.2) >= %{version}
BuildRequires: pkgconfig(libemail-engine) >= %{version}
BuildRequires: pkgconfig(libmapi) >= %{openchange_version}

%description
This package allows Evolution to interact with MS Exchange 2007 servers.

%package devel
Summary: Development files for building against %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig(camel-1.2) >= %{version}
Requires: pkgconfig(evolution-data-server-1.2) >= %{version}
Requires: pkgconfig(evolution-mail-3.0) >= %{version}
Requires: pkgconfig(evolution-shell-3.0) >= %{version}
Requires: pkgconfig(libebackend-1.2) >= %{version}
Requires: pkgconfig(libebook-1.2) >= %{version}
Requires: pkgconfig(libecal-1.2) >= %{version}
Requires: pkgconfig(libedata-book-1.2) >= %{version}
Requires: pkgconfig(libedata-cal-1.2) >= %{version}
Requires: pkgconfig(libemail-engine) >= %{version}
Requires: pkgconfig(libmapi) >= %{openchange_version}

%description devel
Development files needed for building things which link against %{name}.

%prep
%setup -q
#%patch0 -p1 -b .openchange-2.1-changes

%build

CFLAGS="$RPM_OPT_FLAGS"

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

export CFLAGS="$CFLAGS -Wno-deprecated-declarations"

# Regenerate configure to pick up changes
autoreconf --force --install

%configure --disable-maintainer-mode

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT/%{_libdir} -name '*.la' -exec rm {} \;

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING INSTALL README
%{_libdir}/libexchangemapi-1.0.so.*
%{_libdir}/evolution-data-server/camel-providers/libcamelmapi.so
%{_libdir}/evolution-data-server/camel-providers/libcamelmapi.urls
%{_libdir}/evolution-data-server/addressbook-backends/libebookbackendmapi.so
%{_libdir}/evolution-data-server/calendar-backends/libecalbackendmapi.so
%{_libdir}/evolution-data-server/registry-modules/module-mapi-backend.so
%{_libdir}/evolution/modules/module-mapi-configuration.so
%{_datadir}/appdata/evolution-mapi.metainfo.xml
%{_datadir}/evolution-data-server/mapi

%files devel
%{_includedir}/evolution-data-server/mapi
%{_libdir}/libexchangemapi-1.0.so
%{_libdir}/pkgconfig/libexchangemapi-1.0.pc

%changelog
* Mon Mar 13 2017 Milan Crha <mcrha@redhat.com> - 3.22.6-1
- Update to 3.22.6 upstream release

* Thu Feb 16 2017 Milan Crha <mcrha@redhat.com> - 3.22.4-1
- Rebase to 3.22.4

* Tue Aug 16 2016 Milan Crha <mcrha@redhat.com> - 3.12.10-5
- Add patch for RH bug #1366206 (Free/Busy Information returns wrong time)
- Add patch for RH bug #1367455 (No contacts are displayed until search is started)

* Fri Mar 04 2016 Milan Crha <mcrha@redhat.com> - 3.12.10-4
- Add patch for RH bug #1314261 (Rebuild against OpenChange 2.3)

* Wed Jul 08 2015 Milan Crha <mcrha@redhat.com> - 3.12.10-3
- Rebuild against updated libical

* Wed Jul 08 2015 Milan Crha <mcrha@redhat.com> - 3.12.10-2
- Rebuild against updated libical

* Mon May 04 2015 Milan Crha <mcrha@redhat.com> - 3.12.10-1
- Update to 3.12.10

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.8.5-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.8.5-5
- Mass rebuild 2013-12-27

* Thu Oct 17 2013 Milan Crha <mcrha@redhat.com> - 3.8.5-4
- Add patch for RH bug #1019910 (Recurring events not shown in OWA on Exchange 2010)

* Thu Sep 19 2013 Milan Crha <mcrha@redhat.com> - 3.8.5-3
- Fix URL tag in the .spec file to point to evolution project

* Fri Sep 13 2013 Milan Crha <mcrha@redhat.com> - 3.8.5-2
- Add patch for RH bug #619842 (Attached email message is empty in forwarded email)

* Mon Aug 12 2013 Milan Crha <mcrha@redhat.com> - 3.8.5-1
- Update to 3.8.5

* Wed Jul 24 2013 Milan Crha <mcrha@redhat.com> - 3.8.4-1
- Update to 3.8.4

* Mon Jun 10 2013 Milan Crha <mcrha@redhat.com> - 3.8.3-1
- Update to 3.8.3

* Mon May 13 2013 Milan Crha <mcrha@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Milan Crha <mcrha@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Mon Mar 25 2013 Milan Crha <mcrha@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Mon Mar 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.92-1
- Update to 3.7.92
- Remove patch to drop GTK_DOC_CHECK from configure.ac (fixed upstream)

* Mon Mar 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.91-1
- Update to 3.7.91
- Add patch to drop GTK_DOC_CHECK from configure.ac

* Mon Feb 18 2013 Milan Crha <mcrha@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Mon Feb 04 2013 Milan Crha <mcrha@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Mon Jan 14 2013 Milan Crha <mcrha@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Wed Dec 19 2012 Matthew Barnes <mbarnes@redhat.com> - 3.7.3-1
- Update to 3.7.3

* Mon Nov 19 2012 Milan Crha <mcrha@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Mon Oct 22 2012 Milan Crha <mcrha@redhat.com> - 3.7.1-1
- Update to 3.7.1

* Mon Sep 17 2012 Milan Crha <mcrha@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Mon Sep 03 2012 Milan Crha <mcrha@redhat.com> - 3.5.91-1
- Update to 3.5.91

* Mon Aug 20 2012 Milan Crha <mcrha@redhat.com> - 3.5.90-1
- Update to 3.5.90

* Mon Aug 06 2012 Milan Crha <mcrha@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Milan Crha <mcrha@redhat.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Mon Jun 04 2012 Milan Crha <mcrha@redhat.com> - 3.5.2-1
- Update to 3.5.2

* Sun Apr 29 2012 Matthew Barnes <mbarnes@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Tue Apr 24 2012 Milan Crha <mcrha@redhat.com> - 3.4.0-3
- Rebuild against newer OpenChange

* Thu Apr 19 2012 Milan Crha <mcrha@redhat.com> - 3.4.0-2
- Rebuild against newer OpenChange

* Tue Apr 03 2012 Milan Crha <mcrha@redhat.com> - 3.4.0-1
- Update to 3.4.0
- Bump OpenChange dependency to 1.0

* Tue Mar 06 2012 Milan Crha <mcrha@redhat.com> - 3.3.91-1
- Update to 3.3.91
- Remove add-rpath patch (obsolete)

* Thu Feb 23 2012 Milan Crha <mcrha@redhat.com> - 3.3.90-2
- Do not change rpath on .so files (fixes Red Hat bug #790056)

* Mon Feb 20 2012 Milan Crha <mcrha@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Mon Feb 06 2012 Milan Crha <mcrha@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Mon Jan 16 2012 Milan Crha <mcrha@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Milan Crha <mcrha@redhat.com> - 3.3.3-1
- Update to 3.3.3
- Remove patch to remove usage of deprecated flags (fixed upstream)

* Mon Nov 21 2011 Milan Crha <mcrha@redhat.com> - 3.3.2-1
- Update to 3.3.2
- Add patch to remove usage of deprecated flags

* Mon Oct 24 2011 Milan Crha <mcrha@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Mon Sep 26 2011 Milan Crha <mcrha@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Milan Crha <mcrha@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Mon Sep 05 2011 Milan Crha <mcrha@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Mon Aug 29 2011 Milan Crha <mcrha@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Mon Aug 15 2011 Milan Crha <mcrha@redhat.com> - 3.1.5-1
- Update to 3.1.5

* Thu Aug 11 2011 Milan Crha <mcrha@redhat.com> - 3.1.4-1
- Update to 3.1.4
- Remove patch to enable GLib deprecated stuff (fixed upstream)

* Tue Jul 05 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Tue Jun 14 2011 Milan Crha <mcrha@redhat.com> - 3.1.2-1
- Update to 3.1.2
- Add patch to enable GLib deprecated stuff (due to G_CONST_RETURN deprecation)

* Mon May 09 2011 Milan Crha <mcrha@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Wed Apr 06 2011 Matthew Barnes <mbarnes@redhat.com> - 3.0.0-2
- Rebuild against newer Samba4 and OpenChange libraries.

* Mon Apr 04 2011 Milan Crha <mcrha@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 21 2011 Milan Crha <mcrha@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar 07 2011 Milan Crha <mcrha@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Mon Feb 21 2011 Milan Crha <mcrha@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-2
- Rebuild

* Mon Jan 31 2011 Milan Crha <mcrha@redhat.com> - 2.91.6-1
- Update to 2.91.6

* Mon Jan 10 2011 Milan Crha <mcrha@redhat.com> - 2.91.5-1
- Update to 2.91.5

* Mon Dec 20 2010 Milan Crha <mcrha@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Mon Nov 29 2010 Milan Crha <mcrha@redhat.com> - 2.91.3-1
- Update to 2.91.3

* Mon Nov 08 2010 Milan Crha <mcrha@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Mon Oct 18 2010 Milan Crha <mcrha@redhat.com> - 2.91.1-1
- Update to 2.91.1

* Mon Oct 11 2010 Milan Crha <mcrha@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 0.31.92-3
- Rebuilt for gcc bug 634757

* Tue Sep 14 2010 Milan Crha <mcrha@redhat.com> - 0.31.92-2
- Bump openchange requirement to 0.9-8

* Mon Sep 13 2010 Milan Crha <mcrha@redhat.com> - 0.31.92-1
- Update to 0.31.92
- Remove patch for Gnome bug #627999 (fixed upstream)

* Mon Aug 30 2010 Milan Crha <mcrha@redhat.com> - 0.31.91-1
- Update to 0.31.91
- Add patch for Gnome bug #627999 (Cannot autocomplete)

* Mon Aug 16 2010 Matthew Barnes <mbarnes@redhat.com> - 0.31.90-1
- Update to 0.31.90

* Mon Aug 02 2010 Matthew Barnes <mbarnes@redhat.com> - 0.31.6-1
- Update to 0.31.6
- Roll back evo_base_version to 2.32.

* Tue Jul 13 2010 Milan Crha <mcrha@redhat.com> - 0.31.5-1
- Update to 0.31.5

* Mon Jun 07 2010 Milan Crha <mcrha@redhat.com> - 0.31.3-1
- Update to 0.31.3

* Mon May 24 2010 Milan Crha <mcrha@redhat.com> - 0.31.2-1
- Update to 0.31.2

* Mon May 03 2010 Milan Crha <mcrha@redhat.com> - 0.31.1-1
- Update to 0.31.1

* Mon Feb 08 2010 Milan Crha <mcrha@redhat.com> - 0.29.90-1
- Update to 0.29.90

* Mon Jan 25 2010 Milan Crha <mcrha@redhat.com> - 0.29.6-1
- Update to 0.29.6

* Tue Jan 12 2010 Milan Crha <mcrha@redhat.com> - 0.29.5-1
- Update to 0.29.5

* Sat Jan 09 2010 Matthew Barnes <mbarnes@redhat.com> - 0.29.4-2
- Rebuild against OpenChange 0.9.

* Mon Dec 21 2009 Milan Crha <mcrha@redhat.com> - 0.29.4-1
- Update to 0.29.4

* Mon Nov 30 2009 Milan Crha <mcrha@redhat.com> - 0.29.3-1
- Update to 0.29.3
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
