# TODO
# - 1 test fails:
#  BAD: wrong value for dbus_message_get_reply_serial (reply), expected 2 got 3
#        at tests/test_dbus_message.c:149 (test_message_error).
#  Abort
#  FAIL: test_dbus_message
#
# Conditional build:
%bcond_without	static_libs	# static libraries
%bcond_with	tests		# build without tests

Summary:	Lightweight application development library
Summary(pl.UTF-8):	Lekka biblioteka do tworzenia aplikacji
Name:		libnih
Version:	1.0.3
Release:	3
License:	GPL v2
Group:		Libraries
Source0:	https://launchpad.net/libnih/1.0/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	db7990ce55e01daffe19006524a1ccb0
Patch0:		pkgconfig-libdir.patch
URL:		https://launchpad.net/libnih/
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.11
BuildRequires:	dbus-devel >= 1.2.16
BuildRequires:	expat-devel >= 1:2.0.0
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	libtool >= 2:2.2.4
BuildRequires:	pkgconfig >= 1:0.22
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fstack-protector -fPIE
%define		specldflags	-Wl,-z,now -pie

# Filter unsatisfied GLIBC_PRIVATE depenency (caused by using __abort_msg private symbol)
%define		_noautoreq	(GLIBC_PRIVATE)

%description
libnih is a small library for C application development containing
functions that, despite its name, are not implemented elsewhere in the
standard library set.

libnih is roughly equivalent to other C libraries such as glib, except
that its focus is on a small size and intended for applications that
sit very low in the software stack, especially outside of /usr.

%description -l pl.UTF-8
libnih to mała biblioteka do tworzenia aplikacji w C, zawierająca
funkcje, które, wbrew nazwie, nie zostały zaimplementowane nigdzie
indziej w zbiorze standardowych bibliotek.

libnih jest w przybliżeniu odpowiednikiem innych bibliotek C, takich
jak glib, ale skupia się na małym rozmiarze i jest przeznaczona dla
aplikacji położonych nisko w programowym stosie, szczególnie poza
/usr.

%package devel
Summary:	Development files for NIH libraries
Summary(pl.UTF-8):	Pliki programistyczne bibliotek NIH
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The libnih-devel package contains the header files for developing
applications that use libnih.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących libnih.

%package static
Summary:	Static NIH libraries
Summary(pl.UTF-8):	Statyczne biblioteki NIH
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static NIH libraries.

%description static -l pl.UTF-8
Statyczne biblioteki NIH.

%prep
%setup -q
%patch -P0 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

LDFLAGS="%{rpmldflags} %{specldflags}"
%configure \
	--disable-rpath \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la

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
%attr(755,root,root) %{_libdir}/libnih.so
%attr(755,root,root) %{_libdir}/libnih-dbus.so
%{_includedir}/libnih.h
%{_includedir}/libnih-dbus.h
%{_includedir}/nih
%{_includedir}/nih-dbus
%{_pkgconfigdir}/libnih.pc
%{_pkgconfigdir}/libnih-dbus.pc
%{_aclocaldir}/libnih.m4
%{_mandir}/man1/nih-dbus-tool.1*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libnih.a
%{_libdir}/libnih-dbus.a
%endif
