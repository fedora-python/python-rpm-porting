%global srcname example
%global sum An example python module

Name:           python-%{srcname}
Version:        1.2.3
Release:        1%{?dist}
Summary:        %{sum}

License:        MIT
URL:            http://pypi.python.org/pypi/%{srcname}
Source0:        http://pypi.python.org/packages/source/e/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel python3-devel

%description
An python module which provides a convenient example.


%package -n python2-%{srcname}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
An python module which provides a convenient example.


%package -n python3-%{srcname}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
An python module which provides a convenient example.


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build


%install
# We must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in case of conflict
# the Fedora Packaging Guidelines for Python specify that the default
# executable should be the one for python 2.
%py3_install
%py2_install

# The guidelines also specify we provide symlinks with a '-X' suffix.
ln -s %{_bindir}/sample-exec-%{python2_version} %{_bindir}/sample-exec-2
ln -s %{_bindir}/sample-exec-%{python3_version} %{_bindir}/sample-exec-3


%check
%{__python2} setup.py test
%{__python3} setup.py test


# Note that there is no %%files section for the unversioned python module
# if we are building for several python runtimes
%files -n python2-%{srcname}
%license COPYING
%doc README.rst
%{python2_sitelib}/*
%{_bindir}/sample-exec
%{_bindir}/sample-exec-2
%{_bindir}/sample-exec-%{python2_version}

%files -n python3-%{srcname}
%license COPYING
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/sample-exec-3
%{_bindir}/sample-exec-%{python3_version}

%changelog
