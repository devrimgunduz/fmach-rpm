Summary:	Extensible library solution for reading and writing National Imagery Transmission Format (NITF)
Name:		nitro
Version:	2.7
Release:	1%{?dist}
License:	BSD
Group:		Development/Libraries
Source:		nitro-2.7.tar.bz2
URL:		https://github.com/hobu/nitro
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake

%description
Nitro is a library that provides NITF support for PDAL to write LAS-in-NITF
files for writers.nitf.

%prep
%setup -q

%build
cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr -D STATIC_BUILD:BOOL=OFF .

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc README.md
%{_includedir}/nitro/c++/except/*.h
%{_includedir}/nitro/c++/import/*.h
%{_includedir}/nitro/c++/import/*.hpp
%{_includedir}/nitro/c++/io/*.h
%{_includedir}/nitro/c++/logging/*.h
%{_includedir}/nitro/c++/mem/*.h
%{_includedir}/nitro/c++/mt/*.h
%{_includedir}/nitro/c++/nitf/*.hpp
%{_includedir}/nitro/c++/str/*.h
%{_includedir}/nitro/c++/sys/*.h
%{_includedir}/nitro/c/import/*.h
%{_includedir}/nitro/c/nitf/*.h
%{_includedir}/nitro/c/nrt/*.h
   /usr/lib/libnitf-c.so
   /usr/lib/libnitf-cpp.so
   /usr/pkgconfig/libnitf.pc

%changelog
* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial packaging

