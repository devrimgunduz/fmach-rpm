# Warning to ELGIS:
# 1 of the 41 tests is known to fail on EL6 (32 bit and 64 bit Intel)
# Tests pass though on PPC and PPC64
# The author is informed about that.
# The problem seems to stem from Geos.

#EPSG data in libspatialite should be in sync with our current GDAL version

# A new feature available in PostGIS 2.0
#%%global _lwgeom "--enable-lwgeom=yes"
# Disabled due to a circular dependency issue with PostGIS
# https://bugzilla.redhat.com/show_bug.cgi?id=979179
%global _lwgeom "--disable-lwgeom"

# Geocallbacks work with SQLite 3.7.3 and up, available in Fedora and EL 7
%if (0%{?fedora} || 0%{?rhel} > 6)
  %global _geocallback "--enable-geocallbacks"
%endif

%if 0%{?rhel} == 6
# Checks are known to fail if libspatialite is built without geosadvanced
#TODO: Fails to build, reported by mail. If geosadvanced is disabled, linker flags miss geos_c
#TODO: Check if that's still true anywhere
  %global _geosadvanced "--disable-geosadvanced"
  %global _no_checks 1
%endif

%if 0%{?rhel} == 5
# GEOS 3.2 is no longer supported
  %global _geos"--disable-geos"

# The author expects malfunction in versions of libxml2 older than 2.8
  %global _libxml2 "--disable-libxml2"
%endif

# check_bufovflw test fails on gcc 4.9
# https://groups.google.com/forum/#!msg/spatialite-users/zkGP-gPByXk/EAZ-schWn1MJ
%if 0%{?fedora} >= 21
  %global _no_checks 1
%endif

Name:      libspatialite
Version:   4.2.0
Release:   4%{?dist}
Summary:   Enables SQLite to support spatial data
Group:     System Environment/Libraries
License:   MPLv1.1 or GPLv2+ or LGPLv2+
URL:       https://www.gaia-gis.it/fossil/libspatialite
Source0:   http://www.gaia-gis.it/gaia-sins/%{name}-sources/%{name}-%{version}.tar.gz

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# EPEL 5 reminiscences are for ELGIS

BuildRequires: freexl-devel
BuildRequires: geos-devel
BuildRequires: proj-devel >= 4.9.0
BuildRequires: sqlite-devel
BuildRequires: zlib-devel

%if (0%{?fedora} || 0%{?rhel} > 6)
BuildRequires: libxml2-devel
#BuildRequires: postgis
%endif


%description
SpatiaLite is a a library extending the basic SQLite core
in order to get a full fledged Spatial DBMS, really simple
and lightweight, but mostly OGC-SFS compliant.

%package devel
Summary:  Development libraries and headers for SpatiaLite
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q

%build
%configure \
    --disable-static \
    %{?_lwgeom}   \
    %{?_libxml2}   \
    %{?_geos}   \
    %{?_geocallback}   \
    %{?_geosadvanced}

make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

# Delete undesired libtool archives
find %{buildroot} -type f -name "*.la" -delete

%check
%if 0%{?_no_checks}
# Run check but don't fail build
make check V=1 ||:
%else
make check V=1
%endif


%clean
rm -rf %{buildroot}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files 
%doc COPYING AUTHORS
%{_libdir}/%{name}.so.7*
%{_libdir}/mod_spatialite.so.7*
# The symlink must be present to allow loading the extension
# https://groups.google.com/forum/#!topic/spatialite-users/zkGP-gPByXk
%{_libdir}/mod_spatialite.so

%files devel
%doc examples/*.c
%{_includedir}/spatialite.h
%{_includedir}/spatialite
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/spatialite.pc


%changelog
* Tue Mar 3 2015 Devrim Gunduz <devrim@gunduz.org> - 4.2.0-4
- Initial build for FMACH repo
- Trim changelog
- Add explicit version dependency to proj.
