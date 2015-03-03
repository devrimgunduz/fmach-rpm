Summary:	LAS and OGR hexagonal density and boundary surface generation
Name:		hexer
Version:	1.3.0
Release:	1%{?dist}
License:	BSD
Group:		Applications/Libraries
Source:		https://github.com/hobu/hexer/archive/%{version}.tar.gz
URL:		https://github.com/hobu/hexer
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake
BuildRequires:	boost-program-options >= 1.57, boost-thread >= 1.57, boost-iostreams >= 1.57
BuildRequires:	boost-filesystem >= 1.57, boost-system >= 1.57, boost-random >= 1.57

%description
Hexer is a LGPL C++ library that provides some classes for generating hexbin
density surfaces and multipolygon boundaries for large point sets.Hexer
supports two operations at this time, density and boundary. You use hexer
through the curse command.

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
%doc README.md
%{_bindir}/curse
%{_includedir}/hexer/Draw.hpp
%{_includedir}/hexer/HexGrid.hpp
%{_includedir}/hexer/HexInfo.hpp
%{_includedir}/hexer/HexIter.hpp
%{_includedir}/hexer/Hexagon.hpp
%{_includedir}/hexer/Mathpair.hpp
%{_includedir}/hexer/Path.hpp
%{_includedir}/hexer/Processor.hpp
%{_includedir}/hexer/Segment.hpp
%{_includedir}/hexer/Utils.hpp
%{_includedir}/hexer/exception.hpp
%{_includedir}/hexer/export.hpp
%{_includedir}/hexer/gitsha.h
%{_includedir}/hexer/hexer.hpp
%{_includedir}/hexer/hexer_defines.h
#%{_libdir}/libhexer.so
#%{_libdir}/libhexer.so.1.0.2
/usr/lib//libhexer.so
/usr/lib/libhexer.so.1.0.2

%changelog
* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial packaging

