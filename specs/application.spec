%global srcname example

Name:           %{srcname}
Version:        1.2.3
Release:        2%{?dist}
Summary:        An example Python application

License:        MIT
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%description
A Python application which provides a convenient example.


%prep
%autosetup -n %{srcname}-%{version}


%build
%py3_build


%install
%py3_install


%check
%{__python3} setup.py test


%files
%license COPYING
%doc README
%{python3_sitelib}/*
%{_bindir}/sample-exec


%changelog
...
