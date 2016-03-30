%global srcname example
%global sum An example Python module

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
A Python module which provides a convenient example.


%package -n python2-%{srcname}
Summary:        %{sum}
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
A Python module which provides a convenient example.


%package -n python3-%{srcname}
Summary:        %{sum}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A Python module which provides a convenient example.


%prep
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build


%install
# Here we have to think about the order, because the scripts in /usr/bin are
# overwritten with every setup.py install.
# If the script in /usr/bin provides the same functionality regardless
# of the Python version, we only provide Python 3 version and we need to run
# the py3_install after py2_install.

# If the user needs both versions, because the Python version is
# important, then the default executable should be the one for Python 2
# and we need to provide some symlinks as well.
# We are going to assume that case here, because it is a bit more complex.

%py3_install

# Now /usr/bin/sample-exec is Python 3, so we move it away
mv %{buildroot}%{_bindir}/sample-exec %{buildroot}%{_bindir}/sample-exec-%{python3_version}

%py2_install

# Now /usr/bin/sample-exec is Python 2, and we move it away anyway
mv %{buildroot}%{_bindir}/sample-exec %{buildroot}%{_bindir}/sample-exec-%{python2_version}

# The guidelines also specify we must provide symlinks with a '-X' suffix.
ln -s ./sample-exec-%{python2_version} %{buildroot}%{_bindir}/sample-exec-2
ln -s ./sample-exec-%{python3_version} %{buildroot}%{_bindir}/sample-exec-3

# Finally, we provide /usr/bin/sample-exec as a link to /usr/bin/sample-exec-2
ln -s ./sample-exec-2 %{buildroot}%{_bindir}/sample-exec


%check
%{__python2} setup.py test
%{__python3} setup.py test


# Note that there is no %%files section for the unversioned Python module
# if we are building for several Python runtimes
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
