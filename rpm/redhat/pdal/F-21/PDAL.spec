Summary:	Point Data Abstraction Library
Name:		PDAL
Version:	0.9.8
Release:	1%{?dist}
License:	BSD
Group:		Applications/Libraries
Source:		https://github.com/%{name}/%{name}/archive/%{version}.tar.gz
URL:		http://www.pdal.io
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake boost-devel >= 1.57, eigen3-devel, flann-devel, libusb-devel
BuildRequires:	opennni, metslib-devel, zlib-devel, libpng-devel, qhull-devel
BuildRequires:	libpcap-devel, vtk-devel qt-devel

%description
PDAL is a BSD licensed library for translating and manipulating point cloud
data of various formats. It is a library that is analogous to the GDAL raster
library. PDAL is focussed on reading, writing, and translating point cloud
data from the ever-growing constellation of data formats. While PDAL is not
explicitly limited to working with LiDAR data formats, its wides format
coverage is in that domain.

PDAL is related to Point Cloud Library (PCL) in the sense that both work with
point data, but PDAL’s niche is data translation and processing pipelines, and
PCL’s is more in the algorithmic exploition domain. There is cross over of both
niches, however, and PDAL provides a user the ability to exploit data using
PCL’s techniques.

%prep
%setup -q

%build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D HEXER_LIB_DIR=%{_libdir} .
%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/pc2pc
%{_bindir}/pcequal
%{_bindir}/pcinfo
%{_bindir}/pcpipeline
%{_bindir}/pcquery
%{_bindir}/pdal-config
%{_includedir}/pdal/*.h
%{_includedir}/pdal/*.hpp
%{_includedir}/pdal/drivers/buffer/*.hpp
%{_includedir}/pdal/drivers/caris/*.hpp
%{_includedir}/pdal/drivers/faux/*.hpp
%{_includedir}/pdal/drivers/las/*.hpp
%{_includedir}/pdal/drivers/mrsid/*.hpp
%{_includedir}/pdal/drivers/nitf/*.hpp
%{_includedir}/pdal/drivers/oci/*.hpp
%{_includedir}/pdal/drivers/oci/*.h
%{_includedir}/pdal/drivers/p2g/*.hpp
%{_includedir}/pdal/drivers/pgpointcloud/*.hpp
%{_includedir}/pdal/drivers/pipeline/*.hpp
%{_includedir}/pdal/drivers/qfit/*.hpp
%{_includedir}/pdal/drivers/soci/*.hpp
%{_includedir}/pdal/drivers/terrasolid/*.hpp
%{_includedir}/pdal/drivers/text/*.hpp
%{_includedir}/pdal/filters/*.hpp
%{_includedir}/pdal/plang/*.hpp
%{_includedir}/pdal/third/nanoflann.hpp
/usr/lib/libpdal.so
/usr/lib/libpdal.so.0

%changelog
* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 0.9.8-1
- Initial packaging

