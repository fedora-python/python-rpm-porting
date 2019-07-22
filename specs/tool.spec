%global srcname example

Name:           python-%{srcname}
Version:        1.2.3
Release:        2%{?dist}
Summary:        An example Python tool

License:        MIT
URL:            https://pypi.org/project/%{srcname}
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
# Here we have to think about the order, because the scripts in /usr/bin are
# overwritten with every setup.py install.
# If the script in /usr/bin provides the same functionality regardless
# of the Python version, we only provide Python 3 version and we need to run
# the py3_install after py2_install.

# If we need to include the executable both for Python 2 and 3--for example
# because it interacts with code from the user--then the default executable
# should be the one for Python 2.
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


# Note that there is no %%files section for the unversioned Python package
# if we are building for several Python runtimes
%files -n python2-%{srcname}
%license COPYING
%doc README
%{python2_sitelib}/*
%{_bindir}/sample-exec
%{_bindir}/sample-exec-2
%{_bindir}/sample-exec-%{python2_version}

%files -n python3-%{srcname}
%license COPYING
%doc README
%{python3_sitelib}/*
%{_bindir}/sample-exec-3
%{_bindir}/sample-exec-%{python3_version}


%changelog
...
