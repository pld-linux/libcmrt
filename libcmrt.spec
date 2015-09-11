Summary:	C for Media Runtime
Name:		libcmrt
Version:	1.0.5
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/01org/cmrt/archive/%{version}.tar.gz
# Source0-md5:	9a1afc0c0b24f4bac6c629aa5a57e41e
URL:		https://github.com/01org/cmrt
BuildRequires:	libdrm-devel >= 2.4.23
BuildRequires:	libva-devel >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
One solution to expose Intel’s Gen GPU’s high performance through high
level language.

Features:
- Interface between host program and driver
- Manage Gen device
- Manage surfaces
- Manage media GPU kernels
- Manage events
- Manage threads
- Manage execution
- Prepare media GPU kernel arguments
- Transfer data between system and GPU memory
- Report errors

%package devel
Summary:	Header files and development documentation for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and development documentation for %{name}.

%prep
%setup -q -n cmrt-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
		--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libcmrt.so.1
%attr(755,root,root) %{_libdir}/libcmrt.so.*.*.*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cmrt.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmrt.so
%{_includedir}/cm_rt*.h
%{_pkgconfigdir}/cmrt.pc
%{_libdir}/libcmrt.la
