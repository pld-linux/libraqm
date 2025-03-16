#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library
%bcond_without	tests		# unit tests
#
%define		fribidi_ver	1.0.6
#
Summary:	Library for complex text layout
Summary(pl.UTF-8):	Biblioteka do skomplikowanego układu tekstu
Name:		libraqm
Version:	0.10.2
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/HOST-Oman/libraqm/releases
Source0:	https://github.com/HOST-Oman/libraqm/releases/download/v%{version}/raqm-%{version}.tar.xz
# Source0-md5:	ad99436e043caebbee6392a530c86d8e
URL:		https://github.com/HOST-Oman/libraqm
# pkgconfig(freetype2) >= 24.0.18
BuildRequires:	freetype-devel >= 1:2.11.0
BuildRequires:	fribidi-devel >= %{fribidi_ver}
%{?with_tests:BuildRequires:	glib2-devel >= 2.0}
%if %{with tests} && %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	harfbuzz-devel >= 3.0.0
BuildRequires:	meson >= 0.56.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.20
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	fribidi >= %{fribidi_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Raqm is a small library that encapsulates the logic for complex text
layout and provide a convenient API.

It currently provides bidirectional text support (using FriBiDi),
shaping (using HarfBuzz), and proper script itemization. As a result,
Raqm can support most writing systems covered by Unicode.

%description -l pl.UTF-8
Raqm to mała biblioteka opakowująca logikę złożonego układu tekstu i
udostępniająca wygodne API.

Obecnie zapewnia obsługę tekstu dwukierunkowego (przy użyciu FriBiDi),
formowanie (przy użyciu HarfBuzz) i właściwe wyszczególnienie pisma.
W efekcie Raqm potrafi obsłużyć większość systemów pisma pokrytych
przez Unikod.

%package devel
Summary:	Header files for Raqm library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Raqm
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freetype-devel >= 1:2.11.0
Requires:	fribidi-devel >= %{fribidi_ver}
Requires:	harfbuzz-devel >= 3.0.0

%description devel
Header files for Raqm library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Raqm.

%package static
Summary:	Static Raqm library
Summary(pl.UTF-8):	Statyczna biblioteka Raqm
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Raqm library.

%description static -l pl.UTF-8
Statyczna biblioteka Raqm.

%package apidocs
Summary:	API documentation for Raqm library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Raqm
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Raqm library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Raqm.

%prep
%setup -q -n raqm-%{version}

%build
%meson \
	-Ddocs=true

%meson_build

%if %{with tests}
LC_ALL=C.UTF-8 \
%meson_test
%endif

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README.md
%attr(755,root,root) %{_libdir}/libraqm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libraqm.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libraqm.so
%{_includedir}/raqm.h
%{_includedir}/raqm-version.h
%{_pkgconfigdir}/raqm.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libraqm.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/raqm
%endif
