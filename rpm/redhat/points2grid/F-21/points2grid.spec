Summary:	Generate Digital Elevation Models (DEM) using a local gridding method
Name:		points2grid
Version:	1.3.0
Release:	3%{?dist}
License:	BSD
Source:		https://github.com/CRREL/%{name}/archive/%{version}.tar.gz
URL:		https://github.com/CRREL/points2grid
BuildRequires:	cmake libcurl-devel bzip2-devel gdal gdal-devel boost-devel >= 1.57
BuildRequires:	gcc-c++
Requires:	boost-iostreams >= 1.57 boost-program-options >= 1.57

%description
Points2Grid generates Digital Elevation Models (DEM) using a local gridding
method. The local gridding algorithm computes grid cell elevation using a
circular neighbourhood defined around each grid cell based on a radius
provided by the user. This neighbourhood is referred to as a bin, while the
grid cell is referred to as a DEM node. Up to four values — minimum, maximum,
mean, or inverse distance weighted (IDW) mean — are computed for points that
fall within the bin. These values are then assigned to the corresponding DEM
node and used to represent the elevation variation over the neighbourhood
represented by the bin. If no points are found within a given bin, the DEM
node receives a value of null. The Points2Grid service also provides a null
filing option, which applies an inverse distance weighted focal mean via a
square moving window of 3, 5, or 7 pixels to fill cells in the DEM that have
null values.

%package devel
Summary:        points2grid development header files and libraries
Group:          Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The pdal-devel package contains the header files and libraries needed to
compile C or C++ applications which will directly interact with PDAL.

%prep
%setup -q

%build
%cmake .
make %{?_smp_mflags}

%install
make install/fast DESTDIR=%{buildroot}

%postun -p /sbin/ldconfig
%post -p /sbin/ldconfig

%files
%doc README.rst RELEASE_NOTES
%license LICENSE
%{_bindir}/points2grid
/usr/lib/libpts2grd.so

%files devel
%{_includedir}/points2grid/

%changelog
* Mon Apr 20 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-3
 - Add -devel subpackage
 - omit deprecated Group: tags and %%clean section
 - Use better macros for make and cmake
 - use %%{?_isa} macro in subpkg dependencies
 - have %%build section envoke 'make'
 - Update %%install section
 - Improve cmake build parameters
 - Use %%license macro
 - Add %%doc
 - Get rid of BuildRoot definition
 - No need to cleanup buildroot during %%install
 - Remove %%defattr
 - Run ldconfig

* Sun Mar 8 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-2
- Rebuild with GDAL 1.11.2

* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial packaging

