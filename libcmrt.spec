#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	C for Media Runtime - media GPU kernel manager for Intel GPUs
Summary(pl.UTF-8):	C for Media Runtime - zarządca jąder GPU dla układów Intela
Name:		libcmrt
Version:	1.0.5
Release:	3
License:	MIT
Group:		Libraries
Source0:	https://github.com/01org/cmrt/archive/%{version}.tar.gz
# Source0-md5:	9a1afc0c0b24f4bac6c629aa5a57e41e
Patch0:		x32.patch
URL:		https://github.com/01org/cmrt
BuildRequires:	libdrm-devel >= 2.4.23
BuildRequires:	libstdc++-devel
BuildRequires:	libva-devel >= 1.2.0
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libva) >= 0.34
Requires:	libdrm >= 2.4.23
Requires:	libva >= 1.2.0
ExclusiveArch:	%{ix86} %{x8664} x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
One solution to expose Intel's Gen GPU's high performance through high
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

%description -l pl.UTF-8
Rozwiązanie mające na celu udostępnienie wysokiej wydajności
procesorów graficznych (GPU) Intel Gen poprzez język wysokopoziomowy.

Możliwości:
- interfejs między programem hostującym a sterownikiem
- zarządzanie urządzeniem Gen
- zarządzanie powierzchniami
- zarządzanie jądrami GPU
- zarządzanie zdarzeniami
- zarządzanie wątkami
- zarządzanie wykonywaniem
- przygotowywanie argumentów dla jąder GPU
- przesyłanie pamięci między pamięcią systemową a GPU
- raportowanie błędów

%package devel
Summary:	Header files for CMRT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CMRT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libdrm-devel >= 2.4.23
Requires:	libva-devel >= 1.2.0

%description devel
Header files for CMRT library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CMRT.

%package static
Summary:	Static CMRT library
Summary(pl.UTF-8):	Statyczna biblioteka CMRT
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static CMRT library.

%description static -l pl.UTF-8
Statyczna biblioteka CMRT.

%prep
%setup -q -n cmrt-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcmrt.la

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS
%attr(755,root,root) %{_libdir}/libcmrt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcmrt.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cmrt.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmrt.so
%{_includedir}/cm_rt*.h
%{_pkgconfigdir}/cmrt.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcmrt.a
%endif
