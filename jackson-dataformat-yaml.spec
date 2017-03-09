%{?scl:%scl_package jackson-dataformat-yaml}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}jackson-dataformat-yaml
Version:	2.7.6
Release:	3%{?dist}
Summary:	Jackson module to add YAML back-end (parser/generator adapters)
License:	ASL 2.0
URL:		http://wiki.fasterxml.com/JacksonExtensionYAML
Source0:	https://github.com/FasterXML/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz

BuildRequires:	%{?scl_prefix_maven}maven-local
BuildRequires:	%{?scl_prefix}jackson-annotations
BuildRequires:	%{?scl_prefix}jackson-core
BuildRequires:	%{?scl_prefix}jackson-databind
BuildRequires:	%{?scl_prefix}jackson-parent
BuildRequires:	%{?scl_prefix}replacer
BuildRequires:	%{?scl_prefix_maven}maven-failsafe-plugin
BuildRequires:	%{?scl_prefix}slf4j-log4j12
BuildRequires:	%{?scl_prefix}snakeyaml
BuildRequires:	%{?scl_prefix}fasterxml-oss-parent
%{?scl:Requires: %scl_runtime}

BuildArch:	noarch

%description
Support for reading and writing YAML-encoded data via Jackson
abstractions.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}

cp -p src/main/resources/META-INF/{LICENSE,NOTICE} .
sed -i 's/\r//' LICENSE NOTICE

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%pom_remove_plugin :maven-shade-plugin
%pom_remove_plugin org.apache.servicemix.tooling:depends-maven-plugin

%pom_xpath_remove "pom:properties/pom:osgi.private"

# test deps
%pom_remove_dep org.ops4j.pax.exam:pax-exam-container-native
%pom_remove_dep org.ops4j.pax.exam:pax-exam-junit4
%pom_remove_dep org.ops4j.pax.exam:pax-exam-link-mvn
%pom_remove_dep org.ops4j.pax.url:pax-url-aether
%pom_remove_dep :org.apache.felix.framework
rm -r src/test/java/com/fasterxml/jackson/dataformat/yaml/failsafe/OSGiIT.java

%mvn_file : %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc README.md release-notes/*
%license LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE NOTICE

%changelog
* Wed Mar 08 2017 Tomas Repik <trepik@redhat.com>
- scl conversion

* Mon Feb 06 2017 Michael Simacek <msimacek@redhat.com> - 2.7.6-2
- Remove unnecessary dep on felix-framework

* Mon Aug 22 2016 gil cattaneo <puntogil@libero.it> 2.7.6-1
- update to 2.7.6

* Fri Jun 24 2016 gil cattaneo <puntogil@libero.it> 2.6.7-1
- update to 2.6.7

* Thu May 26 2016 gil cattaneo <puntogil@libero.it> 2.6.6-1
- update to 2.6.6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 25 2015 gil cattaneo <puntogil@libero.it> 2.6.3-1
- update to 2.6.3

* Mon Sep 28 2015 gil cattaneo <puntogil@libero.it> 2.6.2-1
- update to 2.6.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 2.5.0-1
- update to 2.5.0

* Sat Sep 20 2014 gil cattaneo <puntogil@libero.it> 2.4.2-1
- update to 2.4.2

* Fri Jul 04 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

* Mon Nov 25 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- initial rpm
