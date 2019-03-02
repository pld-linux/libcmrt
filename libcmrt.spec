#
# Conditional build:
%bcond_without	static_libs	# static library

%define	libva_ver	1.2.0

Summary:	C for Media Runtime - media GPU kernel manager for Intel GPUs
Summary(pl.UTF-8):	C for Media Runtime - zarządca jąder GPU dla układów Intela
Name:		libcmrt
Version:	1.0.6
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/intel/cmrt/releases
Source0:	https://github.com/intel/cmrt/archive/%{version}/cmrt-%{version}.tar.gz
# Source0-md5:	91f5845c9354cce44a5133337f4e881c
Patch0:		x32.patch
URL:		https://github.com/intel/cmrt
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	libdrm-devel >= 2.4.23
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:1.5
BuildRequires:	libva-devel >= %{libva_ver}
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libva) >= 0.34
Requires:	libdrm >= 2.4.23
Requires:	libva >= %{libva_ver}
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

%package jitter
Summary:	Online compiler to convert VirtualISA into Gen HW instructions
Summary(pl.UTF-8):	Kompilator w locie reprezentacji VirtualISA na instrukcje Gen HW
License:	distributable, non-free, closed source
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++ >= 6:4.8

%description jitter
Jitter (igfxcmjit32.so or igfxcmjit64.so) is an online compiler to
convert VirtualISA into Gen HW instruction, while VirtualISA is an
intermediate representation between CM source code and HW instruction.

%description jitter -l pl.UTF-8
Jitter (igfxcmjit32.so lub igfxcmjit64.so) to działający w locie
kompilator przekształcający reprezentację VirtualISA na instrukcje Gen
HW. VirtualISA to reprezentacja pośrednia między kodem źródłowym CM a
instrukcjami sprzętowymi.

%package devel
Summary:	Header files for CMRT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CMRT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

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
%{__aclocal} -I m4
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

%ifarch %{ix86}
install jitter/igfxcmjit32.so $RPM_BUILD_ROOT%{_libdir}
%endif
%ifarch %{x8664}
install jitter/igfxcmjit64.so $RPM_BUILD_ROOT%{_libdir}
%endif

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcmrt.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README
%attr(755,root,root) %{_libdir}/libcmrt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcmrt.so.1
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cmrt.conf

%ifarch %{ix86} %{x8664}
%files jitter
%defattr(644,root,root,755)
%doc jitter/{LICENSE,readme}.txt
%ifarch %{ix86}
%attr(755,root,root) %{_libdir}/igfxcmjit32.so
%endif
%ifarch %{x8664}
%attr(755,root,root) %{_libdir}/igfxcmjit64.so
%endif
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcmrt.so
%{_includedir}/cm_rt*.h
%{_pkgconfigdir}/libcmrt.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcmrt.a
%endif
