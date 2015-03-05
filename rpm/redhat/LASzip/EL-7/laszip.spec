Summary:	Quickly turns bulky LAS files into compant LAZ files
Name:		laszip
Version:	2.2.0
Release:	1%{?dist}
License:	BSD
Group:		Development/Libraries
Source0:	https://github.com/LASzip/LASzip/releases/download/v%{version}/%{name}-src-%{version}.tar.gz
URL:		http://www.laszip.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	cmake

%description
LASzip - a free product of rapidlasso GmbH - quickly turns bulky LAS files into
compact LAZ files without information loss.

%prep
%setup -q -n %{name}-src-%{version}

%build
%configure --includedir=%{_includedir}/laszip

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# Remove .la files
%{__rm} -f %{buildroot}%{_libdir}/liblaszip.la

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc NEWS README INSTALL AUTHORS
%{_bindir}/laszippertest
%{_includedir}/laszip/*.hpp
%{_libdir}/liblaszip.a
%{_libdir}/liblaszip.so*

%changelog
* Tue Jan 13 2015 Devrim GUNDUZ <devrim@gunduz.org> 1.3.0-1
- Initial packaging

