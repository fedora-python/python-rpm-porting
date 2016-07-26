%global srcname example

Name:           python-%{srcname}
Version:        1.2.3
Release:        2%{?dist}
Summary:        An example Python tool

License:        MIT
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python3-devel

%description
A Python tool which provides a convenient example.


%package -n python2-%{srcname}
Summary:        %{summary}
Requires:       python-some-module
Requires:       python2-other-module
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A Python tool which provides a convenient example.


%package -n python3-%{srcname}
Summary:        %{summary}
Requires:       python3-some-module
Requires:       python3-other-module
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A Python tool which provides a convenient example.


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build


%install
%py2_install

# The Python 2 installation process will likely try to install its own version
# of the application. As we only want to package the Python 3 version of the
# application, we delete the Python 2 executable(s) so that the Python 3
# version(s) can take their place afterwards.
rm %{buildroot}%{_bindir}/*

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
%{_bindir}/sample-exec


%changelog
...
