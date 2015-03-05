Name:		libgeotiff
Version:	1.4.0
Release:	3%{?dist}
Summary:	GeoTIFF format library
Group:		System Environment/Libraries
License:	MIT
URL:		http://trac.osgeo.org/geotiff/
Source:		http://download.osgeo.org/geotiff/libgeotiff/libgeotiff-%{version}.tar.gz
BuildRequires:	libtiff-devel libjpeg-devel proj-devel >= 4.9.0 zlib-devel

%description
GeoTIFF represents an effort by over 160 different remote sensing, 
GIS, cartographic, and surveying related companies and organizations 
to establish a TIFF based interchange format for georeferenced 
raster imagery.

%package devel
Summary:	Development Libraries for the GeoTIFF file format library
Group:		Development/Libraries
Requires:	pkgconfig libtiff-devel
Requires:	%{name} = %{version}-%{release}

%description devel
The GeoTIFF library provides support for development of geotiff image format.

%prep
%setup -q

# fix wrongly encoded files from tarball
set +x
for f in `find . -type f` ; do
   if file $f | grep -q ISO-8859 ; then
      set -x
      iconv -f ISO-8859-1 -t UTF-8 $f > ${f}.tmp && \
	mv -f ${f}.tmp $f
      set +x
   fi
   if file $f | grep -q CRLF ; then
      set -x
      sed -i -e 's|\r||g' $f
      set +x
   fi
done
set -x

# remove junks
find . -name ".cvsignore" -exec rm -rf '{}' \;

%build

# disable -g flag removal
sed -i 's| \| sed \"s\/-g \/\/\"||g' configure

# use gcc -shared instead of ld -shared to build with -fstack-protector
sed -i 's|LD_SHARED=@LD_SHARED@|LD_SHARED=@CC@ -shared|' Makefile.in

%configure \
	--prefix=%{_prefix} \
	--includedir=%{_includedir}/%{name}/ \
	--with-proj \
	--with-jpeg \
	--with-zip

# WARNING
# disable %{?_smp_mflags}
# it breaks compile

make

%install
# install libgeotiff
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p"

# install manualy some file
install -p -m 755 bin/makegeo %{buildroot}%{_bindir}

# install pkgconfig file
cat > %{name}.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/%{name}

Name: %{name}
Description: GeoTIFF file format library
Version: %{version}
Libs: -L\${libdir} -lgeotiff
Cflags: -I\${includedir}
EOF

mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -p -m 644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

#clean up junks
rm -rf %{buildroot}%{_libdir}/*.a
echo  >> %{buildroot}%{_datadir}/epsg_csv/codes.csv
%{__rm} -f %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files 
%doc ChangeLog LICENSE README
%{_bindir}/applygeo
%{_bindir}/geotifcp
%{_bindir}/listgeo
%{_bindir}/makegeo
%{_libdir}/libgeotiff.so.*
%dir %{_datadir}/epsg_csv
%attr(0644,root,root) %{_datadir}/epsg_csv/*.csv
%{_mandir}/man1/listgeo.1.gz

%files devel
%dir %{_includedir}/%{name}
%attr(0644,root,root) %{_includedir}/%{name}/*.h
%attr(0644,root,root) %{_includedir}/%{name}/*.inc
%{_libdir}/libgeotiff.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Mar 5 2015 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-3
- Rebuild with new proj.

* Sat Dec 27 2014 Devrim Gündüz <devrim@gunduz.org> - 1.4.0-1
- Initial build for PostgreSQL YUM repository, to satisfy dependency
  for gdal (and so PostGIS). based on EPEL spec.
