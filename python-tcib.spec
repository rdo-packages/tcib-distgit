%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}}
%global pypi_name tcib

%global common_desc A repository to build OpenStack Services container \
images.

%{?!_licensedir:%global license %%doc}

Name:           python-%{pypi_name}
Summary:        A repository to build container images
Version:        XXX
Release:        XXX
License:        ASL 2.0
URL:            https://github.com/openstack-k8s-operators/tcib
Source0:        https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
BuildRequires:  git-core
BuildRequires:  python3-pbr
BuildRequires:  openstack-macros 

# testing requirements
BuildRequires:  python3-stestr
BuildRequires:  python3-subunit
BuildRequires:  python3-oslotest
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-requests-mock
BuildRequires:  python3-osc-lib
BuildRequires:  python3-tenacity

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:   A repository to build container images

Requires: python3-pbr
Requires: python3-openstackclient
Requires: ansible-core
Requires: ansible-runner
Requires: python3-osc-lib
Requires: python3-oslo-config
Requires: python-oslo-log
Requires: python3-oslo-utils
Requires: python3-oslo-concurrency
Requires: python3-tenacity
Requires: python3-requests
Requires: python3-yaml

Requires: %{name}-containers = %{version}-%{release}

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
%{common_desc}

%prep

%autosetup -n %{pypi_name}-%{upstream_version} -S git
rm -rf *.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

%install
%{py3_install}

%check
export PYTHON=%{__python3}
stestr run

%package containers
Summary:   A repository to build container images

%description containers
This package installs the dependencies and files which are required on the base
TCIB container image.

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{_datadir}/ansible/roles/
# Exclude build_containers ci specific role
%exclude %{_datadir}/ansible/roles/build_containers
%exclude %{_datadir}/%{pypi_name}/healthcheck
%exclude %{_datadir}/%{pypi_name}/container-images

%files containers
%{_datadir}/%{pypi_name}/healthcheck
%{_datadir}/%{pypi_name}/container-images