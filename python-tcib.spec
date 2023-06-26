%{!?upstream_version: %global upstream_version %{version}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order sphinx openstackdocstheme
%global pypi_name tcib

%global common_desc A repository to build OpenStack Services container \
images.

%{?!_licensedir:%global license %%doc}

Name:           python-%{pypi_name}
Summary:        A repository to build container images
Version:        XXX
Release:        XXX
License:        Apache-2.0
URL:            https://github.com/openstack-k8s-operators/tcib
Source0:        https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-osc-lib-tests

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:   A repository to build container images

Requires: %{name}-containers = %{version}-%{release}


%description -n python3-%{pypi_name}
%{common_desc}

%prep

%autosetup -n %{pypi_name}-%{upstream_version} -S git
rm -rf *.egg-info


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
# we switch data files to relative path in order to install them
# to the right place
sed -i 's/\/usr\///' setup.cfg

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/ansible/roles/
install -d -m 755 %{buildroot}%{_datadir}/ansible/roles/container_image_build
install -d -m 755 %{buildroot}%{_datadir}/ansible/roles/modify_container_image
install -d -m 755 %{buildroot}%{_datadir}/%{pypi_name}/roles/container-images

%check
%tox -e %{default_toxenv}

%package containers
Summary:   A repository to build container images

%description containers
This package installs the dependencies and files which are required on the base
TCIB container image.

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.dist-info
%{_datadir}/ansible/roles/

%files containers
%{_datadir}/%{pypi_name}
# Exclude build_containers ci specific role
%exclude %{_datadir}/%{pypi_name}/roles/container-images

%changelog
