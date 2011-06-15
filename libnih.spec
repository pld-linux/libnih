# TODO
# - check why make re-invokes configure again
# - 1 test fails:
#  BAD: wrong value for dbus_message_get_reply_serial (reply), expected 2 got 3
#        at tests/test_dbus_message.c:149 (test_message_error).
#  Abort
#  FAIL: test_dbus_message
#
# Conditional build:
%bcond_with	tests		# build without tests

Summary:	Lightweight application development library
Name:		libnih
Version:	1.0.3
Release:	1
License:	GPL v2
Group:		Libraries
URL:		https://launchpad.net/libnih/
Source0:	http://launchpad.net/libnih/1.0/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	db7990ce55e01daffe19006524a1ccb0
Patch0:		pkgconfig-libdir.patch
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-devel >= 1.2.16
BuildRequires:	expat-devel >= 1:2.0.0
BuildRequires:	gettext >= 0.17
BuildRequires:	gettext-devel
BuildRequires:	libtool >= 2:2.2.4
BuildRequires:	pkgconfig >= 0.22
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fstack-protector -fPIE
%define		specldflags	-Wl,-z,now -pie

# Filter GLIBC_PRIVATE Requires
%define		_noautoreq	(GLIBC_PRIVATE)

%description
libnih is a small library for C application development containing
functions that, despite its name, are not implemented elsewhere in the
standard library set.

libnih is roughly equivalent to other C libraries such as glib, except
that its focus is on a small size and intended for applications that
sit very low in the software stack, especially outside of /usr.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The libnih-devel package contains libraries and header files for
developing applications that use libnih.

%prep
%setup -q
%patch0 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__automake}
%{__autoconf}
%{__autoheader}

LDFLAGS="%{rpmldflags} %{specldflags}"
%configure \
	--disable-static \
	--disable-rpath

# prevent make from re-running auto-tools and configure
touch aclocal.m4 configure config.status Makefile.in Makefile config.h.in

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# move to /%{_lib} for upstart
install -d $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libnih.so.* $RPM_BUILD_ROOT/%{_lib}
mv $RPM_BUILD_ROOT%{_libdir}/libnih-dbus.so.* $RPM_BUILD_ROOT/%{_lib}
ln -fs /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libnih.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libnih.so
ln -fs /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libnih-dbus.so.*.*) $RPM_BUILD_ROOT%{_libdir}/libnih-dbus.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README AUTHORS ChangeLog
%attr(755,root,root) /%{_lib}/libnih.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libnih.so.1
%attr(755,root,root) /%{_lib}/libnih-dbus.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libnih-dbus.so.1

%files devel
%defattr(644,root,root,755)
%doc HACKING TODO
%attr(755,root,root) %{_bindir}/nih-dbus-tool
%{_mandir}/man1/nih-dbus-tool.1*
%{_libdir}/libnih.la
%{_libdir}/libnih.so
%{_libdir}/libnih-dbus.la
%{_libdir}/libnih-dbus.so
%{_includedir}/libnih.h
%{_includedir}/libnih-dbus.h
%{_includedir}/nih
%{_includedir}/nih-dbus
%{_pkgconfigdir}/libnih.pc
%{_pkgconfigdir}/libnih-dbus.pc
%{_aclocaldir}/libnih.m4
