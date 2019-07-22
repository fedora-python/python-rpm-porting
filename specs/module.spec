%global srcname example

Name:           python-%{srcname}
Version:        1.2.3
Release:        2%{?dist}
Summary:        An example Python module

License:        MIT
URL:            https://pypi.org/project/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python3-devel

%description
A Python module which provides a convenient example.


%package -n python2-%{srcname}
Summary:        %{summary}
Requires:       python2-some-module
Requires:       python2-other-module
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A Python module which provides a convenient example.


%package -n python3-%{srcname}
Summary:        %{summary}
Requires:       python3-some-module
Requires:       python3-other-module
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A Python module which provides a convenient example.


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build


%install
%py2_install
%py3_install


%check
%{__python2} setup.py test
%{__python3} setup.py test


# Note that there is no %%files section for the unversioned Python package
# if we are building for several Python runtimes
%files -n python2-%{srcname}
%license COPYING
%doc README
%{python2_sitelib}/*

%files -n python3-%{srcname}
%license COPYING
%doc README
%{python3_sitelib}/*


%changelog
...
