Summary:	points2grid
Name:		points2grid
Version:	1.3.0
Release:	2%{?dist}
License:	BSD
Group:		Applications/Libraries
Source:		https://github.com/CRREL/%{name}/archive/%{version}.tar.gz
URL:		https://github.com/CRREL/points2grid
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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

%prep
%setup -q

%build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr .

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/points2grid
%{_includedir}/points2grid/CoreInterp.hpp
%{_includedir}/points2grid/Global.hpp
%{_includedir}/points2grid/GridFile.hpp
%{_includedir}/points2grid/GridMap.hpp
%{_includedir}/points2grid/GridPoint.hpp
%{_includedir}/points2grid/InCoreInterp.hpp
%{_includedir}/points2grid/Interpolation.hpp
%{_includedir}/points2grid/OutCoreInterp.hpp
%{_includedir}/points2grid/config.h
%{_includedir}/points2grid/export.hpp
%{_includedir}/points2grid/lasfile.hpp
 /usr/lib/libpts2grd.so

%changelog
* Sun Mar 8 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-2
- Rebuild with GDAL 1.11.2

* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial packaging

