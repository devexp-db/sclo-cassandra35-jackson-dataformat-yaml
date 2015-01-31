Name:          jackson-dataformat-yaml
Version:       2.5.0
Release:       1%{?dist}
Summary:       Jackson module to add YAML back-end (parser/generator adapters)
License:       ASL 2.0
URL:           http://wiki.fasterxml.com/JacksonExtensionYAML
Source0:       https://github.com/FasterXML/jackson-dataformat-yaml/archive/%{name}-%{version}.tar.gz
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: mvn(com.fasterxml.jackson.core:jackson-core)
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-databind)
%if %{?fedora} > 20
BuildRequires: mvn(com.fasterxml.jackson:jackson-parent:pom:)
%else
BuildRequires: mvn(com.fasterxml.jackson:jackson-parent)
%endif
BuildRequires: mvn(org.yaml:snakeyaml)
# Test deps
BuildRequires: mvn(com.fasterxml.jackson.core:jackson-annotations)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:org.apache.felix.framework)
BuildRequires: mvn(org.slf4j:slf4j-log4j12)

BuildRequires: maven-local
BuildRequires: mvn(com.google.code.maven-replacer-plugin:replacer)
BuildRequires: mvn(org.apache.maven.plugins:maven-failsafe-plugin)

BuildArch:     noarch

%description
Support for reading and writing YAML-encoded data via Jackson
abstractions.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

cp -p %{SOURCE1} .
cp -p src/main/resources/META-INF/{LICENSE,NOTICE} .
sed -i 's/\r//' LICENSE NOTICE LICENSE-2.0.txt

%pom_remove_plugin :maven-shade-plugin
%pom_remove_plugin org.apache.servicemix.tooling:depends-maven-plugin

%pom_xpath_remove "pom:properties/pom:osgi.private"
%pom_xpath_remove "pom:properties/pom:osgi.import"
%pom_xpath_inject "pom:properties" "
    <osgi.import>
com.fasterxml.jackson.core,
com.fasterxml.jackson.core.base,
com.fasterxml.jackson.core.format,
com.fasterxml.jackson.core.io,
com.fasterxml.jackson.core.json,
com.fasterxml.jackson.core.type,
com.fasterxml.jackson.core.util,
com.fasterxml.jackson.databind,
org.yaml.snakeyaml,
org.yaml.snakeyaml.emitter,
org.yaml.snakeyaml.error,
org.yaml.snakeyaml.events,
org.yaml.snakeyaml.parser,
org.yaml.snakeyaml.reader
</osgi.import>"

# test deps
# pax-exam 4.3.0
%pom_remove_dep org.ops4j.pax.exam:pax-exam-container-native
%pom_remove_dep org.ops4j.pax.exam:pax-exam-junit4
%pom_remove_dep org.ops4j.pax.exam:pax-exam-link-mvn
# pax-url 2.2.0
%pom_remove_dep org.ops4j.pax.url:pax-url-aether
rm -r src/test/java/com/fasterxml/jackson/dataformat/yaml/failsafe/OSGiIT.java

%mvn_file : %{name}

%build

%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc README.md release-notes/*
%license LICENSE LICENSE-2.0.txt NOTICE

%files javadoc -f .mfiles-javadoc
%license LICENSE LICENSE-2.0.txt NOTICE

%changelog
* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 2.5.0-1
- update to 2.5.0

* Sat Sep 20 2014 gil cattaneo <puntogil@libero.it> 2.4.2-1
- update to 2.4.2

* Fri Jul 04 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

* Mon Nov 25 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- initial rpm
