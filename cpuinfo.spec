#
# Conditional build:
%bcond_without perl
%bcond_without python

%define		rel	1
%define		svndate	20110325
Summary:	A CPU identification tool and library
Name:		cpuinfo
Version:	1.0
Release:	0.%{svndate}.%{rel}
License:	LGPL v2.1+, GPL v2+
Group:		Libraries
# based on branch at https://code.launchpad.net/cpuinfo/trunk, please don't
# replace until merged upstream
Source0:	%{name}-%{version}-%{svndate}.tar.xz
# Source0-md5:	8631f610a61403765a064a82464a1ebd
URL:		http://gwenole.beauchesne.info/projects/cpuinfo/
%if %{with perl}
BuildRequires:	perl-devel
%endif
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-setuptools
%endif
ExclusiveArch:	%{ix86} %{x8664} ppc ppc64 ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cpuinfo consists of an API/library used by programs to get information
about the underlying CPU. Such information includes CPU vendor, model
name, cache hierarchy, and supported features (e.g. CMP, SMT, and
SIMD). cpuinfo is also a standalone program to demonstrate the use of
this API.

%package devel
Summary:	Development files for cpuinfo
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and libraries needed to use cpuinfo's
processor characterisation features in your programs.

%package static
Summary:	Static library for cpuinfo
License:	LGPLv2.1+
Group:		Development/Libraries
Provides:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libraries needed to statically link
cpuinfo's processor characterisation features in your programs.

%package -n perl-Cpuinfo
Summary:	Perl bindings for cpuinfo
License:	GPL v2+
Group:		Development/Languages/Perl

%description -n perl-Cpuinfo
Provides a Perl API to the cpuinfo library.

%package -n python-cpuinfo
Summary:	Python bindings for cpuinfo
License:	GPL v2+
Group:		Libraries/Python

%description -n python-cpuinfo
Provides a Python API to the cpuinfo library.

%prep
%setup -q

%build
# NOTE: not autoconf generated configure
%configure \
	--with-cc="%{__cc}" \
	--enable-shared \
%if %{with perl}
	--enable-perl=vendor \
%endif
%if %{with python}
	--enable-python \
%endif
	--install-sdk

LDFLAGS="%{rpmldflags}" \
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install -j1 \
	DESTDIR=$RPM_BUILD_ROOT

# nuke unpackaged files
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/cpuinfo.pl
%{__rm} $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Cpuinfo/.packlist
%{__rm} $RPM_BUILD_ROOT%{perl_vendorarch}/auto/Cpuinfo/Cpuinfo.bs

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README NEWS
%attr(755,root,root) %{_bindir}/cpuinfo
%attr(755,root,root) %{_libdir}/libcpuinfo.so.*.*.*
%ghost %{_libdir}/libcpuinfo.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/cpuinfo.h
%{_pkgconfigdir}/libcpuinfo.pc
%{_libdir}/libcpuinfo.so

%files static
%defattr(644,root,root,755)
%{_libdir}/libcpuinfo.a

%if %{with perl}
%files -n perl-Cpuinfo
%defattr(644,root,root,755)
%doc src/bindings/perl/cpuinfo.pl
%{perl_vendorarch}/Cpuinfo.pm
%dir %{perl_vendorarch}/auto/Cpuinfo
%attr(755,root,root) %{perl_vendorarch}/auto/Cpuinfo/Cpuinfo.so
%endif

%if %{with python}
%files -n python-cpuinfo
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/CPUInfo.so
%{py_sitedir}/pycpuinfo-0.1-py*.egg-info
%endif
